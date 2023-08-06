import string
from sqlite3 import Connection, Cursor, connect
from typing import Any, Dict, List, Optional, Tuple

from blackline.adapters.sql import SQLAdapter
from blackline.models.sqlite import SQLiteConfig


class SQLiteAdapter(SQLAdapter):
    config_model = SQLiteConfig

    def __init__(self, config: SQLiteConfig.Config, *args, **kwargs):
        super().__init__(config=config, *args, **kwargs)

    def connection(self) -> Connection:
        return connect(**self.config.connection.dict())

    def execute(self, sql: str, values: Optional[Dict[str, Any]] = None) -> Any:
        with self.connection() as conn:
            return conn.execute(sql, values or ())

    def fetchall(self, results: Cursor) -> List[Tuple]:
        return results.fetchall()

    def update_template(self) -> str:
        return "UPDATE {{ table }}"

    def set_template(self) -> str:
        return "SET"

    def redact_template(self) -> str:
        return "{{ name }} = null"

    def replace_template(self) -> str:
        return "{{ name }} = :{{ value }}"

    def mask_template(self) -> str:
        """Mask template for SQLite.

        SQLite does not support regex, so we have to use a nested replace
        function to mask digits in a column. We are limited to digits because
        if we mask mask characters will will run into an OperationalError: parser
        stack overflow

        Returns:
            str: Mask template for SQLite.
        """

        replace_str = "{{ name }}"
        for c in string.digits:
            replace_str = f"REPLACE({replace_str}, '{c}', :{{{{ value }}}})"

        return f"{{{{ name }}}} = {replace_str}"

    def where_template(self) -> str:
        return "WHERE {{ datetime_column }} < :cutoff"

    def columns(self, name: str) -> List[Tuple[str, str]]:
        """
        Return a list of columns for a given table.

        Args:
            name (str): Table name.

        Returns:
            List[Tuple[str, str]]: A list of (column name, type) tuple pairs.
        """
        results = self.connection().execute(f"PRAGMA table_info({name})").fetchall()
        return [(column[1], column[2]) for column in results]

    def test_connection(self) -> bool:
        try:
            with self.connection() as conn:
                conn.execute("SELECT 1")
                return True
        except Exception:
            return False
