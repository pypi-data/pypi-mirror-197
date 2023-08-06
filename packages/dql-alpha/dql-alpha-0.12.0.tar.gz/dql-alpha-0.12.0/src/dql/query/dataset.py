import random
import string
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

import sqlalchemy
from sqlalchemy import sql

from dql.catalog import Catalog
from dql.data_storage.sqlite import SQLiteDataStorage, compile_statement
from dql.dataset import core_dataset_columns
from dql.query.schema import create_udf_table

if TYPE_CHECKING:
    from sqlalchemy.sql.base import Executable

    from dql.query.udf import UDF


class Step(ABC):
    """A query processing step (filtering, mutation, etc.)"""

    @abstractmethod
    def apply(self, query: "Executable", conn) -> "Executable":
        """Apply the processing step."""


class UDFSignal(Step):
    """Add a custom column to the result set."""

    def __init__(self, name: str, udf: "UDF"):
        self.name = name
        self.udf = udf

    def clone(self):
        return self.__class__(self.name, self.udf)

    def apply(self, query, conn):
        temp_table_name = f"udf_{self.name}"
        col = sqlalchemy.Column(self.name, self.udf.output_type, nullable=True)
        tbl = create_udf_table(
            conn,
            temp_table_name,
            [col],
        )
        selected_columns = [c.name for c in query.selected_columns]
        results = conn.execute(*compile_statement(query))
        for row in results:
            cols = {c: v for c, v in zip(selected_columns, row)}
            signal = {self.name: self.udf(cols)}
            update = tbl.insert().values(id=cols["id"], **signal)
            conn.execute(*compile_statement(update))

        # Construct a new query that will join the udf-generated partial table.
        subq = query.subquery()
        return (
            sqlalchemy.select(subq.c)
            .select_from(subq)
            .join(tbl, tbl.c.id == subq.c.id)
            .add_columns(col)
        )


class SQLFilter(Step):
    def __init__(self, *args):  # pylint: disable=super-init-not-called
        self.expressions = args

    def __and__(self, other):
        return self.__class__(*(self.expressions + other))

    def clone(self):
        return self.__class__(*self.expressions)

    def apply(self, query, conn):
        return query.filter(*self.expressions)


class SQLQuery:
    def __init__(
        self, table: str = "", engine=None
    ):  # pylint: disable=super-init-not-called
        self.engine = engine
        self.steps: List["Step"] = []
        self.table = table

    def __iter__(self):
        return iter(self.results())

    def __base_query(self, engine):
        """Return the query for the table the query refers to."""
        tbl = sqlalchemy.Table(self.table, sqlalchemy.MetaData(), autoload_with=engine)
        return sqlalchemy.select(tbl)

    def apply_steps(self):
        """
        Apply the steps in the query and return the resulting
        sqlalchemy.Executable.
        """
        engine = self.engine
        query = self.__base_query(engine)
        with engine.connect() as connection:
            # use the sqlite3 dbapi directly for consistency with
            # SQLiteDataStorage, until we can use sqlalchemy
            # connections for everything
            conn = connection.connection.driver_connection
            for step in self.steps:
                query = step.apply(query, conn)  # a chain of steps linked by results
        return query

    def results(self):
        engine = self.engine
        query = self.apply_steps()
        with engine.connect() as connection:
            conn = connection.connection.driver_connection
            result = conn.execute(*compile_statement(query)).fetchall()
        return result

    def clone(self):
        obj = self.__class__()
        obj.engine = self.engine
        obj.table = self.table
        obj.steps = self.steps.copy()
        return obj

    def filter(self, *args):
        query = self.clone()
        steps = query.steps
        if steps and isinstance(steps[-1], SQLFilter):
            steps[-1] = steps[-1] & args
        else:
            steps.append(SQLFilter(*args))
        return query


class DatasetQuery(SQLQuery):
    def __init__(self, path: str = "", name: str = "", catalog=None):
        if catalog is None:
            catalog = Catalog(SQLiteDataStorage())
        self.catalog = catalog

        data_storage = catalog.data_storage
        table = ""
        if path:
            # TODO add indexing step
            raise NotImplementedError("path not supported")
        elif name:
            if catalog is None:
                raise ValueError("using name requires catalog")
            table = data_storage._dataset_table_name(data_storage.get_dataset(name).id)
        super().__init__(table=table, engine=data_storage.engine)

    def clone(self):
        obj = self.__class__(catalog=self.catalog)
        obj.engine = self.engine
        obj.table = self.table
        obj.steps = self.steps.copy()
        return obj

    def add_signal(self, name: str, udf: "UDF"):
        query = self.clone()
        steps = query.steps
        steps.append(UDFSignal(name, udf))
        return query

    def save(self, name: str):
        """Save the query as a shadow dataset."""

        engine = self.engine
        query = self.apply_steps()

        # Save to a temporary table first.
        temp_tbl = f"tmp_{name}_" + _random_string(6)
        columns: List["sqlalchemy.Column"] = [
            sqlalchemy.Column(col_desc["name"], col_desc["type"])
            for col_desc in query.column_descriptions
            if col_desc["name"] not in CORE_COLUMN_NAMES
        ]
        self.catalog.data_storage.create_dataset_rows_table(
            temp_tbl,
            custom_columns=columns,
            if_not_exists=False,
        )

        with engine.connect() as connection:
            conn = connection.connection.driver_connection
            tbl = sqlalchemy.Table(
                temp_tbl, sqlalchemy.MetaData(), autoload_with=engine
            )
            cols = [col.name for col in tbl.c]
            conn.execute(*compile_statement(tbl.insert().from_select(cols, query)))

        # Create a shadow dataset.
        self.catalog.data_storage.create_shadow_dataset(name, create_rows=False)
        dataset = self.catalog.data_storage.get_dataset(name)
        # pylint: disable=protected-access
        table_name = self.catalog.data_storage._dataset_table_name(dataset.id)
        with self.engine.connect() as connection:
            conn = connection.connection.driver_connection
            conn.execute(
                *compile_statement(
                    sql.text(f"ALTER TABLE {temp_tbl} RENAME TO {table_name}")
                )
            )


def _random_string(length: int) -> str:
    return "".join(
        random.choice(string.ascii_letters + string.digits)  # nosec B311
        for i in range(length)
    )


CORE_COLUMN_NAMES = [col.name for col in core_dataset_columns()]
