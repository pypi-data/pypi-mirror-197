from abc import ABC, abstractmethod
from functools import cached_property
from pathlib import Path
from typing import Any, Generator

import yaml


class BaseParser(ABC):
    def __init__(self) -> None:
        pass

    def parse(self, filepath: Path, model) -> Any:
        with open(filepath, "rb") as f:
            return model.parse_obj(yaml.safe_load(f))

    def config_files(self, folderpath: Path) -> Generator[Path, None, None]:
        return folderpath.glob("**/*.yml")

    @abstractmethod
    @cached_property
    def config(self) -> Any:
        raise NotImplementedError
