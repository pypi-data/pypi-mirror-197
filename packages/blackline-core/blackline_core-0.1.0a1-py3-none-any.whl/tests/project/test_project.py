from pathlib import Path

from blackline.models.project_config import ProjectConfig
from blackline.parsers.project import ProjectParser
from blackline.project.project import Project


def test__init__(project_root: Path, project_config_file: Path) -> None:
    """Test the Project class constructor."""
    project = Project(path=project_root, filename=project_config_file)
    assert project.parser.path == project_root
    assert project.parser.filename == project_config_file
    assert isinstance(project.parser, ProjectParser)


def test_adapters_path(project: Project) -> None:
    """Test the adapters_path property."""

    assert Path(*project.adapters_path.parts[-4:]) == Path(
        "tests/mock_projects/core/adapters"
    )


def test_catalogue_path(project: Project) -> None:
    """Test the catalogue_path property."""

    assert Path(*project.catalogue_path.parts[-4:]) == Path(
        "tests/mock_projects/core/catalogue"
    )


def test_config(project: Project) -> None:
    """Test the config method."""

    assert isinstance(project.config(), ProjectConfig)
