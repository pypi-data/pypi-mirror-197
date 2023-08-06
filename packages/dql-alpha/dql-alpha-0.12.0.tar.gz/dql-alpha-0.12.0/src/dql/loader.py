from typing import List

from dql.catalog import Catalog
from dql.dataset import DatasetRow


class DataLoader:
    def __init__(
        self,
        contents: List[DatasetRow],
        reader,
        transform,
        catalog: Catalog,
        client_config,
    ):
        self.contents = contents
        self.reader = reader
        self.transform = transform
        self.catalog = catalog
        self.client_config = client_config

    @classmethod
    def from_dataset(cls, name: str, reader, transform, *, catalog=None, client_config):
        contents = list(catalog.ls_dataset_rows(name))
        return cls(contents, reader, transform, catalog, client_config)

    def __len__(self):
        return len(self.contents)

    def __getitem__(self, i):
        row = self.contents[i]
        sample = self.catalog.read_object(row, self.reader, **self.client_config)
        return self.transform(row, sample)
