from blackline.adapters.sqlite import SQLiteAdapter
from blackline.models.adapter import AdapterConfig
from blackline.models.project_config import ProjectConfig
from blackline.models.store import StoreConfig
from blackline.parsers.stores import StoresParser


def test__init__(project_config: ProjectConfig) -> None:
    adapter_parser = StoresParser(path=project_config.adapters_path)
    assert adapter_parser.path == project_config.adapters_path


def test_config(stores_parser: StoresParser, profile: str, store_name: str) -> None:

    # Run
    stores = stores_parser.stores

    # Assert
    store = [store for store in stores.stores if store.name == store_name][0]

    assert isinstance(store, StoreConfig)
    assert isinstance(store.profiles[profile], AdapterConfig)
    assert isinstance(store.profiles[profile].adapter, SQLiteAdapter)
    assert (
        store.profiles[profile].config.connection.database
        == "file::memory:?cache=shared"
    )
