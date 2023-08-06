import pytest
from blackline.models.sqlite import SQLiteConfig
from blackline.models.store import StoreConfig, StoresConfig
from yaml import safe_load


def test_StoreConfig(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    info["name"] = "foo"
    config = StoreConfig.parse_obj(info)
    assert config.name == "foo"
    assert isinstance(config.profiles[profile], SQLiteConfig)


def test_StoresConfig(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    info["name"] = "foo"
    config = StoreConfig.parse_obj(info)
    stores = StoresConfig(stores=[config])
    for store in stores.stores:
        assert isinstance(store, StoreConfig)


def test_StoresConfig_store_with_profile(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    info["name"] = "foo"
    config = StoreConfig.parse_obj(info)
    stores = StoresConfig(stores=[config])
    store = stores.store(name="foo", profile=profile)
    assert isinstance(store, SQLiteConfig)


def test_StoresConfig_store_no_profile(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    info["name"] = "foo"
    config = StoreConfig.parse_obj(info)
    stores = StoresConfig(stores=[config])
    store = stores.store(name="foo")
    assert isinstance(store, dict)


def test_StoresConfig_store_not_found(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    info["name"] = "foo"
    config = StoreConfig.parse_obj(info)
    stores = StoresConfig(stores=[config])
    with pytest.raises(ValueError) as excinfo:
        stores.store(name="bar")
        assert "Store bar not found" in str(excinfo.value)
