from datetime import datetime
from typing import Any, Dict, List, Union

from blackline.adapters.base import AdapterBase
from blackline.models.catalogue import ColumnRetention


class Query:
    def __init__(
        self,
        adapter: AdapterBase,
        sql: str,
        columns: List[ColumnRetention],
        cutoff_date: datetime,
    ) -> None:
        self.adapter = adapter
        self.sql = sql
        self.columns = columns
        self.cutoff_date = cutoff_date

    def __str__(self) -> str:
        return f"{self.sql}"

    def execute(self) -> Any:
        values: Dict[str, Union[str, None]] = {
            f"{column.name}_value": column.deidentifier.value for column in self.columns
        }
        values["cutoff"] = self.cutoff_date.strftime(self.adapter.date_format)
        return self.adapter.execute(self.sql, values)
