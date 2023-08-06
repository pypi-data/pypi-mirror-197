from datetime import datetime, timedelta
from typing import Dict, List, Optional

from blackline.adapters.base import AdapterBase
from blackline.models.catalogue import ColumnRetention, TableCatalogue
from blackline.query.query import Query
from blackline.query.template import Template


class QueryFactory:
    """Query builder class to build query object."""

    def __init__(
        self,
        adapter: AdapterBase,
        table: TableCatalogue,
        start_date: Optional[datetime] = None,
    ) -> None:
        self.adapter = adapter
        self.table = table
        self.start_date = start_date or datetime.now()
        self.template = Template(self.adapter, trim_blocks=True, lstrip_blocks=True)

    def queries(self) -> List[Query]:
        """Get queries."""
        return [
            self.query_by_period(period=period, columns=columns)
            for period, columns in self.columns_by_period().items()
        ]

    def query_by_period(
        self, period: timedelta, columns: List[ColumnRetention]
    ) -> Query:
        return Query(
            adapter=self.adapter,
            sql=self.render_sql(columns=columns),
            columns=columns,
            cutoff_date=self.cutoff_date(period=period),
        )

    def render_sql(self, columns: List[ColumnRetention]) -> str:
        return self.template.template.render(
            table=self.table.name,
            columns=columns,
            datetime_column=self.table.datetime_column,
        )

    def cutoff_date(self, period: timedelta) -> datetime:
        """Get cutoff date."""
        return self.start_date - period

    def columns_by_period(self) -> Dict[timedelta, List[ColumnRetention]]:
        """Get columns by retention period."""
        columns: Dict[timedelta, List[ColumnRetention]] = {
            column.period: [
                _column
                for _column in self.table.columns
                if column.period == _column.period
            ]
            for column in self.table.columns
        }
        return columns
