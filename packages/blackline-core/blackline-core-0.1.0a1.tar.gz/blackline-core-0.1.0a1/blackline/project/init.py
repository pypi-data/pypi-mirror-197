from pathlib import Path
from shutil import rmtree

from blackline.constants import (
    DEFAULT_ADAPTERS_FOLDER,
    DEFAULT_CATALOGUE_FOLDER,
    PROJECT_CONFIG_FILE,
    PROJECT_CONFIG_VERSION,
    PROJECT_VERSION,
)
from blackline.models.project_config import ProjectConfig
from jinja2 import Environment, PackageLoader


def init_project(
    path: Path,
    name: str,
    default_profile="default",
    catalogue_folder=None,
    adapters_folder=None,
    overwrite=False,
) -> ProjectConfig:
    """Initialise a new project."""
    return _init_project(
        path=path,
        name=name,
        default_profile=default_profile,
        catalogue_folder=catalogue_folder,
        adapters_folder=adapters_folder,
        overwrite=overwrite,
    )


def _init_project(
    path: Path,
    name: str,
    default_profile="default",
    catalogue_folder=None,
    adapters_folder=None,
    overwrite=False,
) -> ProjectConfig:
    """Initialise a new project."""

    project_path = Path(path, name)
    if project_path.exists() and not overwrite:
        raise FileExistsError(f"Directory {path} already exists.")

    if project_path.exists() and overwrite:
        rmtree(project_path)

    path = Path(path, name)
    catalogue_path = Path(path, catalogue_folder or DEFAULT_CATALOGUE_FOLDER)
    adapters_path = Path(path, adapters_folder or DEFAULT_ADAPTERS_FOLDER)

    path.mkdir(parents=True, exist_ok=True)
    project_config = ProjectConfig(
        name=name,
        config_version=PROJECT_CONFIG_VERSION,
        version=PROJECT_VERSION,
        default_profile=default_profile,
        catalogue_path=catalogue_path,
        adapters_path=adapters_path,
        project_root=path,
    )
    create_project_yml(path=path, project_config=project_config)
    create_folders(project_config=project_config)
    return project_config


def create_project_yml(path: Path, project_config: ProjectConfig) -> None:
    env = Environment(loader=PackageLoader("blackline.project", "templates"))
    template = env.get_template("blackline_project.yml")
    project = template.render(config=project_config)
    Path(path, PROJECT_CONFIG_FILE).write_text(project)


def create_folders(project_config: ProjectConfig) -> None:
    """Create the project folders."""
    project_config.adapters_path.mkdir(parents=True, exist_ok=True)
    project_config.catalogue_path.mkdir(parents=True, exist_ok=True)
