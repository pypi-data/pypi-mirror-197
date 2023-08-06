from pathlib import Path

from blackline.constants import PROJECT_CONFIG_FILE
from blackline.parsers.catalogue import CatalogueParser
from blackline.parsers.project import ProjectParser
from blackline.parsers.stores import StoresParser


def create_report(path: Path, filename: str = PROJECT_CONFIG_FILE):
    project = ProjectParser(path=path, filename=filename).project
    stores = StoresParser(
        path=Path(project.project_root, project.adapters_path)
    ).stores.stores
    catalogue = CatalogueParser(
        path=Path(project.project_root, project.catalogue_path)
    ).catalogue
    return project, stores, catalogue
