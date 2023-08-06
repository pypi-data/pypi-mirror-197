from pathlib import Path

from pydantic import BaseModel, Field


class ProjectConfig(BaseModel):
    name: str
    config_version: int = Field(alias="config-version")
    version: str
    default_profile: str = Field(alias="default-profile")
    catalogue_path: Path = Field(alias="catalogue-path")
    adapters_path: Path = Field(alias="adapters-path")
    project_root: Path

    class Config:
        allow_population_by_field_name = True
