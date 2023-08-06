from functools import cached_property
from pathlib import Path
from typing import Optional, Union

import yaml
from blackline.constants import PROJECT_CONFIG_FILE
from blackline.models.project_config import ProjectConfig
from blackline.parsers.base import BaseParser


class ProjectParser(BaseParser):
    model = ProjectConfig

    def __init__(
        self,
        path: Union[str, Path],
        filename: Union[str, Path] = PROJECT_CONFIG_FILE,
    ) -> None:
        self.path = Path(path)
        self.filename = Path(filename)
        self.filepath = Path(path, filename)
        self._config: Optional[ProjectConfig] = None
        super().__init__()

    @property
    def adapters_path(self) -> Path:
        return Path(self.path, self.config().adapters_path)

    @property
    def catalogue_path(self) -> Path:
        return Path(self.path, self.config().catalogue_path)

    def config(self) -> ProjectConfig:
        with open(self.filepath, "rb") as f:
            info = yaml.safe_load(f)
            info["project_root"] = self.filepath.parent
            return self.model.parse_obj(info)

    @cached_property
    def project(self) -> ProjectConfig:
        return self.config()
