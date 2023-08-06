from datetime import datetime
from pathlib import Path

from blackline.cli.cli import cli
from click.testing import CliRunner


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0


def test_cli_init(monkeypatch, tmp_path):
    def _init_project(*args, **kwargs):
        assert kwargs["path"] == tmp_path
        assert kwargs["name"] == "blackline"
        assert kwargs["default_profile"] == "default"
        assert kwargs["catalogue_folder"] == Path("catalogue")
        assert kwargs["adapters_folder"] == Path("adapters")

    monkeypatch.setattr("blackline.project.init._init_project", _init_project)
    runner = CliRunner()
    result = runner.invoke(cli, ["init", "--project-dir", str(tmp_path)])
    assert result.exit_code == 0


def test_run(monkeypatch):
    def _deidentify(path, profile, start_date):
        assert path == Path("project")
        assert profile == "default"
        assert start_date == datetime(2023, 1, 1)

    monkeypatch.setattr("blackline.cli.cli.deidentify", _deidentify)
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "run",
            "--project-dir",
            "project",
            "--profile",
            "default",
            "--start-date",
            "2023-01-01",
        ],
    )
    assert result.exit_code == 0


def test_debug(monkeypatch, project_root, profile):
    def _debug(path, profile):
        assert path == project_root
        assert profile == profile
        return {"test_store_0": True, "test_store_1": False}

    monkeypatch.setattr("blackline.cli.cli.execution_debug", _debug)
    runner = CliRunner()
    result = runner.invoke(
        cli, ["debug", "--project-dir", str(project_root), "--profile", profile]
    )
    assert result.exit_code == 0
