from datetime import datetime
from pathlib import Path
from sqlite3 import Connection

import pytest
from blackline.adapters.factory import AdapterFactory
from blackline.catalogue.catalogue import Catalogue
from blackline.constants import PROJECT_CONFIG_FILE
from blackline.execution.deidentify import Deidentify
from blackline.models.catalogue import StoreCatalogue
from blackline.models.project_config import ProjectConfig
from blackline.models.store import StoreConfig, StoresConfig
from blackline.parsers.catalogue import CatalogueParser
from blackline.parsers.project import ProjectParser
from blackline.parsers.stores import StoresParser
from blackline.project.project import Project
from blackline.query.query_factory import QueryFactory

pytest_plugins = [
    "tests.conftest_sqlite",
]


@pytest.fixture
def project_root() -> Path:
    return Path(Path(__file__).parent.resolve(), "mock_projects/core")


@pytest.fixture
def fake_project_name() -> str:
    return "fake-project"


@pytest.fixture
def test_table() -> str:
    return "test_table"


@pytest.fixture
def project_config_file() -> Path:
    return Path(PROJECT_CONFIG_FILE)


@pytest.fixture
def profile() -> str:
    return "dev"


@pytest.fixture
def project_parser(project_root: Path, project_config_file: Path) -> ProjectParser:
    return ProjectParser(path=project_root, filename=project_config_file)


@pytest.fixture
def project_config(project_parser: ProjectParser) -> ProjectConfig:
    return project_parser.config()


@pytest.fixture
def stores_parser(project_config: ProjectConfig) -> StoresParser:
    path = Path(project_config.project_root, project_config.adapters_path)
    return StoresParser(path=path)


@pytest.fixture
def catalogue_parser(project_config: ProjectConfig) -> CatalogueParser:
    path = Path(project_config.project_root, project_config.catalogue_path)
    return CatalogueParser(path=path)


@pytest.fixture
def adapter_factory() -> AdapterFactory:
    return AdapterFactory()


@pytest.fixture
def project(project_root: Path, project_config_file: Path) -> Project:
    return Project(path=project_root, filename=project_config_file)


@pytest.fixture
def catalogue(project_config: ProjectConfig) -> Catalogue:
    path = Path(project_config.project_root, project_config.catalogue_path)
    return Catalogue(path=path)


@pytest.fixture
def start_date() -> datetime:
    return datetime(2023, 1, 1)


@pytest.fixture
def stores(
    stores_parser: StoresParser,
    project_config: ProjectConfig,
    profile: str,
    start_date: datetime,
) -> StoresConfig:
    return stores_parser.stores


@pytest.fixture
def store_name() -> str:
    return "core"


@pytest.fixture
def store(
    stores_parser: StoresParser, profile: str, store_name: str, start_date: datetime
) -> StoreConfig:
    return stores_parser.store(name=store_name).profiles[profile]


@pytest.fixture
def store_catalogue(catalogue: Catalogue, store_name: str) -> StoreCatalogue:
    return catalogue.store(name=store_name)


@pytest.fixture
def query_factory(
    catalogue: Catalogue,
    store: StoreConfig,
    store_name: str,
    start_date: datetime,
    mock_sqlite_store: Connection,
    test_table: str,
) -> QueryFactory:
    store_catalogue = [store for store in catalogue.stores if store.name == store_name][
        0
    ]

    return QueryFactory(
        adapter=store.adapter,
        table=store_catalogue.tables[test_table],
        start_date=start_date,
    )


@pytest.fixture
def deidentify(project_root: Path, profile: str, start_date: datetime) -> None:
    return Deidentify(path=project_root, profile=profile, start_date=start_date)
