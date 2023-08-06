from functools import cached_property
from pathlib import Path
from typing import Generator, List

import yaml
from blackline.models.catalogue import Catalogue, StoreCatalogue
from blackline.parsers.base import BaseParser


class CatalogueParser(BaseParser):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path

    def _parse_store_catalogues(
        self, files: Generator[Path, None, None]
    ) -> List[StoreCatalogue]:
        return [self._parse_yml(path=path) for path in files]

    def _store_name(self, path: Path) -> str:
        return str(path.parent.parts[-1])

    def _parse_yml(self, path: Path) -> StoreCatalogue:
        with open(path, "rb") as f:
            info = yaml.safe_load(f)
            info = {"name": self._store_name(path=path), "tables": info}
            return StoreCatalogue.parse_obj(info)

    def config(self) -> List[StoreCatalogue]:
        return self.catalogue.stores

    def stores(self) -> List[StoreCatalogue]:
        return self.config()

    @cached_property
    def catalogue(self) -> Catalogue:
        files = self.config_files(folderpath=self.path)
        stores = self._parse_store_catalogues(files=files)
        return Catalogue(stores=stores)
