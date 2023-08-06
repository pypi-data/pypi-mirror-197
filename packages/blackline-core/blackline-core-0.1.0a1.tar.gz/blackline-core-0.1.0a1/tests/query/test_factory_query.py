from datetime import timedelta

from blackline.catalogue.catalogue import Catalogue
from blackline.models.catalogue import ColumnRetention
from blackline.models.store import StoreConfig
from blackline.query.query import Query
from blackline.query.query_factory import QueryFactory


def test__init__(
    catalogue: Catalogue, store: StoreConfig, test_table: str, store_name: str
) -> None:
    """Test init method."""
    # Setup
    store_catalogue = [store for store in catalogue.stores if store.name == store_name][
        0
    ]
    table = store_catalogue.tables[test_table]

    # Run
    factory = QueryFactory(adapter=store.adapter, table=table)

    # Assert
    assert isinstance(factory, QueryFactory)
    assert factory.adapter == store.adapter
    assert factory.table == table


def test_queries(query_factory: QueryFactory) -> None:
    """Test query construction."""

    sql_0 = """UPDATE test_table\nSET\n  name = null,\n  email = :email_value\nWHERE created_at < :cutoff"""  # noqa E501
    sql_1 = """UPDATE test_table\nSET\n  ip = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(ip, '0', :ip_value), '1', :ip_value), '2', :ip_value), '3', :ip_value), '4', :ip_value), '5', :ip_value), '6', :ip_value), '7', :ip_value), '8', :ip_value), '9', :ip_value)\nWHERE created_at < :cutoff"""  # noqa E501

    # Run
    queries = query_factory.queries()

    # Assert
    assert len(queries) == len(query_factory.columns_by_period())
    assert queries[0].sql == sql_0
    assert queries[1].sql == sql_1
    for query in queries:
        assert isinstance(query, Query)
        assert query.adapter == query_factory.adapter


def test_columns_by_period(query_factory: QueryFactory) -> None:
    """Test columns by retention period method."""
    # Run
    columns = query_factory.columns_by_period()

    # Assert
    assert isinstance(columns, dict)
    assert len(columns) == 2
    for key, value in columns.items():
        assert isinstance(key, timedelta)
        assert isinstance(value, list)
        for column in value:
            assert isinstance(column, ColumnRetention)
