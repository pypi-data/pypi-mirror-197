from datetime import datetime
from typing import Any, List

from blackline.adapters.factory import AdapterFactory
from blackline.query.query import Query
from blackline.query.query_factory import QueryFactory
from pydantic import BaseModel, root_validator, validator


class ConnectionConfig(BaseModel):
    ...


class AdapterConfig(BaseModel):
    type: str
    adapter: Any = None

    @validator("adapter", pre=True, always=True)
    def load_adapter_cls(cls, value, values):
        return AdapterFactory.load_adapter(name=values["type"])

    @root_validator
    def initialize_adapter(cls, values):
        values["adapter"] = values["adapter"](values["config"])
        return values

    def deidentify(self, catalogue, start_date: datetime = datetime.now()):
        for table in catalogue.tables.values():
            queries = QueryFactory(
                adapter=self.adapter,
                table=table,
                start_date=start_date,
            ).queries()
            self.execute_queries(queries=queries)

    def execute_queries(self, queries: List[Query]) -> None:
        for query in queries:
            query.execute()
