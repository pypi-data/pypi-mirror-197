import pytest
from sqlalchemy import Integer

from dql.query import C, DatasetQuery, asUDF


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_filter(cloud_test_catalog):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    sources = [str(cloud_test_catalog.src)]
    globs = [s.rstrip("/") + "/*" for s in sources]
    catalog.index(sources, client_config=conf)
    catalog.create_shadow_dataset("animals", globs, client_config=conf, recursive=True)
    q = (
        DatasetQuery(name="animals", catalog=catalog)
        .filter(C.size < 13)
        .filter(C.path_str.glob("cats/*") | (C.size < 4))
    )
    result = q.results()
    assert len(result) == 3


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_save_to_table(cloud_test_catalog):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    sources = [str(cloud_test_catalog.src)]
    globs = [s.rstrip("/") + "/*" for s in sources]
    catalog.index(sources, client_config=conf)
    catalog.create_shadow_dataset("animals", globs, client_config=conf, recursive=True)
    q = (
        DatasetQuery(name="animals", catalog=catalog)
        .filter(C.size < 13)
        .filter(C.path_str.glob("cats/*") | (C.size < 4))
    )
    q.save("animals_cats")

    new_query = DatasetQuery(name="animals_cats", catalog=catalog)
    result = new_query.results()
    assert len(result) == 3


@pytest.mark.parametrize(
    "cloud_type,version_aware",
    [("s3", True)],
    indirect=True,
)
def test_udf(cloud_test_catalog):
    catalog = cloud_test_catalog.catalog
    conf = cloud_test_catalog.client_config
    sources = [str(cloud_test_catalog.src)]
    globs = [s.rstrip("/") + "/*" for s in sources]
    catalog.index(sources, client_config=conf)
    catalog.create_shadow_dataset("animals", globs, client_config=conf, recursive=True)

    @asUDF(Integer, C.name)
    def udf(name):
        # A very simple udf.
        return len(name)

    q = (
        DatasetQuery(name="animals", catalog=catalog)
        .filter(C.size < 13)
        .filter(C.path_str.glob("cats/*") | (C.size < 4))
        .add_signal("name_len", udf)
    )
    result = q.results()

    assert len(result) == 3
