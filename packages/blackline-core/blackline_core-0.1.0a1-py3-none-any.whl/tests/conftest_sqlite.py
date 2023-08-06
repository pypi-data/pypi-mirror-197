import datetime
import sqlite3
from sqlite3 import Connection
from typing import List

import pytest
from blackline.adapters.sqlite import SQLiteAdapter
from blackline.parsers.stores import StoresParser


@pytest.fixture
def sqlite_store_name() -> str:
    return "test_sqlite"


@pytest.fixture
def mock_data() -> List:
    return [
        (
            datetime.datetime(2021, 1, 1),
            "Dave",
            "dave@example.com",
            "12345",
            True,
            "127.0.0.1",
        ),
        (
            datetime.datetime(2021, 6, 1),
            "Alison",
            "alison@example.com",
            "23456",
            True,
            "127.0.0.2",
        ),
        (
            datetime.datetime(2022, 3, 1),
            "Chris",
            "chris@example.com",
            "34567",
            False,
            "127.0.0.3",
        ),
        (
            datetime.datetime(2022, 4, 1),
            "Megan",
            "megan@example.com",
            "45678",
            True,
            "127.0.0.4",
        ),
    ]


@pytest.fixture
def deidentified_mock_data() -> List:
    return [
        ("2021-01-01 00:00:00", None, "fake@email.com", "12345", 1, "###.#.#.#"),
        ("2021-06-01 00:00:00", None, "fake@email.com", "23456", 1, "###.#.#.#"),
        ("2022-03-01 00:00:00", "Chris", "chris@example.com", "34567", 0, "###.#.#.#"),
        (
            "2022-04-01 00:00:00",
            "Megan",
            "megan@example.com",
            "45678",
            1,
            "127.0.0.4",
        ),
    ]


@pytest.fixture
def mock_sqlite_store(mock_data: List, test_table: str) -> Connection:
    con = sqlite3.connect(
        "file::memory:?cache=shared",
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        uri=True,
    )
    cur = con.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {test_table}")
    cur.execute(
        f"""CREATE TABLE {test_table}(
            created_at TEXT,
            name TEXT,
            email TEXT,
            postal_code TEXT,
            active BOOLEAN,
            ip TEXT
            )"""
    )

    cur.executemany(f"INSERT INTO {test_table} VALUES (?, ?, ?, ?, ?, ?)", mock_data)
    con.commit()

    yield con

    con.cursor().execute(f"DROP TABLE {test_table}")
    con.close()


@pytest.fixture
def sqlite_adapter(
    stores_parser: StoresParser, mock_sqlite_store: Connection, store_name: str
) -> SQLiteAdapter:
    store = stores_parser.store(name=store_name).profiles["dev"]
    return store.adapter


@pytest.fixture
def sqlite_store_yml() -> str:
    return """
    profiles:
      dev:
        type: sqlite
        config:
          connection:
            database: "file::memory:?cache=shared"
            uri: true
    """
