from ..data import ENTRIES, INVALID_ENTRIES
from ..utils import insert_entries


def test_validate_paths(data_storage):
    src = "s3://bucket1"
    data_storage = data_storage.clone(uri=src)
    data_storage.init_db(src, True)
    insert_entries(data_storage, ENTRIES + INVALID_ENTRIES)

    before_count = len(data_storage.nodes.where(valid=True).all())
    data_storage.validate_paths()
    after_count = len(data_storage.nodes.where(valid=True).all())

    assert before_count == 14
    assert after_count == 11
