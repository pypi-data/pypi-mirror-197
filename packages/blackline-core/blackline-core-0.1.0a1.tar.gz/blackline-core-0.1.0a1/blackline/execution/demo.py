from datetime import datetime
from pathlib import Path
from sqlite3 import Connection, connect

from blackline.constants import SAMPLE_DATABASE, SAMPLE_PROJECT_NAME
from blackline.models.project_config import ProjectConfig
from blackline.project.init import init_project
from yaml import dump

current_path = Path(__file__).parent.resolve()


def create_demo(path: Path, name: str = SAMPLE_PROJECT_NAME, overwrite: bool = False):
    project_config = init_project(path=path, name=name, overwrite=overwrite)
    root_path = Path(path, name)
    create_database(path=root_path)
    create_adapters(root_path=root_path, project_config=project_config)
    create_catalogue(project_config=project_config)


def create_database(path: Path):
    users = load_users()
    shipments = load_shipments()
    conn = connection(path=path)
    create_user_table(conn=conn, users=users)
    create_shipment_table(conn=conn, shipments=shipments)


def load_users() -> list[list[object]]:
    users = [
        ["00", "Bar", "bar@example.com", "555.444.3.2", True, datetime(2021, 2, 1)],
        ["01", "Biz", "biz@example.com", "555.444.3.3", True, datetime(2022, 6, 1)],
        ["02", "Baz", "baz@example.com", "555.444.3.4", False, datetime(2022, 2, 1)],
        ["03", "Cat", "cat@example.com", "555.444.3.5", True, datetime(2023, 1, 1)],
        ["04", "Dog", "dog@example.com", "555.444.3.6", False, datetime(2023, 1, 1)],
    ]
    return users


def load_shipments() -> list[list[object]]:
    shipments = [
        [
            "00",
            "01",
            datetime(2022, 6, 1),
            "Ceintuurbaan 282",
            "1072 GK",
            "Amsterdam",
            "delivered",
        ],
        [
            "01",
            "02",
            datetime(2022, 3, 1),
            "Singel 542",
            "1017 AZ",
            "Amsterdam",
            "delivered",
        ],
        [
            "02",
            "02",
            datetime(2022, 4, 15),
            "Singel 542",
            "1017 AZ",
            "Amsterdam",
            "delivered",
        ],
        [
            "03",
            "03",
            datetime(2023, 1, 5),
            "Wibautstraat 150",
            "1091 GR",
            "Amsterdam",
            "delivered",
        ],
        [
            "04",
            "03",
            datetime(2023, 1, 6),
            "Wibautstraat 150",
            "1091 GR",
            "Amsterdam",
            "returned",
        ],
        [
            "05",
            "03",
            datetime(2023, 1, 6),
            "Wibautstraat 150",
            "1091 GR",
            "Amsterdam",
            "delivered",
        ],
    ]
    return shipments


def connection(path: Path) -> Connection:
    path = Path(path, SAMPLE_DATABASE)
    con = connect(str(path))
    return con


def create_user_table(conn: Connection, users: list[list[object]]) -> None:
    with conn:
        cur = conn.execute(
            "CREATE TABLE IF NOT EXISTS user(id, name, email, ip, verified, created_at)"
        )
        cur.executemany("INSERT INTO user VALUES(?, ?, ?, ?, ?, ?)", users)


def create_shipment_table(conn: Connection, shipments: list[list[object]]) -> None:
    with conn:
        cur = conn.execute(
            "CREATE TABLE IF NOT EXISTS shipment(id, user_id, order_date, street, postcode, city,status)"  # noqa E501
        )
        cur.executemany("INSERT INTO shipment VALUES(?, ?, ?, ?, ?, ?, ?)", shipments)


def sample_adapter(root_path: Path) -> dict:
    database = Path(root_path, SAMPLE_DATABASE)
    return {
        "profiles": {
            "dev": {
                "type": "sqlite",
                "config": {
                    "connection": {
                        "database": str(database),
                        "uri": True,
                    }
                },
            }
        }
    }


def create_adapters(root_path: Path, project_config: ProjectConfig) -> None:
    _sample_adapter = sample_adapter(root_path=root_path)
    with open(Path(project_config.adapters_path, "sample_sqlite.yml"), "wt") as f:
        dump(_sample_adapter, f)


def sample_catalogue() -> dict:
    return {
        "user": {
            "datetime_column": "created_at",
            "columns": [
                {
                    "name": "name",
                    "deidentifier": {"type": "redact"},
                    "period": "P365D",
                    "description": "Name of user",
                },
                {
                    "name": "email",
                    "deidentifier": {"type": "replace", "value": "fake@email.com"},
                    "period": "P365D",
                },
                {
                    "name": "ip",
                    "deidentifier": {"type": "mask", "value": "#"},
                    "period": "280 00",
                },
            ],
        },
        "shipment": {
            "datetime_column": "order_date",
            "columns": [
                {
                    "name": "street",
                    "deidentifier": {"type": "redact"},
                    "period": "P185D",
                }
            ],
        },
    }


def create_catalogue(project_config: ProjectConfig) -> None:
    _sample_catalogue = sample_catalogue()
    sample_adapter_folder = Path(project_config.catalogue_path, "sample_sqlite")
    sample_adapter_folder.mkdir(parents=True)
    with open(
        Path(sample_adapter_folder, "sample_catalogue.yml"),
        "wt",
    ) as f:
        dump(_sample_catalogue, f)
