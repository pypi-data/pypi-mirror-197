import inspect
from importlib import import_module
from types import ModuleType
from typing import Dict, Optional

from blackline.adapters.base import AdapterBase

ADAPTER_SUBMODULE = "adapters"


class AdapterFactory:
    def __init__(self) -> None:
        self.adapters: Dict[str, AdapterBase] = {}

    def adapter(self, name: str) -> AdapterBase:
        adapter = self.adapters.get(name)
        if adapter is not None:
            return adapter
        _cls = self.load_adapter(name)
        self.adapters[name] = _cls
        return _cls

    @staticmethod
    def load_adapter(name: str) -> AdapterBase:
        mod = AdapterFactory._import_module(submodule=ADAPTER_SUBMODULE, name=name)
        return AdapterFactory._filter_class_from_module(mod)

    @staticmethod
    def _import_module(
        submodule: str, name: str, suffix: Optional[str] = None
    ) -> ModuleType:
        _name = f"blackline.{submodule}.{name}"
        if suffix is not None:
            _name += f"_{suffix}"
        try:
            return import_module(_name)
        except ModuleNotFoundError as e:
            if e.name and "blackline" in e.name:
                raise ModuleNotFoundError(
                    f"Could not import plugin: {_name}. Have you install the blackline-{name} package?"  # noqa: E501
                )
            raise e

    @staticmethod
    def _filter_class_from_module(mod):

        return inspect.getmembers(
            mod,
            lambda member: inspect.isclass(member)
            and member.__module__ == mod.__name__,
        )[0][1]
        # noqa: E501 getmembers returns a list of tuples, where the first element is the name of the class and the second is the class itself.
