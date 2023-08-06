from typing import Any, Dict, Optional

from blackline.adapters.base import AdapterBase


class SQLAdapter(AdapterBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, sql: str, values: Optional[Dict[str, Any]] = None) -> Any:
        with self.connection() as conn:
            with conn.cursor() as cur:
                return cur.execute(sql, values)

    def update_template(self) -> str:
        return "UPDATE {{ table }}"

    def set_template(self) -> str:
        return "SET"

    def redact_template(self) -> str:
        return "{{ name }} = null"

    def replace_template(self) -> str:
        return "{{ name }} = %({{ value }})s"

    def where_template(self) -> str:
        return "WHERE {{ datetime_column }} < %(cutoff)s"
