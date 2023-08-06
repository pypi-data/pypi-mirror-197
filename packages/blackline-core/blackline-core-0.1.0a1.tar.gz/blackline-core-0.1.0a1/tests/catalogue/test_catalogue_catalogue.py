from pathlib import Path

from blackline.catalogue.catalogue import Catalogue
from blackline.models.catalogue import StoreCatalogue
from blackline.models.project_config import ProjectConfig
from blackline.parsers.catalogue import CatalogueParser


def test__init__(project_config: ProjectConfig) -> None:
    # Setup
    path = Path(project_config.project_root, project_config.catalogue_path)

    # Run & Assert
    catalogue = Catalogue(path=path)
    assert isinstance(catalogue.parser, CatalogueParser)


def test_config(catalogue: Catalogue) -> None:
    # Run & Assert
    stores = catalogue.stores
    assert isinstance(stores, list)
    for store in stores:
        assert isinstance(store, StoreCatalogue)


def test_stores(catalogue: Catalogue) -> None:
    # Run & Assert
    stores = catalogue.stores
    assert isinstance(stores, list)
    for store in stores:
        assert isinstance(store, StoreCatalogue)
