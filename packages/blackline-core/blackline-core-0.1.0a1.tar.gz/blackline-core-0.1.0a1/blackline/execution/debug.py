from pathlib import Path

from blackline.parsers.stores import StoresParser
from blackline.project.project import Project


class Debug:
    def __init__(self, path: Path, profile: str):
        self.path = path
        self.profile = profile
        self.project = Project(path=path)
        self.stores = StoresParser(path=self.project.adapters_path).stores

    def debug(self):
        return {
            store.name: store.profiles[self.profile].adapter.test_connection()
            for store in self.stores.stores
        }


def debug(path: Path, profile: str):
    debug = Debug(path=path, profile=profile)
    return debug.debug()
