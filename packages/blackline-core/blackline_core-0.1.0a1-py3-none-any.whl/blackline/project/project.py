from pathlib import Path

from blackline.constants import PROJECT_CONFIG_FILE
from blackline.models.project_config import ProjectConfig
from blackline.parsers.project import ProjectParser


class Project:
    def __init__(self, path: Path, filename: str = PROJECT_CONFIG_FILE) -> None:
        self.parser = ProjectParser(path=path, filename=filename)

    @property
    def adapters_path(self) -> Path:
        return self.parser.adapters_path

    @property
    def catalogue_path(self) -> Path:
        return self.parser.catalogue_path

    def config(self) -> ProjectConfig:
        return self.parser.config()
