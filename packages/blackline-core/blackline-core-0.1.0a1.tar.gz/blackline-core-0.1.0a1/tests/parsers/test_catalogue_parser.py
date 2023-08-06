from pathlib import Path

from blackline.models.catalogue import (
    ColumnRetention,
    Mask,
    Redact,
    Replace,
    StoreCatalogue,
    TableCatalogue,
)
from blackline.models.project_config import ProjectConfig
from blackline.parsers.catalogue import CatalogueParser


def test__init__(project_config: ProjectConfig) -> None:
    path = Path(project_config.project_root, project_config.catalogue_path)
    parser = CatalogueParser(path=path)
    assert parser.path == path


def test_config(catalogue_parser: CatalogueParser, test_table: str) -> None:
    config = catalogue_parser.config()
    assert isinstance(config[0], StoreCatalogue)
    assert isinstance(config[0].tables[test_table], TableCatalogue)
    assert isinstance(config[0].tables[test_table].columns[0], ColumnRetention)
    assert config[0].name == "core"
    assert len(config[0].tables) == 1
    assert len(config[0].tables[test_table].columns) == 3
    assert isinstance(config[0].tables[test_table].columns[0].deidentifier, Redact)
    assert isinstance(config[0].tables[test_table].columns[1].deidentifier, Replace)
    assert isinstance(config[0].tables[test_table].columns[2].deidentifier, Mask)
