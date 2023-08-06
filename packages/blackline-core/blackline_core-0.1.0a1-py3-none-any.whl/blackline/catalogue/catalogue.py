from functools import cached_property
from pathlib import Path
from typing import List

from blackline.models.catalogue import StoreCatalogue
from blackline.parsers.catalogue import CatalogueParser


class Catalogue:
    def __init__(self, path: Path) -> None:
        self.parser = CatalogueParser(path=path)

    @cached_property
    def stores(self) -> List[StoreCatalogue]:
        return self.parser.stores()

    def store(self, name: str) -> StoreCatalogue:
        return [store for store in self.stores if store.name == name][0]
