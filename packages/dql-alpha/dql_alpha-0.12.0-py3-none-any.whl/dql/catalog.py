import logging
import os
import os.path
import posixpath
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
)

import yaml
from dvc_data.hashfile.db.local import LocalHashFileDB
from dvc_objects.fs.local import LocalFileSystem as _LocalFileSystem
from fsspec.implementations.local import LocalFileSystem
from tqdm import tqdm

from dql.client import Client
from dql.data_storage import AbstractDataStorage
from dql.dataset import DatasetRecord, DatasetRow
from dql.dataset import Status as DatasetStatus
from dql.listing import Listing
from dql.node import NodeWithPath
from dql.storage import Status, Storage
from dql.utils import DQLDir, dql_paths_join

logger = logging.getLogger("dql")

DEFAULT_DATASET_DIR = "dataset"
DATASET_FILE_SUFFIX = ".dql"

TTL_INT = 4 * 60 * 60

T = TypeVar("T")


class PendingIndexingError(Exception):
    pass


class DataSource:
    def __init__(self, listing, node):
        self.listing = listing
        self.node = node

    def get_full_path(self):
        return self.get_node_full_path(self.node)

    def get_node_full_path(self, node):
        return self.listing.client.get_full_path(node.full_path)


@dataclass
class NodeGroup:
    """Class for a group of nodes from the same source"""

    listing: Listing
    nodes: List[NodeWithPath]

    # The source path within the bucket
    # (not including the bucket name or s3:// prefix)
    source_path: str = ""


def check_output_dataset_file(
    output: str,
    force: bool = False,
    dataset_filename: Optional[str] = None,
    skip_check_output: bool = False,
    skip_check_dql: bool = False,
) -> str:
    """
    Checks the output directory and dataset filename for existence or if they
    should be force-overwritten.
    """
    if not skip_check_output:
        if os.path.exists(output):
            if force:
                shutil.rmtree(output)
            else:
                raise RuntimeError(f"Output directory already exists: {output}")

    dataset_file = (
        dataset_filename if dataset_filename else output + DATASET_FILE_SUFFIX
    )
    if not skip_check_dql:
        if os.path.exists(dataset_file):
            if force:
                os.remove(dataset_file)
            else:
                raise RuntimeError(
                    f"Output dataset file already exists: {dataset_file}"
                )
    return dataset_file


def parse_dql_file(filename: str) -> List[Dict[str, Any]]:
    with open(filename, encoding="utf-8") as f:
        contents = yaml.safe_load(f)

    if not isinstance(contents, list):
        contents = [contents]

    for entry in contents:
        if not isinstance(entry, dict):
            raise ValueError(
                "Failed parsing DQL file, "
                "each data source entry must be a dictionary"
            )
        if "data-source" not in entry or "files" not in entry:
            raise ValueError(
                "Failed parsing DQL file, "
                "each data source entry must contain the "
                '"data-source" and "files" keys'
            )

    return contents


def prepare_output_for_cp(
    node_groups: List[NodeGroup],
    output: str,
    force: bool = False,
    dql_only: bool = False,
    no_dql_file: bool = False,
) -> Tuple[bool, Optional[str]]:
    total_node_count = 0
    for node_group in node_groups:
        if not node_group.nodes:
            raise FileNotFoundError(
                f"No such file or directory: {node_group.source_path}"
            )
        total_node_count += len(node_group.nodes)

    always_copy_dir_contents = False
    copy_to_filename = None

    if dql_only:
        return always_copy_dir_contents, copy_to_filename

    if not os.path.isdir(output):
        if total_node_count == 1:
            first_node: NodeWithPath = node_groups[0].nodes[0]
            if first_node.is_dir:
                if os.path.exists(output):
                    if force:
                        os.remove(output)
                    else:
                        raise FileExistsError(f"Path already exists: {output}")
                always_copy_dir_contents = True
                os.mkdir(output)
            else:  # Is a File
                if os.path.exists(output):
                    if force:
                        os.remove(output)
                    else:
                        raise FileExistsError(f"Path already exists: {output}")
                copy_to_filename = output
        else:
            raise FileNotFoundError(f"Is not a directory: {output}")

    if copy_to_filename and not no_dql_file:
        raise RuntimeError("File to file cp not supported with .dql files!")

    return always_copy_dir_contents, copy_to_filename


def collect_nodes_for_cp(
    node_groups: Iterable[NodeGroup],
    recursive: bool = False,
) -> Tuple[int, int]:
    total_size: int = 0
    total_files: int = 0

    # Collect all nodes to process
    for node_group in node_groups:
        listing: Listing = node_group.listing
        valid_nodes: List[NodeWithPath] = []
        for node in node_group.nodes:
            if node.is_dir:
                if not recursive:
                    print(f"{node.full_path} is a directory (not copied).")
                    continue
                add_size, add_files = listing.du(node)
                total_size += add_size
                total_files += add_files
                valid_nodes.append(node)
            else:
                # This node is a file
                total_size += node.size
                total_files += 1
                valid_nodes.append(node)

        node_group.nodes = valid_nodes

    return total_size, total_files


def download_node_groups(
    node_groups: Iterable[NodeGroup],
    cache: LocalHashFileDB,
    bar_format: str,
    total_size: int,
    recursive: bool = False,
):
    download_progress_bar = tqdm(
        desc="Downloading files: ",
        unit="B",
        bar_format=bar_format,
        unit_scale=True,
        unit_divisor=1000,
        total=total_size,
    )

    # Download these nodes
    for node_group in node_groups:
        if not node_group.nodes:
            continue
        listing: Listing = node_group.listing

        updated_nodes: List[NodeWithPath] = listing.download_nodes(
            node_group.nodes,
            cache,
            total_size,
            recursive=recursive,
            shared_progress_bar=download_progress_bar,
        )

        # This assert is hopefully not necessary, but is here mostly to
        # ensure this functionality stays consistent (and catch any bugs)
        assert len(node_group.nodes) == len(updated_nodes)

        node_group.nodes = updated_nodes

    download_progress_bar.close()


def instantiate_node_groups(
    node_groups: Iterable[NodeGroup],
    cache: LocalHashFileDB,
    output: str,
    bar_format: str,
    total_files: int,
    force: bool = False,
    recursive: bool = False,
    virtual_only: bool = False,
    always_copy_dir_contents: bool = False,
    copy_to_filename: Optional[str] = None,
) -> List[Dict[str, Any]]:
    instantiate_progress_bar = (
        None
        if virtual_only
        else tqdm(
            desc=f"Instantiating {output}: ",
            unit=" f",
            bar_format=bar_format,
            unit_scale=True,
            unit_divisor=1000,
            total=total_files,
        )
    )

    metafile_data = []

    # Instantiate these nodes
    for node_group in node_groups:
        if not node_group.nodes:
            continue
        listing: Listing = node_group.listing
        source_path: str = node_group.source_path
        metafile_group = {
            "data-source": listing.storage.to_dict(source_path),
            "files": [],
        }
        output_dir = output
        if copy_to_filename:
            output_dir = os.path.dirname(output)
            if not output_dir:
                output_dir = "."
            node_group.nodes = [
                node._replace(path=[], name=os.path.basename(output))  # type: ignore [call-arg] # noqa: E501
                for node in node_group.nodes
            ]
        copy_dir_contents = always_copy_dir_contents or source_path.endswith("/")
        instantiated_nodes = listing.collect_nodes_to_instantiate(
            node_group.nodes,
            recursive,
            copy_dir_contents,
            source_path,
        )
        if not virtual_only:
            listing.instantiate_nodes(
                instantiated_nodes,
                output_dir,
                cache,
                total_files,
                force=force,
                shared_progress_bar=instantiate_progress_bar,
            )

        for node in instantiated_nodes:
            if not node.is_dir:
                metafile_group["files"].append(node.get_metafile_data())
        if metafile_group["files"]:
            metafile_data.append(metafile_group)

    if instantiate_progress_bar:
        instantiate_progress_bar.close()

    return metafile_data


def trim_node_path(node: NodeWithPath) -> NodeWithPath:
    return node._replace(path=node.path[:-1])  # type: ignore[call-arg,attr-defined]


def find_column_to_str(node: NodeWithPath, src: DataSource, column: str) -> str:
    if column == "du":
        return str(src.listing.du(node)[0])
    if column == "name":
        return node.name or ""
    if column == "owner":
        return node.owner_name or ""
    if column == "path":
        return src.get_node_full_path(node)
    if column == "size":
        return str(node.size)
    if column == "type":
        return "d" if node.is_dir else "f"
    return ""


class Catalog:
    def __init__(
        self,
        data_storage: AbstractDataStorage,
        cache_dir=None,
        tmp_dir=None,
    ):
        dql_dir = DQLDir(cache=cache_dir, tmp=tmp_dir)
        self.data_storage = data_storage
        self.cache = LocalHashFileDB(
            _LocalFileSystem(),
            dql_dir.cache,
            tmp_dir=dql_dir.tmp,
        )

    def add_storage(self, source: str, symlinks: bool = False) -> None:
        # pylint:disable-next=protected-access
        path = LocalFileSystem._strip_protocol(source)
        if not os.path.isdir(path):
            raise RuntimeError(f"{path} is not a directory")
        uri = Path(path).as_uri()
        print(f"Registering storage {uri}")
        self.data_storage.create_storage_if_not_registered(uri, symlinks)

    def parse_url(self, uri: str, **config: Any) -> Tuple[Client, str]:
        return Client.parse_url(uri, self.data_storage, **config)

    def enlist_source(
        self,
        source: str,
        ttl: int,
        force_update=False,
        skip_indexing=False,
        to_fetch=True,
        client_config=None,
    ) -> Tuple[Listing, str]:
        if force_update and skip_indexing:
            raise ValueError(
                "Both force_update and skip_indexing flags"
                " cannot be True at the same time"
            )

        client_config = client_config or {}
        client, path = self.parse_url(source, **client_config)
        prefix = posixpath.dirname(path)
        source_data_storage = self.data_storage.clone(uri=client.uri)

        if skip_indexing:
            source_data_storage.create_storage_if_not_registered(client.uri)
            storage = source_data_storage.get_storage(client.uri)
            assert storage
            return (
                Listing(storage, source_data_storage, client),
                path,
            )

        (
            storage,
            need_index,
            in_progress,
            is_new,
        ) = source_data_storage.register_storage_for_indexing(
            client.uri, force_update, prefix
        )
        if in_progress:
            raise PendingIndexingError(f"Pending indexing operation: uri={storage.uri}")

        lst = Listing(storage, source_data_storage, client)

        if not need_index:
            logger.debug(  # type: ignore[unreachable]
                f"Using cached listing {storage.uri}."
                + f" Valid till: {storage.expires_to_local}"
            )
            # Listing has to have correct version of data storage
            # initialized with correct Storage
            return lst, path

        if to_fetch:
            try:
                source_data_storage.init_db(prefix, is_new)
                lst.fetch(prefix)
                source_data_storage.validate_paths()
                source_data_storage.mark_storage_indexed(
                    storage.uri,
                    Status.PARTIAL if prefix else Status.COMPLETE,
                    ttl,
                    prefix=prefix,
                )
            except:  # noqa: E722,B001
                source_data_storage.mark_storage_indexed(
                    storage.uri, Status.FAILED, ttl, prefix=prefix
                )
                raise
            lst.storage = storage
        else:
            source_data_storage.init_db()
        return lst, path

    def enlist_sources(
        self,
        sources: List[str],
        ttl: int,
        update: bool,
        skip_indexing=False,
        client_config=None,
    ) -> List["DataSource"]:
        enlisted_sources = []
        for src in sources:  # Opt: parallel
            listing, file_path = self.enlist_source(
                src,
                ttl,
                update,
                skip_indexing=skip_indexing,
                client_config=client_config,
            )
            enlisted_sources.append((listing, file_path))

        dsrc_all = []
        for listing, file_path in enlisted_sources:
            nodes = listing.expand_path(file_path)
            for node in nodes:
                dsrc_all.append(DataSource(listing, node))

        return dsrc_all

    def enlist_sources_grouped(
        self,
        sources: List[str],
        ttl: int,
        update: bool,
        no_glob: bool = False,
        client_config=None,
    ) -> List[NodeGroup]:
        enlisted_sources: List[Tuple[bool, Any]] = []
        for src in sources:  # Opt: parallel
            if src.endswith(DATASET_FILE_SUFFIX) and os.path.isfile(src):
                # TODO: Also allow using DQL files from cloud locations?
                dql_data = parse_dql_file(src)
                indexed_sources = []
                for ds in dql_data:
                    listing, source_path = self.enlist_source(
                        ds["data-source"]["uri"],
                        ttl,
                        update,
                        client_config=client_config,
                    )
                    paths = dql_paths_join(
                        source_path, (f["name"] for f in ds["files"])
                    )
                    indexed_sources.append((listing, source_path, paths))
                enlisted_sources.append((True, indexed_sources))
            else:
                listing, source_path = self.enlist_source(
                    src, ttl, update, client_config=client_config
                )
                enlisted_sources.append((False, (listing, source_path)))

        node_groups = []
        nodes: List[NodeWithPath] = []
        for is_dql, payload in enlisted_sources:  # Opt: parallel
            if is_dql:
                for listing, source_path, paths in payload:
                    nodes = [trim_node_path(listing.resolve_path(p)) for p in paths]
                    node_groups.append(NodeGroup(listing, nodes, source_path))
            else:
                listing, source_path = payload
                if no_glob:
                    nodes = [trim_node_path(listing.resolve_path(source_path))]
                else:
                    nodes = listing.expand_path(source_path)
                    if len(nodes) == 1 and not nodes[0].is_dir:
                        nodes = [trim_node_path(nodes[0])]

                node_groups.append(NodeGroup(listing, nodes, source_path))

        return node_groups

    def create_shadow_dataset(
        self,
        name: str,
        sources: List[str],
        client_config=None,
        recursive=False,
        populate=True,
    ) -> DatasetRecord:
        """
        Creates shadow dataset in DB if it doesn't exist and updates it with
        entries from sources.
        Example of sources:
            s3://bucket_name/dir1/dir2/*
            s3://bucket_name/*
            s3://bucket_name/image_*
        """
        client_config = client_config or {}
        dataset = self.data_storage.create_shadow_dataset(name, create_rows=populate)
        assert dataset
        if not populate:
            # returning empty dataset without dataset rows table and data inside
            return dataset

        final_status = DatasetStatus.FAILED
        try:
            for source in sources:
                client, path = self.parse_url(source, **client_config)
                self.data_storage.insert_into_shadow_dataset(
                    name, client.uri, path, recursive=recursive
                )
            final_status = DatasetStatus.COMPLETE
        finally:
            self.data_storage.update_dataset_status(dataset, final_status)

        return dataset

    def register_shadow_dataset(
        self,
        shadow_name: str,
        registered_name: Optional[str] = None,
        version: Optional[int] = None,
        description: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ):
        """
        Method for registering shadow dataset as a new dataset with version 1, or
        as a new version of existing registered dataset
        """
        version = version or 1

        # getting shadow dataset
        shadow_dataset = self.data_storage.get_dataset(shadow_name)
        if not shadow_dataset:
            raise ValueError(f"Shadow dataset {shadow_name} doesn't exist")

        if not shadow_dataset.shadow:
            raise ValueError(f"Dataset {shadow_name} must be shadow")

        registered_dataset = (
            self.data_storage.get_dataset(registered_name) if registered_name else None
        )

        if registered_dataset:
            # if registered dataset already exists, we are creating new version
            # of it out of shadow dataset
            version = version or registered_dataset.next_version
            if not registered_dataset.is_valid_next_version(version):
                raise ValueError(
                    f"Version {version} must be higher than the current latest one"
                )

            self.data_storage.create_dataset_version(
                registered_dataset.name, version, create_rows_table=False
            )
            # to avoid re-creating rows table, we are just taking shadow one and
            # renaming it for a new version of registered one
            self.data_storage.rename_dataset_table(
                shadow_dataset.name,
                registered_dataset.name,
                old_version=None,
                new_version=version,
            )
            # finally, we are removing shadow dataset from datasets table
            self.data_storage.remove_shadow_dataset(shadow_dataset, drop_rows=False)
            return

        # if registered dataset doesn't exist we are modifying shadow dataset
        # to become registered one
        update_data = {
            "shadow": False,
            "description": description,
            "labels": labels,
        }

        if registered_name:
            update_data["name"] = registered_name

        self.data_storage.update_dataset(shadow_name, **update_data)
        self.data_storage.create_dataset_version(
            registered_name or shadow_name,
            version,
            create_rows_table=False,
        )
        self.data_storage.rename_dataset_table(
            registered_name or shadow_name,
            registered_name or shadow_name,
            old_version=None,
            new_version=version,
        )

    def ls_datasets(self, shadow_only=None) -> Iterable[DatasetRecord]:
        yield from self.data_storage.get_datasets(shadow_only=shadow_only)

    def ls_dataset_rows(
        self, name: str, limit=None, version=None
    ) -> Iterable[DatasetRow]:
        dataset = self.data_storage.get_dataset(name)
        assert dataset
        if not dataset.shadow and not version:
            raise ValueError(
                f"Missing dataset version from input for registered dataset {name}"
            )

        yield from self.data_storage.get_dataset_rows(
            name, limit=limit, version=version
        )

    def remove_dataset(
        self,
        name: str,
        version: Optional[int] = None,
        force: Optional[bool] = False,
    ):
        dataset = self.data_storage.get_dataset(name)
        assert dataset
        if dataset.registered and not version and not force:
            raise ValueError(
                f"Missing dataset version from input for registered dataset {name}"
            )
        if version and not dataset.has_version(version):
            raise RuntimeError(f"Dataset {name} doesn't have version {version}")

        if dataset.registered and version:
            # removing one version of registered dataset
            self.data_storage.remove_dataset_version(dataset, version)

        elif dataset.registered and force:
            for version in dataset.versions.copy():  # type: ignore [union-attr]
                self.data_storage.remove_dataset_version(dataset, version)
        else:
            self.data_storage.remove_shadow_dataset(dataset)

    def edit_dataset(
        self,
        name: str,
        new_name: Optional[str] = None,
        description: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ):
        update_data = {}
        if new_name:
            update_data["name"] = new_name
        if description:
            update_data["description"] = description
        if labels:
            update_data["labels"] = labels  # type: ignore[assignment]

        self.data_storage.update_dataset(name, **update_data)

    def merge_datasets(
        self,
        src_name: str,
        dst_name: str,
        src_version: Optional[int] = None,
        dst_version: Optional[int] = None,
    ) -> DatasetRecord:
        """
        Merges records from source to destination dataset.
        If destination dataset is shadow, it will copy all the records from source
        dataset to shadow one
        If destination dataset is registered, it will create a new version
        of dataset with records merged from old version and the source
        """

        src = self.data_storage.get_dataset(src_name)
        dst = self.data_storage.get_dataset(dst_name)

        # validation
        if not src:
            raise ValueError(f"Source dataset {src_name} doesn't exist")
        if src.shadow and src_version:
            raise ValueError(
                f"Source dataset {src_name} is shadow, cannot use it with versions"
            )
        if not src.shadow and not src_version:
            raise ValueError(f"Source dataset {src_name} is registered, need a version")
        if not dst:
            raise ValueError(f"Dataset {dst_name} doesn't exist")
        if dst.shadow and dst_version:
            raise ValueError(
                f"Dataset {dst_name} is shadow, cannot use it with versions"
            )

        if dst_version and not dst.is_valid_next_version(dst_version):
            raise ValueError(
                f"Version {dst_version} must be higher than the current latest one"
            )

        if dst.shadow:
            self.data_storage.merge_dataset_rows(
                src,
                dst,
                src_version,
                dst_version=None,
            )
        else:
            dst_version = dst_version or dst.next_version
            dst = self.data_storage.create_dataset_version(dst_name, dst_version)
            self.data_storage.merge_dataset_rows(
                src,
                dst,
                src_version,
                dst_version,
            )

        return dst

    def read_object(
        self, row: DatasetRow, reader: Callable[[Any], T], **config: Any
    ) -> T:
        client, _ = self.parse_url(row.source, **config)
        with client.open(row.path_str) as f:
            return reader(f)

    def ls(
        self,
        sources: List[str],
        ttl=TTL_INT,
        update=False,
        skip_indexing=False,
        *,
        client_config=None,
    ) -> Iterator[Tuple[DataSource, Iterator[NodeWithPath]]]:
        data_sources = self.enlist_sources(
            sources,
            ttl,
            update,
            skip_indexing=skip_indexing,
            client_config=client_config,
        )

        for source in data_sources:
            yield source, iter(source.listing.ls_path(source.node))

    def ls_storages(self) -> Iterator[Storage]:
        yield from self.data_storage.get_storage_all()

    def get(
        self,
        source,
        output,
        force=False,
        update=False,
        ttl=TTL_INT,
        *,
        client_config=None,
    ) -> None:
        listing, file_path = self.enlist_source(
            source, ttl, update, client_config=client_config
        )

        if not output:
            if file_path:
                output = os.path.basename(file_path.rstrip("/"))
            else:
                output = listing.storage.name

        dataset_file = check_output_dataset_file(output, force)

        node = listing.resolve_path(file_path)
        total_size, total_files = listing.du(node)
        listing.download_subtree(node, self.cache, total_size)
        listing.instantiate_subtree(node, output, self.cache, total_files)
        listing.metafile_for_subtree(file_path, node, dataset_file)

    def cp(
        self,
        sources: List[str],
        output: str,
        force: bool = False,
        update: bool = False,
        recursive: bool = False,
        dql_file: Optional[str] = None,
        dql_only: bool = False,
        no_glob: bool = False,
        no_dql_file: bool = False,
        create_dataset: bool = False,
        ttl: int = TTL_INT,
        *,
        client_config=None,
    ) -> List[Dict[str, Any]]:
        node_groups = self.enlist_sources_grouped(
            sources,
            ttl,
            update,
            no_glob,
            client_config=client_config,
        )

        always_copy_dir_contents, copy_to_filename = prepare_output_for_cp(
            node_groups, output, force, dql_only, no_dql_file
        )

        dataset_file = check_output_dataset_file(
            output, force, dql_file, True, no_dql_file
        )

        total_size, total_files = collect_nodes_for_cp(node_groups, recursive)

        if total_files == 0:
            # Nothing selected to cp
            return []

        desc_max_len = max(len(output) + 16, 19)
        bar_format = (
            "{desc:<"
            f"{desc_max_len}"
            "}{percentage:3.0f}%|{bar}| {n_fmt:>5}/{total_fmt:<5} "
            "[{elapsed}<{remaining}, {rate_fmt:>8}]"
        )

        if not dql_only:
            download_node_groups(
                node_groups, self.cache, bar_format, total_size, recursive
            )

        metafile_data = instantiate_node_groups(
            node_groups,
            self.cache,
            output,
            bar_format,
            total_files,
            force,
            recursive,
            dql_only,
            always_copy_dir_contents,
            copy_to_filename,
        )

        if create_dataset:
            self.create_shadow_dataset(
                output, sources, client_config, recursive=recursive
            )

        if not metafile_data or no_dql_file:
            # Don't write the metafile if nothing was copied (or skipped)
            return metafile_data

        print(f"Creating '{dataset_file}'")
        with open(dataset_file, "w", encoding="utf-8") as fd:
            yaml.dump(metafile_data, fd, sort_keys=False)

        return metafile_data

    def du(
        self,
        sources,
        depth=0,
        ttl=TTL_INT,
        update=False,
        *,
        client_config=None,
    ) -> Iterable[Tuple[str, float]]:
        sources = self.enlist_sources(
            sources,
            ttl,
            update,
            client_config=client_config,
        )

        def du_dirs(src, node, subdepth):
            if subdepth > 0:
                subdirs = src.listing.data_storage.get_nodes_by_parent_id(
                    node.id, type="dir"
                )
                for sd in subdirs:
                    yield from du_dirs(src, sd, subdepth - 1)
            yield (src.get_node_full_path(node), src.listing.du(node)[0])

        for src in sources:
            yield from du_dirs(src, src.node, depth)

    def find(
        self,
        sources,
        ttl=TTL_INT,
        update=False,
        names=None,
        inames=None,
        paths=None,
        ipaths=None,
        size=None,
        typ=None,
        jmespath=None,
        columns=None,
        *,
        client_config=None,
    ) -> Iterable[str]:
        sources = self.enlist_sources(
            sources,
            ttl,
            update,
            client_config=client_config,
        )
        if not columns:
            columns = ["path"]
        for src in sources:
            nodes = src.listing.find(
                src.node, names, inames, paths, ipaths, size, typ, jmespath
            )
            for node in nodes:
                yield "\t".join(
                    [find_column_to_str(node, src, column) for column in columns]
                )

    def index(
        self, sources, ttl=TTL_INT, update=False, *, client_config=None
    ) -> List["DataSource"]:
        root_sources = [
            src for src in sources if Client.get_implementation(src).is_root_url(src)
        ]
        non_root_sources = [
            src
            for src in sources
            if not Client.get_implementation(src).is_root_url(src)
        ]

        client_config = client_config or {}

        # for root sources (e.g s3://) we are just getting all buckets and
        # saving them as storages, without further indexing in each bucket
        for source in root_sources:
            for bucket in Client.get_implementation(source).ls_buckets(**client_config):
                client, _ = self.parse_url(bucket.uri)
                print(f"Registering storage {client.uri}")
                self.data_storage.create_storage_if_not_registered(client.uri)

        return self.enlist_sources(
            non_root_sources,
            ttl,
            update,
            client_config=client_config,
        )

    def find_stale_storages(self) -> None:
        self.data_storage.find_stale_storages()
