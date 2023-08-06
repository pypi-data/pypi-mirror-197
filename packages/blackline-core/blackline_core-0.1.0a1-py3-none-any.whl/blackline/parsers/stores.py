from functools import cached_property
from pathlib import Path
from typing import Generator, List

import yaml
from blackline.models.store import StoreConfig, StoresConfig
from blackline.parsers.base import BaseParser


class StoresParser(BaseParser):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path
        self._stores: List[StoreConfig] = []

    @cached_property
    def stores(self) -> StoresConfig:
        return StoresConfig(stores=self.config)

    @cached_property
    def config(self) -> List[StoreConfig]:
        files = self.config_files(folderpath=self.path)
        return self._parse_raw_yml(files)

    def _parse_raw_yml(self, files: Generator[Path, None, None]) -> List[StoreConfig]:
        for filepath in files:
            with open(filepath, "rb") as f:
                adapter_info = yaml.safe_load(f)
                adapter_info["name"] = filepath.stem
                _store = StoreConfig.parse_obj(adapter_info)
            self._stores.append(_store)
        return self._stores

    def store(self, name: str) -> StoreConfig:
        for store in self.stores.stores:
            if store.name == name:
                return store
        raise ValueError(f"Store {name} not found")
