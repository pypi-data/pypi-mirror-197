from sqlite3 import Connection
from typing import List

from blackline.adapters.sqlite import SQLiteAdapter
from blackline.parsers.stores import StoresParser


def test_sqlite_adapter_init(
    stores_parser: StoresParser, profile: str, store_name: str
) -> None:
    # Setup
    store = stores_parser.store(name=store_name).profiles[profile]

    # Run
    SQLiteAdapter(config=store.config)

    # Assert
    assert True


def test_connection(sqlite_adapter: SQLiteAdapter) -> None:
    # Run
    conn = sqlite_adapter.connection()

    # Assert
    assert isinstance(conn, Connection)


def test_test_connection(sqlite_adapter: SQLiteAdapter) -> None:

    # Run & Assert
    assert sqlite_adapter.test_connection()


def test_execute(sqlite_adapter: SQLiteAdapter, mock_data: List) -> None:
    # Run
    res = sqlite_adapter.execute(sql="SELECT * FROM test_table")
    data = res.fetchall()

    # Assert
    assert len(data) == len(mock_data)
