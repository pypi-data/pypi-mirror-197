from datetime import datetime
from os import listdir
from pathlib import Path
from sqlite3 import connect

from blackline.execution.demo import (
    create_demo,
    load_shipments,
    load_users,
    sample_adapter,
    sample_catalogue,
)
from yaml import safe_load


def test_create_demo(tmp_path: Path):
    # Setup
    name = "sample_project"
    root_path = Path(tmp_path, name)
    # Run
    create_demo(path=tmp_path, name=name, overwrite=True)

    # Assert
    assert "adapters" in listdir(Path(tmp_path, name))
    assert "sample_sqlite.yml" in listdir(Path(tmp_path, name, "adapters"))
    assert "catalogue" in listdir(Path(tmp_path, name))
    assert "sample_sqlite" in listdir(Path(tmp_path, name, "catalogue"))
    assert "sample_catalogue.yml" in listdir(
        Path(tmp_path, name, "catalogue", "sample_sqlite")
    )
    assert "blackline_sample.db" in listdir(Path(tmp_path, name))
    assert "blackline_project.yml" in listdir(Path(tmp_path, name))

    adapter_path = Path(tmp_path, name, "adapters", "sample_sqlite.yml")
    catalogue_path = Path(
        tmp_path, name, "catalogue", "sample_sqlite", "sample_catalogue.yml"
    )

    with open(adapter_path, "rt") as f:
        adapter = safe_load(f.read())
        assert adapter == sample_adapter(root_path=root_path)

    with open(catalogue_path, "rt") as f:
        catalogue = safe_load(f.read())
        assert catalogue == sample_catalogue()

    with connect(Path(tmp_path, name, "blackline_sample.db")) as conn:
        cur = conn.execute("SELECT * FROM user")
        users = cur.fetchall()
        cur = conn.execute("SELECT * FROM shipment")
        shipments = cur.fetchall()

        users = [
            [
                u[0],
                u[1],
                u[2],
                u[3],
                bool(u[4]),
                datetime.strptime(u[5], "%Y-%m-%d %H:%M:%S"),
            ]
            for u in users
        ]
        shipments = [
            [
                s[0],
                s[1],
                datetime.strptime(s[2], "%Y-%m-%d %H:%M:%S"),
                s[3],
                s[4],
                s[5],
                s[6],
            ]
            for s in shipments
        ]
        assert users == load_users()
        assert shipments == load_shipments()
