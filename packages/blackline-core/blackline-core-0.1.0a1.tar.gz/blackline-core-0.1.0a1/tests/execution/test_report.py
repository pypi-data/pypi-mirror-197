from pathlib import Path

from blackline.execution.report import create_report
from blackline.models.catalogue import Catalogue
from blackline.models.project_config import ProjectConfig
from blackline.models.store import StoreConfig


def test_create_report(project_root: Path):
    # Run
    project, stores, catalogue = create_report(path=project_root)

    # Assert
    assert isinstance(project, ProjectConfig)
    for store in stores:
        assert isinstance(store, StoreConfig)
    assert isinstance(catalogue, Catalogue)
