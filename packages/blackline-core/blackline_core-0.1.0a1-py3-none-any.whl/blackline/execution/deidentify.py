from datetime import datetime
from pathlib import Path

from blackline.catalogue.catalogue import Catalogue
from blackline.parsers.stores import StoresParser
from blackline.project.project import Project


class Deidentify:
    """Deidentify class to orchestrate deidentification process."""

    def __init__(self, path: Path, profile: str, start_date: datetime) -> None:
        self.profile = profile
        self.start_date = start_date
        self.project = Project(path=path)
        self.stores = StoresParser(path=self.project.adapters_path).stores
        self.catalogue = Catalogue(path=self.project.catalogue_path)

    def deidentify(self) -> None:
        """Run method to orchestrate deidentification process."""
        for catalogue_store in self.catalogue.stores:
            store = self.stores.store(name=catalogue_store.name, profile=self.profile)
            store.deidentify(catalogue=catalogue_store, start_date=self.start_date)


def deidentify(path: Path, profile: str, start_date: datetime) -> None:
    """Run method to orchestrate deidentification process."""
    deidentify = Deidentify(path=path, profile=profile, start_date=start_date)
    deidentify.deidentify()
