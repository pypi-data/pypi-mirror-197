from pathlib import Path

from blackline.constants import (
    DEFAULT_ADAPTERS_FOLDER,
    DEFAULT_CATALOGUE_FOLDER,
    PROJECT_CONFIG_FILE,
    PROJECT_CONFIG_VERSION,
    PROJECT_VERSION,
)
from blackline.models.project_config import ProjectConfig
from blackline.project.init import create_project_yml, init_project
from yaml import Loader, load


def test_init_project(tmp_path: Path, fake_project_name: str) -> None:
    """Test that the project is initialised correctly."""
    # Setup
    project_config_path = Path(tmp_path, fake_project_name, PROJECT_CONFIG_FILE)

    # Run
    project_config = init_project(path=tmp_path, name=fake_project_name)

    # Assert
    assert project_config_path.is_file()
    assert project_config.catalogue_path.is_dir()
    assert project_config.adapters_path.is_dir()
    assert (
        Path(tmp_path, fake_project_name, DEFAULT_ADAPTERS_FOLDER)
        == project_config.adapters_path
    )
    assert (
        Path(tmp_path, fake_project_name, DEFAULT_CATALOGUE_FOLDER)
        == project_config.catalogue_path
    )


def test_create_project_yml(tmp_path: Path, fake_project_name: str) -> None:
    """Test that the project is initialised correctly."""
    # Setup
    project_config_path = Path(tmp_path, PROJECT_CONFIG_FILE)
    project_config = ProjectConfig(
        name=fake_project_name,
        config_version=PROJECT_CONFIG_VERSION,
        version=PROJECT_VERSION,
        default_profile="default",
        catalogue_path=Path(DEFAULT_CATALOGUE_FOLDER),
        adapters_path=Path(DEFAULT_ADAPTERS_FOLDER),
        project_root=tmp_path,
    )

    # Run
    create_project_yml(path=tmp_path, project_config=project_config)

    # Assert
    project_text = project_config_path.read_text()
    project_obj = load(project_text, Loader=Loader)

    assert project_config_path.is_file()
    assert project_config.name == project_obj["name"]
    assert project_config.config_version == project_obj["config-version"]
    assert project_config.version == project_obj["version"]
    assert project_config.default_profile == project_obj["default-profile"]
    assert project_config.catalogue_path == Path(project_obj["catalogue-path"])
    assert project_config.adapters_path == Path(project_obj["adapters-path"])
