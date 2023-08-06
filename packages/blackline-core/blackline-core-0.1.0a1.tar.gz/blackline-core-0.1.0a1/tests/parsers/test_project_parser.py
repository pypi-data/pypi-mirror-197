from pathlib import Path

from blackline.constants import (
    DEFAULT_ADAPTERS_FOLDER,
    DEFAULT_CATALOGUE_FOLDER,
    PROJECT_CONFIG_FILE,
)
from blackline.models.project_config import ProjectConfig
from blackline.parsers.project import ProjectParser


def test__init__(project_root):
    parser = ProjectParser(path=project_root, filename=PROJECT_CONFIG_FILE)

    assert isinstance(parser, ProjectParser)


def test_parse_project_config(project_parser, project_root):
    config = project_parser.config()

    assert isinstance(config, ProjectConfig)
    assert config.name == "test_project"
    assert config.config_version == 1
    assert config.version == "0.0.1"
    assert config.default_profile == "dev"
    assert config.catalogue_path == Path(DEFAULT_CATALOGUE_FOLDER)
    assert config.adapters_path == Path(DEFAULT_ADAPTERS_FOLDER)
    assert config.project_root == project_root
