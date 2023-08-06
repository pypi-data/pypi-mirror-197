from datetime import timedelta
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, validator


class DeidentifierBase(BaseModel):
    ...


class Redact(DeidentifierBase):
    type: Literal["redact"]
    value: None = None


class Mask(DeidentifierBase):
    type: Literal["mask"]
    value: str


class Replace(DeidentifierBase):
    type: Literal["replace"]
    value: str


class ColumnRetention(BaseModel):
    name: str
    deidentifier: Union[Redact, Mask, Replace] = Field(..., discriminator="type")
    period: timedelta
    description: Optional[str] = None


class TableCatalogue(BaseModel):
    name: str
    columns: List[ColumnRetention]
    datetime_column: str


class StoreCatalogue(BaseModel):
    name: str
    tables: Dict[str, TableCatalogue]

    @validator("tables", pre=True, always=True)
    def add_table_name(cls, value):
        """This will add the table name to the table info"""
        for name, table_info in value.items():
            table_info["name"] = name
        return value


class Catalogue(BaseModel):
    stores: List[StoreCatalogue]
