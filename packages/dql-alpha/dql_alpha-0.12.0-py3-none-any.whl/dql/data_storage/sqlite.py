import hashlib
import json
import logging
import operator
import os
import posixpath
import sqlite3
from datetime import MAXYEAR, MINYEAR, datetime, timezone
from functools import partial, wraps
from itertools import groupby
from time import sleep
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import sqlalchemy
from sqlalchemy import select, update
from sqlalchemy.dialects.sqlite import dialect as get_sqlite_dialect
from sqlalchemy.schema import CreateTable

from dql.data_storage.abstract import AbstractDataStorage
from dql.dataset import DATASET_ROW_FIELDS, DatasetRecord, DatasetRow
from dql.dataset import Status as DatasetStatus
from dql.dataset import dataset_table
from dql.error import DQLError
from dql.node import AnyNode, DirType, Node, NodeWithPath
from dql.storage import Status as StorageStatus
from dql.storage import Storage
from dql.utils import GLOB_CHARS, DQLDir, is_expired

from .query import Query, Schema

if TYPE_CHECKING:
    from sqlalchemy.sql.elements import ColumnClause, CompilerElement, TextClause

logger = logging.getLogger("dql")

RETRY_START_SEC = 0.01
RETRY_MAX_TIMES = 10
RETRY_FACTOR = 2

Column = Union[str, "ColumnClause[Any]", "TextClause"]

# sqlite 3.31.1 is the earliest version tested in CI
if sqlite3.sqlite_version_info < (3, 31, 1):
    logger.warning(
        "Possible sqlite incompatibility. The earliest tested version of "
        f"sqlite is 3.31.1 but you have {sqlite3.sqlite_version}"
    )


sqlite_dialect = get_sqlite_dialect(paramstyle="named")


def compile_statement(
    statement: "CompilerElement",
) -> Union[Tuple[str], Tuple[str, Dict[str, Any]]]:
    compiled = statement.compile(dialect=sqlite_dialect)
    if compiled.params is None:
        return (compiled.string,)
    return compiled.string, compiled.params


def select_table(
    table: str,
    columns: Optional[Sequence[Column]] = None,
):
    column_objects: List[Union["ColumnClause[Any]", "TextClause"]]
    if columns is None:
        column_objects = [sqlalchemy.text("*")]
    else:
        column_objects = [
            sqlalchemy.column(c) if isinstance(c, str) else c for c in columns
        ]
    return select(*column_objects).select_from(sqlalchemy.table(table))


def adapt_datetime(val: datetime) -> str:
    if not (val.tzinfo is timezone.utc or val.tzname() == "UTC"):
        try:
            val = val.astimezone(timezone.utc)
        except (OverflowError, ValueError, OSError):
            if val.year == MAXYEAR:
                val = datetime.max
            elif val.year == MINYEAR:
                val = datetime.min
            else:
                raise
    return val.replace(tzinfo=None).isoformat(" ")


def convert_datetime(val: bytes) -> datetime:
    return datetime.fromisoformat(val.decode()).replace(tzinfo=timezone.utc)


sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("datetime", convert_datetime)


class NodeSchema(Schema):
    fields = [
        "id",
        "dir_type",
        "parent_id",
        "name",
        "checksum",
        "etag",
        "version",
        "is_latest",
        "last_modified",
        "size",
        "owner_name",
        "owner_id",
        "path_str",
        "anno",
        "valid",
    ]

    def lookup_type(self, query, _, value):
        if value in {"f", "file", "files"}:
            return query.compile_op("dir_type", "eq", DirType.FILE)
        elif value in {"d", "dir", "directory", "directories"}:
            return query.compile_op("dir_type", "ne", DirType.FILE)
        else:
            return None


DATASET_FIELDS = [
    "name",
    "shadow",
    "description",
    "version",
    "labels",
    "status",
    "created_at",
    "finished_at",
]

PATH_STR_INDEX = NodeSchema.fields.index("path_str")


class StorageSchema(Schema):
    table = "buckets"
    fields = [
        "uri",
        "timestamp",
        "expires",
        "started_inserting_at",
        "last_inserted_at",
        "status",
        "symlinks",
    ]


class PartialSchema(Schema):
    fields = ["path_str", "timestamp", "expires"]


def get_retry_sleep_sec(retry_count: int) -> int:
    return RETRY_START_SEC * (RETRY_FACTOR**retry_count)


def retry_sqlite_locks(func):
    # This retries the database modification in case of concurrent access
    @wraps(func)
    def wrapper(*args, **kwargs):
        exc = None
        for retry_count in range(RETRY_MAX_TIMES):
            try:
                return func(*args, **kwargs)
            except sqlite3.OperationalError as operror:
                exc = operror
                sleep(get_retry_sleep_sec(retry_count))
        raise exc

    return wrapper


def retry_sqlite_locks_async(func):
    # This retries the database modification in case of concurrent access
    # (For async code)
    @wraps(func)
    async def wrapper(*args, **kwargs):
        exc = None
        for retry_count in range(RETRY_MAX_TIMES):
            try:
                return await func(*args, **kwargs)
            except sqlite3.OperationalError as operror:
                exc = operror
                sleep(get_retry_sleep_sec(retry_count))
        raise exc

    return wrapper


class SQLiteDataStorage(AbstractDataStorage):
    """
    SQLite data storage uses SQLite3 for storing indexed data locally.
    This is currently used for the cli although could potentially support or
    be expanded for cloud storage as well.
    """

    LISTING_TABLE_NAME_PREFIX = "dsrc_"
    DATASET_TABLE_PREFIX = "ds_"
    TABLE_NAME_SHA_LIMIT = 12

    def __init__(self, db_file: Optional[str] = None, uri: str = ""):
        self.uri = uri.rstrip("/")
        self.db_file = db_file if db_file else DQLDir.find().db
        detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES

        try:
            if self.db_file == ":memory:":
                # Enable multithreaded usage of the same in-memory db
                self.db = sqlite3.connect(
                    "file::memory:?cache=shared", uri=True, detect_types=detect_types
                )
            else:
                self.db = sqlite3.connect(self.db_file, detect_types=detect_types)
            self.engine = sqlalchemy.create_engine(
                "sqlite+pysqlite:///", creator=lambda: self.db, future=True
            )

            self.db.isolation_level = None  # Use autocommit mode
            self.db.execute("PRAGMA foreign_keys = ON")
            self.db.execute("PRAGMA cache_size = -102400")  # 100 MiB
            # Enable Write-Ahead Log Journaling
            self.db.execute("PRAGMA journal_mode = WAL")
            self.db.execute("PRAGMA synchronous = NORMAL")
            self.db.execute("PRAGMA case_sensitive_like = ON")
            if os.environ.get("DEBUG_SHOW_SQL_QUERIES"):
                self.db.set_trace_callback(print)

            self._init_storage_table()
            self._init_datasets_tables()
        except RuntimeError:
            raise DQLError("Can't connect to SQLite DB")
        self._table = None

    @property
    def table(self):
        table_name = self.table_name
        if table_name is None:
            return None
        elif self._table is None or self._table.name != table_name:
            self._table = sqlalchemy.table(
                table_name, *[sqlalchemy.column(f) for f in NodeSchema.fields]
            )
        return self._table

    def _init_storage_table(self):
        """Initialize only tables related to storage, e.g s3"""
        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS buckets
            (
                uri         TEXT PRIMARY KEY NOT NULL,
                timestamp   DATETIME,
                expires     DATETIME,
                started_inserting_at  DATETIME,
                last_inserted_at  DATETIME,
                status      INTEGER NOT NULL,
                symlinks    BOOL NOT NULL
            )
        """
        )

    def _init_datasets_tables(self) -> None:
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS datasets
            (
                id              INTEGER PRIMARY KEY,
                name            TEXT NOT NULL UNIQUE,
                description     TEXT,
                labels          JSON DEFAULT('[]'),
                shadow          BOOL NOT NULL,
                status          INTEGER NOT NULL,
                created_at      DATETIME,
                finished_at    DATETIME
            );
            CREATE TABLE IF NOT EXISTS datasets_versions
            (
                id              INTEGER PRIMARY KEY,
                dataset_id      INTEGER NOT NULL,
                version         INTEGER NOT NULL,
                created_at      DATETIME,
                FOREIGN KEY(dataset_id) REFERENCES datasets(id) ON DELETE CASCADE,
                UNIQUE(dataset_id, version)
            );
            """
        )

    def init_db(self, prefix: str = "", is_new: bool = True):
        # Note that an index on the primary key (id) is automatically created
        if not prefix or is_new:
            self.db.executescript(
                f"""
                DROP TABLE IF EXISTS {self.table_name};
                DROP TABLE IF EXISTS {self.table_name}_indexed;
                """
            )
        self.db.executescript(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name}
            (
                id              INTEGER PRIMARY KEY,
                dir_type        INTEGER,
                parent_id       INTEGER,
                name            TEXT NOT NULL,
                checksum        TEXT,
                etag            TEXT,
                version         TEXT,
                is_latest       BOOL,
                last_modified   DATETIME,
                size            BIGINT NOT NULL,
                owner_name      TEXT,
                owner_id        TEXT,
                path_str        TEXT,
                anno            JSON,
                valid           BOOL DEFAULT 1 NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_dir_type_{self.table_name}
            ON {self.table_name} (dir_type);
            CREATE INDEX IF NOT EXISTS idx_parent_id_{self.table_name}
            ON {self.table_name} (parent_id);
            CREATE INDEX IF NOT EXISTS idx_name_{self.table_name}
            ON {self.table_name} (name);
            CREATE INDEX IF NOT EXISTS idx_path_str_{self.table_name}
            ON {self.table_name} (path_str);

            CREATE TABLE IF NOT EXISTS {self.table_name}_indexed
            (
                path_str    TEXT PRIMARY KEY NOT NULL,
                timestamp   DATETIME,
                expires     DATETIME
            );

            CREATE INDEX IF NOT EXISTS idx_path_str_{self.table_name}_indexed
            ON {self.table_name}_indexed (path_str);
        """
        )

    @classmethod
    def _table_name(cls, name, prefix) -> str:
        sha = hashlib.sha256(name.encode("utf-8")).hexdigest()
        return prefix + sha[: cls.TABLE_NAME_SHA_LIMIT]

    @classmethod
    def _listing_table_name(cls, uri) -> str:
        return cls._table_name(uri, cls.LISTING_TABLE_NAME_PREFIX)

    @classmethod
    def _dataset_table_name(cls, dataset_id: int, version=None) -> str:
        name = cls.DATASET_TABLE_PREFIX + str(dataset_id)
        if version:
            name += f"_{version}"
        else:
            name += "_shadow"

        return name

    @property
    def table_name(self) -> Optional[str]:
        if not self.uri:
            return None

        return self._listing_table_name(self.uri)

    def clone(self, uri: Optional[str] = None) -> "SQLiteDataStorage":
        uri = uri or self.uri
        return SQLiteDataStorage(db_file=self.db_file, uri=uri)

    # Query starters
    @property
    def nodes(self):
        def with_path(row, cut):
            path_str = row[PATH_STR_INDEX]
            assert path_str.startswith(cut)
            cut_path = path_str[len(cut) :].lstrip("/") if cut else path_str
            return NodeWithPath(*row, cut_path.split("/"))  # type: ignore [call-arg]

        q = Query(self.db, NodeSchema(), self.table_name, wrap=Node._make)
        q.with_path = lambda cut="": q.wrap(partial(with_path, cut=cut))
        return q

    @property
    def storages(self):
        return Query(self.db, StorageSchema(), wrap=Storage._make)

    @property
    def partials(self):
        assert self.table_name, "Should choose uri/table_name first"
        return Query(self.db, PartialSchema(), f"{self.table_name}_indexed")

    def _get_nodes_by_glob_path_pattern(
        self, path_list: List[str], glob_name: str
    ) -> Iterable[NodeWithPath]:
        """Finds all Nodes that correspond to GLOB like path pattern."""
        node = self._get_node_by_path_list(path_list)
        if not node.is_dir:
            raise RuntimeError(f"Can't resolve name {'/'.join(path_list)}")

        def _with_path(row):
            return NodeWithPath(*row, path_list)  # type: ignore [call-arg]

        q = self.nodes.where(
            valid=True, parent_id=node.id, is_latest=True, name__glob=glob_name
        )
        return q.wrap(_with_path).all()

    def _get_node_by_path_list(self, path_list: List[str]) -> NodeWithPath:
        """
        Gets node that correspond some path list, e.g ["data-lakes", "dogs-and-cats"]
        """
        path_str = "/".join(path_list)
        node = (
            self.nodes.with_path()
            .where(valid=True, path_str=path_str, is_latest=True)
            .order_by("dir_type")
            .get()
        )
        if not node:
            raise FileNotFoundError(f"Unable to resolve path {path_str}")
        return node

    def _populate_nodes_by_path(
        self, path_list: List[str], num: int, res: List[NodeWithPath]
    ) -> None:
        """
        Puts all nodes found by path_list into the res input variable.
        Note that path can have GLOB like pattern matching which means that
        res can have multiple nodes as result.
        If there is no GLOB pattern, res should have one node as result that
        match exact path by path_list
        """
        if num >= len(path_list):
            res.append(self._get_node_by_path_list(path_list))
            return

        curr_name = path_list[num]
        if set(curr_name).intersection(GLOB_CHARS):
            nodes = self._get_nodes_by_glob_path_pattern(path_list[:num], curr_name)
            for node in nodes:
                if not node.is_dir:
                    res.append(node)
                else:
                    path = (
                        path_list[:num]
                        + [node.name or ""]
                        + path_list[num + 1 :]  # type: ignore [attr-defined]
                    )
                    self._populate_nodes_by_path(path, num + 1, res)
        else:
            self._populate_nodes_by_path(path_list, num + 1, res)
            return
        return

    @staticmethod
    def _prepare_node(d: Dict[str, Any]) -> Dict[str, Any]:
        if d.get("dir_type") is None:
            if d.get("is_root"):
                dir_type = DirType.ROOT
            elif d.get("is_dir"):
                dir_type = DirType.DIR
            else:
                dir_type = DirType.FILE
            d["dir_type"] = dir_type

        if not d.get("path_str"):
            if d.get("path"):
                path = d["path"]
                if isinstance(path, list):
                    d["path_str"] = "/".join(path)
                else:
                    d["path_str"] = path
            elif d.get("dir_type") == DirType.ROOT:
                d["path_str"] = ""
            else:
                raise RuntimeError(f"No Path for node data: {d}")

        d = {
            "name": "",
            "is_latest": True,
            "size": 0,
            "valid": True,
            **d,
        }
        return {f: d.get(f) for f in NodeSchema.fields[1:]}

    def get_datasets(
        self, shadow_only: Optional[bool] = None
    ) -> Iterator["DatasetRecord"]:
        if shadow_only is None:
            cond = ""
        elif shadow_only:
            cond = "WHERE datasets.shadow"
        else:
            cond = "WHERE NOT datasets.shadow"

        rows = self.db.execute(
            f"""
            SELECT
                datasets.id,
                datasets.name,
                datasets.description,
                datasets.labels,
                datasets.shadow,
                datasets.status,
                datasets.created_at,
                datasets.finished_at,
                datasets_versions.version
            FROM datasets
            LEFT JOIN datasets_versions ON datasets.id = datasets_versions.dataset_id
            {cond}
            """,
        ).fetchall()

        for _, g in groupby(rows, operator.itemgetter(0)):
            dataset = self._parse_dataset(list(g))
            if dataset:
                yield dataset

    def create_dataset_rows_table(
        self,
        name: str,
        custom_columns: Sequence["sqlalchemy.Column"] = (),
        if_not_exists: bool = True,
    ):
        q = CreateTable(
            dataset_table(name, custom_columns=custom_columns),
            if_not_exists=if_not_exists,
        )
        self.db.execute(*compile_statement(q))

    def get_dataset_row_values(
        self,
        name: str,
        columns: Optional[Sequence[Column]] = None,
        limit=20,
        version=None,
    ) -> Iterable[Mapping[str, Any]]:
        dataset = self.get_dataset(name)
        assert dataset
        dataset_table_name = self._dataset_table_name(dataset.id, version)

        q = select_table(dataset_table_name, columns=columns)
        if limit:
            q = q.limit(limit)

        cur = self.db.cursor()
        cur.row_factory = sqlite3.Row  # type: ignore[assignment]
        yield from cur.execute(*compile_statement(q)).fetchall()

    def get_dataset_rows(
        self, name: str, limit=20, version=None
    ) -> Iterable[DatasetRow]:
        for row in self.get_dataset_row_values(
            name, columns=DATASET_ROW_FIELDS, limit=limit, version=version
        ):
            yield DatasetRow(**row)

    def create_shadow_dataset(
        self, name: str, create_rows: Optional[bool] = True
    ) -> DatasetRecord:
        """Creates new shadow dataset if it doesn't exist yet"""
        with self.db:
            self.db.execute("begin")

            # adds entry into datasets table
            self.db.execute(
                """
                INSERT INTO datasets(name, shadow, status, created_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(name) DO NOTHING
                """,
                [name, True, DatasetStatus.CREATED, datetime.now(timezone.utc)],
            )
            dataset = self.get_dataset(name)
            assert dataset
            assert dataset.shadow

            if create_rows:
                table_name = self._dataset_table_name(dataset.id)
                self.create_dataset_rows_table(table_name)
                dataset = self.update_dataset_status(dataset, DatasetStatus.PENDING)

            return dataset  # type: ignore[return-value]

    def insert_into_shadow_dataset(
        self, name: str, uri: str, path: str, recursive=False
    ) -> None:
        dataset = self.get_dataset(name)
        assert dataset
        assert dataset.shadow

        source_table_name = self._listing_table_name(uri)
        dataset_table_name = self._dataset_table_name(dataset.id)

        self.uri = uri  # needed for parent node and .nodes
        if recursive:
            if not path.endswith("*"):
                path = path.rstrip("/")
                if path:
                    # setting sufix for globs only if path is defined
                    path = path + "/*"  # glob filter must end with /*

            if path:
                nodes = self.nodes.where(valid=True, path_str__glob=path, type="file")
            else:
                # we are getting the whole storage, no need to query by path
                nodes = self.nodes.where(valid=True, type="file")
        else:
            parent = self.get_node_by_path(path.lstrip("/").rstrip("/*"))
            nodes = self.nodes.where(valid=True, parent_id=parent.id, type="file")

        (
            where_sql,
            where_params,
        ) = nodes._compile_where()  # pylint: disable=protected-access
        insert_q = f"""
            INSERT into {dataset_table_name}
            (
                path_str,
                dir_type,
                parent_id,
                name,
                checksum,
                etag,
                version,
                is_latest,
                last_modified,
                size,
                owner_name,
                owner_id,
                anno,
                source
            )
            SELECT
                path_str,
                dir_type,
                parent_id,
                name,
                checksum,
                etag,
                version,
                is_latest,
                last_modified,
                size,
                owner_name,
                owner_id,
                anno,
                ? AS source
            FROM {source_table_name}
            {where_sql}
            """
        self.db.execute(
            insert_q,
            [uri] + where_params,
        )

    def rename_dataset_table(
        self,
        old_name: str,
        new_name: str,
        old_version: Optional[int] = None,
        new_version: Optional[int] = None,
    ) -> None:
        old_dataset = self.get_dataset(old_name)
        new_dataset = self.get_dataset(new_name)
        assert old_dataset
        assert new_dataset

        old_name = self._dataset_table_name(old_dataset.id, old_version)
        new_name = self._dataset_table_name(new_dataset.id, new_version)

        self.db.execute(f"ALTER TABLE {old_name} RENAME TO {new_name}")

    def update_dataset(self, dataset_name: str, **kwargs) -> None:
        args = []
        fields = []
        for field, value in kwargs.items():
            if field in DATASET_FIELDS:
                fields.append(field)
                if field == "labels":
                    args.append(json.dumps(value))
                else:
                    args.append(value)

        if not fields:
            # Nothing to update
            return

        args.append(dataset_name)  # for WHERE part

        set_query = "SET " + ", ".join(f"{field} = ?" for field in fields)
        self.db.execute(f"UPDATE datasets {set_query} WHERE name = ?", args)

    def create_dataset_version(
        self, name: str, version: int, create_rows_table=True
    ) -> DatasetRecord:
        with self.db:
            self.db.execute("begin")

            dataset = self.get_dataset(name)
            assert dataset

            self.db.execute(
                """INSERT INTO datasets_versions(
                    dataset_id, version, created_at
                ) VALUES (?, ?, ?)
                ON CONFLICT(dataset_id, version) DO NOTHING
                """,
                [dataset.id, version, datetime.now(timezone.utc)],
            )

            if create_rows_table:
                table_name = self._dataset_table_name(dataset.id, version)
                self.create_dataset_rows_table(table_name)

            return dataset

    def merge_dataset_rows(
        self,
        src: DatasetRecord,
        dst: DatasetRecord,
        src_version: Optional[int] = None,
        dst_version: Optional[int] = None,
    ) -> None:
        src_table_name = self._dataset_table_name(src.id, src_version)
        dst_table_name = self._dataset_table_name(dst.id, dst_version)
        dst_table_name_latest = self._dataset_table_name(dst.id, dst.latest_version)

        select_fields = ",".join([f for f in DATASET_ROW_FIELDS if f != "id"])
        self.db.execute(
            f"""
            INSERT OR IGNORE INTO {dst_table_name} ({select_fields})
            SELECT {select_fields} FROM {src_table_name}
            UNION SELECT {select_fields} from {dst_table_name_latest}
            """,
        )

    @staticmethod
    def _parse_dataset(rows) -> Optional[DatasetRecord]:
        dataset = None
        for r in rows:
            if not dataset:
                dataset = DatasetRecord.parse(*r)
                continue
            dataset.merge_versions(DatasetRecord.parse(*r))  # type: ignore[unreachable]

        return dataset

    def get_dataset(self, name: str) -> Optional[DatasetRecord]:
        rows = self.db.execute(
            """
            SELECT
                datasets.id,
                datasets.name,
                datasets.description,
                datasets.labels,
                datasets.shadow,
                datasets.status,
                datasets.created_at,
                datasets.finished_at,
                datasets_versions.version
            FROM datasets
            LEFT JOIN datasets_versions ON datasets.id = datasets_versions.dataset_id
            WHERE datasets.name = ?
            """,
            [name],
        ).fetchall()
        if not rows:
            return None

        return self._parse_dataset(rows)

    def remove_dataset_version(self, dataset: DatasetRecord, version: int) -> None:
        if not dataset.has_version(version):
            return

        self.db.execute(
            """
            DELETE FROM datasets_versions WHERE dataset_id = ? and version = ?
            """,
            [dataset.id, version],
        )

        if dataset.versions and len(dataset.versions) == 1:
            # had only one version, fully deleting dataset
            self.db.execute("DELETE FROM datasets WHERE id = ?", [dataset.id])

        dataset.remove_version(version)

        self.db.execute(f"DROP TABLE {self._dataset_table_name(dataset.id, version)}")

    def remove_shadow_dataset(self, dataset: DatasetRecord, drop_rows=True) -> None:
        with self.db:
            self.db.execute("begin")
            self.db.execute("DELETE FROM datasets WHERE id = ?", [dataset.id])
            if drop_rows:
                self.db.execute(f"DROP TABLE {self._dataset_table_name(dataset.id)}")

    @retry_sqlite_locks_async
    async def update_last_inserted_at(self, uri: Optional[str] = None) -> None:
        uri = uri or self.uri
        updates = {"last_inserted_at": datetime.now(timezone.utc)}
        self.storages.where(uri=uri).update(**updates)

    @retry_sqlite_locks_async
    async def insert_entry(self, entry: Dict[str, Any]) -> int:
        return self.nodes.insert(self._prepare_node(entry))

    @retry_sqlite_locks_async
    async def insert_entries(self, entries: List[Dict[str, Any]]) -> None:
        self.nodes.insertmany(map(self._prepare_node, entries))

    async def insert_root(self) -> int:
        return await self.insert_entry({"dir_type": DirType.ROOT})

    def get_nodes_by_parent_id(
        self,
        parent_id: int,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
    ) -> Iterable[Node]:
        """Gets nodes from database by parent_id, with optional filtering"""
        return self.nodes.where(valid=True, parent_id=parent_id, type=type).all()

    def get_storage_all(self) -> Iterator[Storage]:
        return self.storages.all()

    def get_storage(self, uri: str) -> Optional[Storage]:
        return self.storages.where(uri=uri).get()

    @retry_sqlite_locks
    def create_storage_if_not_registered(
        self, uri: str, symlinks: bool = False
    ) -> None:
        self.storages.insert(
            {"uri": uri, "status": StorageStatus.CREATED, "symlinks": symlinks},
            silent=True,
        )

    def find_stale_storages(self):
        """
        Finds all pending storages for which the last inserted node has happened
        before STALE_HOURS_LIMIT hours, and marks it as STALE
        """
        with self.db:
            self.db.execute("begin")
            pending_storages = self.storages.where(status=StorageStatus.PENDING).all()
            for storage in pending_storages:
                if storage.is_stale:
                    print(f"Marking storage {storage.uri} as stale")
                    self.mark_storage_stale(storage)

    def register_storage_for_indexing(
        self,
        uri: str,
        force_update: bool = True,
        prefix: str = "",
    ) -> Tuple[Storage, bool, bool, bool]:
        """
        Prepares storage for indexing operation.
        This method should be called before index operation is started
        It returns:
            - storage, prepared for indexing
            - boolean saying if indexing is needed
            - boolean saying if indexing is currently pending (running)
        """
        # This ensures that all calls to the DB are in a single transaction
        # and commit is automatically called once this function returns
        with self.db:
            self.db.execute("begin")

            # Create storage if it doesn't exist
            self.create_storage_if_not_registered(uri)
            saved_storage = self.get_storage(uri)

            assert (
                saved_storage is not None
            ), f"Unexpected error, storage for {uri} doesn't exist"
            storage: Storage = saved_storage

            if storage.status == StorageStatus.PENDING:
                return storage, False, True, False

            elif storage.is_expired or storage.status == StorageStatus.STALE:
                storage = self.mark_storage_pending(storage)
                return storage, True, False, False

            elif storage.status == StorageStatus.COMPLETE and not force_update:
                return storage, False, False, False

            elif (
                storage.status == StorageStatus.PARTIAL and prefix and not force_update
            ):
                if self.check_partial_index_valid(prefix):
                    return storage, False, False, False
                self.delete_partial_index(prefix)
                return storage, True, False, False

            else:
                is_new = storage.status == StorageStatus.CREATED
                storage = self.mark_storage_pending(storage)
                return storage, True, False, is_new

    def delete_partial_index(self, prefix: str):
        """
        Deletes the provided and any subdir indexed prefixes and nodes
        """
        bare_prefix = prefix.rstrip("/")
        dir_prefix = posixpath.join(prefix, "")
        self.partials.where(path_str__startswith=dir_prefix).delete()
        self.nodes.where(path_str__startswith=dir_prefix).delete()
        self.nodes.where(path_str=bare_prefix).delete()

    def check_partial_index_valid(self, prefix: str):
        # This SQL statement finds all matching path_str entries that are
        # prefixes of the provided prefix, matching this or parent directories
        # that are indexed.
        dir_prefix = posixpath.join(prefix, "")
        expire_values = self.partials.where(path_str__startof=dir_prefix).col("expires")
        return not all(is_expired(expires) for expires in expire_values)

    @retry_sqlite_locks
    def mark_storage_pending(self, storage: Storage) -> Storage:
        # Update status to pending and dates
        updates = {
            "status": StorageStatus.PENDING,
            "timestamp": None,
            "expires": None,
            "last_inserted_at": None,
            "started_inserting_at": datetime.now(timezone.utc),
        }
        storage = storage._replace(**updates)  # type: ignore [arg-type]
        self.storages.where(uri=storage.uri).update(**updates)
        return storage

    @retry_sqlite_locks
    def mark_storage_stale(self, storage: Storage) -> Storage:
        # Update status to pending and dates
        updates = {"status": StorageStatus.STALE, "timestamp": None, "expires": None}
        storage = storage._replace(**updates)  # type: ignore [arg-type]
        self.storages.where(uri=storage.uri).update(**updates)
        return storage

    @retry_sqlite_locks
    def mark_storage_indexed(
        self,
        uri: str,
        status: int,
        ttl: int,
        end_time: Optional[datetime] = None,
        prefix: str = "",
    ) -> None:
        if status == StorageStatus.PARTIAL and not prefix:
            raise AssertionError("Partial indexing requires a prefix")

        if end_time is None:
            end_time = datetime.now(timezone.utc)
        expires = Storage.get_expiration_time(end_time, ttl)

        with self.db:
            self.db.execute("BEGIN")

            self.storages.where(uri=uri).update(
                timestamp=end_time,
                expires=expires,
                status=status,
                last_inserted_at=end_time,
            )

            if not self.table_name:
                # This only occurs in tests
                return

            if status in {StorageStatus.COMPLETE, StorageStatus.FAILED}:
                # Delete remaining partial index paths
                self.partials.delete()
            elif status == StorageStatus.PARTIAL:
                dirprefix = posixpath.join(prefix, "")
                row = {"path_str": dirprefix, "timestamp": end_time, "expires": expires}
                try:
                    self.partials.insert(row)
                # If path_str unique constraint is violated, do an update.
                # Exception type depends on db.
                except Exception:  # pylint: disable=broad-except
                    self.partials.where(path_str=dirprefix).update(
                        timestamp=end_time, expires=expires
                    )

    @retry_sqlite_locks
    def update_dataset_status(
        self, dataset: DatasetRecord, status: int
    ) -> DatasetRecord:
        update_data: Dict[str, Any] = {"status": status}
        if status in [DatasetStatus.COMPLETE, DatasetStatus.FAILED]:
            # if in final state, updating finished_at datetime
            update_data["finished_at"] = datetime.now(timezone.utc)

        self.update_dataset(dataset.name, **update_data)
        dataset.update(**update_data)
        return dataset

    def validate_paths(self) -> int:
        assert isinstance(self.table_name, str), "table_name must be a string"
        t1 = self.table.alias("t1")
        t2 = self.table.alias("t2")
        t3 = self.table.alias("t3")
        id_query = (
            select(t2.c.id)  # type: ignore[attr-defined]
            .select_from(t2)
            .join(t3, (t2.c.path_str == t3.c.path_str) & (t2.c.id != t3.c.id))
            .where(
                t2.c.valid == True,  # noqa: E712 pylint:disable=singleton-comparison
                t2.c.dir_type == 0,
            )
        )
        query = (
            update(t1)
            .values(valid=False)
            .where(t1.c.id.in_(id_query))  # type: ignore[attr-defined]
        )

        row_count = self.db.execute(*compile_statement(query)).rowcount
        if row_count:
            logger.warning(
                "File names that collide with directory names will be ignored. "
                f"Number found: {row_count}"
            )
        return row_count

    def get_node_by_path(self, path: str) -> NodeWithPath:
        conds: Dict[str, Any] = {"path_str": path.strip("/")}
        if path.endswith("/"):
            conds["dir_type__ne"] = DirType.FILE
        node = self.nodes.with_path().where(valid=True, **conds).get()
        if not node:
            raise FileNotFoundError(f"Unable to resolve path {path}")
        return node

    def expand_path(self, path: str) -> List[NodeWithPath]:
        """Simulates Unix-like shell expansion"""
        clean_path = path.strip("/")
        path_list = clean_path.split("/") if clean_path != "" else []

        res: List[NodeWithPath] = []
        self._populate_nodes_by_path(path_list, 0, res)
        return res

    def get_latest_files_by_parent_node(self, parent_node: Node) -> Iterable[Node]:
        if not parent_node.is_dir:
            return [parent_node]

        return self.nodes.where(
            valid=True, parent_id=parent_node.id, is_latest=True
        ).all()

    def size(self, node: Node) -> Tuple[int, int]:
        if not node.is_dir:
            # Return node size if this is not a directory
            return node.size, 1

        sub_glob = posixpath.join(node.path_str, "*")
        size, count = self.nodes.where(
            valid=True, path_str__glob=sub_glob, is_latest=True
        ).get("SUM(size)", "SUM(dir_type = 0)")
        return size or 0, count or 0

    def walk_subtree(
        self,
        node: AnyNode,
        sort: Union[List[str], str, None] = None,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
        _conds: Dict[str, Any] = None,
    ) -> Iterable[NodeWithPath]:
        conds = _conds.copy() if _conds else {}

        if node.path_str:
            sub_glob = posixpath.join(node.path_str, "*")
            conds.setdefault("path_str__glob", []).append(sub_glob)

        conds = dict(
            conds,
            dir_type__ne=DirType.ROOT,
            is_latest=True,
        )
        if type is not None:
            conds["type"] = type

        q = self.nodes.with_path(cut=node.path_str).where(valid=True, **conds)
        if sort:
            q = q.order_by(sort)
        return q.all()

    def find(self, node: AnyNode, jmespath="", **conds) -> Iterable[NodeWithPath]:
        if jmespath:
            raise NotImplementedError("jmespath queries not supported!")
        return self.walk_subtree(node, _conds=conds)

    @retry_sqlite_locks
    def update_annotation(self, node: Node, annotation_content: str) -> None:
        # TODO: This will likely need to be updated for annotation support
        img_exts = ["jpg", "jpeg", "png"]
        names = [node.name_no_ext + "." + ext for ext in img_exts]

        res = self.nodes.where(
            valid=True,
            parent_id=node.parent_id,
            type="file",
            is_latest=True,
            name__ieq=names,
        )

        if res is None or len(res) == 0:
            msg = f"no image file was found for annotation {node.name}"
            logger.warning(msg)
        elif res[0][0] > 1:
            msg = (
                f"multiple image files were updated for a single "
                f"annotation {node.name}"
            )
            logger.warning(msg)

    @retry_sqlite_locks
    def update_checksum(self, node: Node, checksum: str) -> None:
        self.nodes.where(id=node.id).update(checksum=checksum)
