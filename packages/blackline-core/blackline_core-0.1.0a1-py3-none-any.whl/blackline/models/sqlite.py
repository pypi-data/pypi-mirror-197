from typing import Literal

from blackline.models.adapter import AdapterConfig, ConnectionConfig
from pydantic import BaseModel


class SQLiteConnectionConfig(ConnectionConfig):
    database: str
    uri: bool = False


class SQLiteConfig(AdapterConfig):
    class Config(BaseModel):
        connection: SQLiteConnectionConfig

    type: Literal["sqlite"]
    config: Config
