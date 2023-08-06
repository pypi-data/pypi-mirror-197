import inspect
from importlib import import_module
from typing import Annotated, Any, Dict, List, Optional, Type, Union

from blackline.models.adapter import AdapterConfig
from blackline.models.sqlite import SQLiteConfig
from pydantic import BaseModel, Field


def load_adapter_configs_from_submodules() -> set:
    mod = import_module("blackline.models")
    adapter_configs = {SQLiteConfig}
    model_modules = inspect.getmembers(mod, lambda member: inspect.ismodule(member))
    for module in model_modules:
        members = inspect.getmembers(
            module[1],
            lambda member: inspect.isclass(member)
            and issubclass(member, AdapterConfig)
            and member != AdapterConfig,  # Exclused the base class
        )
        adapter_configs.update({member[1] for member in members})
    adapter_configs.update({member[1] for member in members})
    return adapter_configs


def assign_store(
    adapter_configs: set,
) -> Union[Type[AdapterConfig], Type[object]]:
    if len(adapter_configs) == 1:
        return SQLiteConfig
    return Annotated[
        Union[tuple(adapter_configs)],  # type: ignore
        Field(discriminator="type"),
    ]


adapter_configs = load_adapter_configs_from_submodules()
Store: Any = assign_store(
    adapter_configs=adapter_configs
)  # TODO: Fix the typing, should be Type[AdapterConfig]


class StoreConfig(BaseModel):

    profiles: Dict[str, Store]
    name: str


class StoresConfig(BaseModel):

    stores: List[StoreConfig]

    def store(self, name: str, profile: Optional[str] = None):
        for store in self.stores:
            if store.name == name:
                if profile:
                    return store.profiles[profile]
                return store.profiles
        raise ValueError(f"Store {name} not found")
