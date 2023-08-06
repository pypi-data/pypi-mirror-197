from sqlalchemy import Integer

from dql.query import C, asUDF


def test_udf():
    @asUDF(Integer, C.a, C.b)
    def udf(a, b):
        return a * b

    row = {"a": 6, "b": 7}  # sqlalchemy.Row acts as a dict
    result = udf(row)  # pylint: disable=no-value-for-parameter
    assert result == 42
