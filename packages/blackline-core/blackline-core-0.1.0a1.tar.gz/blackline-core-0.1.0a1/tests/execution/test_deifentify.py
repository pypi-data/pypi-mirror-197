from datetime import datetime
from pathlib import Path
from sqlite3 import Connection
from typing import List, Tuple

from blackline.catalogue.catalogue import Catalogue
from blackline.execution.deidentify import Deidentify
from blackline.models.store import StoresConfig
from blackline.project.project import Project


def test__init__(project_root: Path, profile: str) -> None:
    """Test that the Deidentify class is initialised correctly."""
    # Setup
    deidentify = Deidentify(
        path=project_root, profile=profile, start_date=datetime.now()
    )

    # Assert
    assert isinstance(deidentify, Deidentify)
    assert isinstance(deidentify.project, Project)
    assert isinstance(deidentify.stores, StoresConfig)
    assert isinstance(deidentify.catalogue, Catalogue)


def test_deidentify(
    deidentify: Deidentify,
    mock_sqlite_store: Connection,
    deidentified_mock_data: List[Tuple],
    profile: str,
) -> None:
    """Test that the Deidentify class is initialised correctly."""
    # Run
    deidentify.deidentify()

    # Assert
    assert deidentify.catalogue is not None
    adapter = deidentify.stores.store(name="core", profile=profile).adapter

    with adapter.connection() as conn:
        deidentified_data = conn.execute("SELECT * FROM test_table").fetchall()
    assert deidentified_data == deidentified_mock_data
