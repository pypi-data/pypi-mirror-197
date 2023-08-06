import logging
from datetime import datetime
from pathlib import Path

import click
from blackline.execution.debug import debug as execution_debug
from blackline.execution.deidentify import deidentify
from blackline.execution.demo import create_demo
from blackline.execution.report import create_report
from blackline.project.init import init_project

from blackline import __version__

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def default_project_dir() -> Path:
    """Return the default project directory."""
    return Path.cwd()


debug_flag = click.option("--debug/--no-debug", default=False, help="Debug mode")

version = click.option("--version", "-v", is_flag=True, help="Show blackline version")

project_dir = click.option(
    "--project-dir",
    "-p",
    type=Path,
    default=default_project_dir(),
    show_default=True,
    help="Project directory, where blackline_project.yml is located",
)
name = click.option(
    "--name",
    "-n",
    type=str,
    default="blackline",
    show_default=True,
    help="Project name",
)
name_sample = click.option(
    "--name",
    "-n",
    type=str,
    default="blackline_sample",
    show_default=True,
    help="Project name",
)

profile = click.option(
    "--profile", type=str, required=True, help="Data stores profile to use"
)

start_date = click.option(
    "--start-date",
    type=click.DateTime(),
    default=datetime.now().strftime("%Y-%m-%d"),
    show_default=True,
    help="Start date for deidentification",
)

default_profile = click.option(
    "--default-profile",
    type=str,
    default="default",
    show_default=True,
    help="Default profile to use",
)
catalogue_path = click.option(
    "--catalogue-path",
    type=Path,
    default="catalogue",
    show_default=True,
    help="Path to the catalogue folder",
)
adapters_path = click.option(
    "--adapters-path",
    type=Path,
    default="adapters",
    show_default=True,
    help="Path to the adapters folder",
)

overwrite = click.option(
    "--overwrite/--no-overwrite",
    default=False,
    show_default=True,
    help="Overwrite existing project",
)


@click.version_option(package_name="blackline-core", prog_name="blackline-core")
@click.group(
    invoke_without_command=True,
    help=f"Blackline CLI version {__version__}",
    no_args_is_help=True,
)
@click.pass_context
@debug_flag
def cli(ctx, debug):
    if ctx.invoked_subcommand is None:
        if debug:
            click.echo("Debug mode is %s" % ("on" if debug else "off"))


@cli.command(help="Initialize a project.", no_args_is_help=True)
@project_dir
@name
@default_profile
@catalogue_path
@adapters_path
def init(project_dir, name, default_profile, catalogue_path, adapters_path):
    init_project(
        path=project_dir,
        name=name,
        default_profile=default_profile,
        catalogue_folder=catalogue_path,
        adapters_folder=adapters_path,
    )
    click.echo(f"Initialized blackline project at: {project_dir}")


@cli.command(help="Run project.", no_args_is_help=True)
@profile
@project_dir
@start_date
def run(profile, project_dir, start_date):
    click.echo(f"Running project: {project_dir}")
    click.echo(f"Running profile: {profile}")
    click.echo(f"Running start date: {start_date}")
    deidentify(path=project_dir, profile=profile, start_date=start_date)


@cli.command(help="Test data store connections.", no_args_is_help=True)
@profile
@project_dir
def debug(profile, project_dir):
    result = execution_debug(path=project_dir, profile=profile)
    click.secho(f"Testing connections for profile: {profile}", bold=True)
    for name, status in result.items():
        click.secho(
            f"  {name}: {status}",
            fg="green" if status else "red",
        )


@cli.command(help="Create a sample project.", no_args_is_help=False)
@project_dir
@name_sample
@overwrite
def sample(project_dir, name, overwrite):
    create_demo(path=project_dir, name=name, overwrite=overwrite)
    click.echo(f"Created sample project at: {project_dir}")


@cli.command(help="Report the defined project.", no_args_is_help=False)
@project_dir
def report(project_dir):
    project, stores, catalogue = create_report(path=project_dir)

    click.secho("=" * 80, fg="magenta")
    click.secho("Project Settings:", fg="magenta")
    click.echo(f"Project name: {project.name}")
    click.echo(f"Project Root: {project.project_root}")
    click.echo(f"Adapters path: {project.adapters_path}")
    click.echo(f"Catalogue path: {project.catalogue_path}")
    click.echo(f"Default profile: {project.default_profile}")
    click.echo("")
    click.secho("Data Stores:", fg="magenta")
    for store in stores:
        click.echo("Data Store: " + click.style(f"{store.name}", fg="blue"))
        click.echo("Profiles:")
        for profile, value in store.profiles.items():
            click.echo(f"  {profile}")
            click.echo(f"    Type: {value.type}")
            click.echo(f"    Adapter: {value.adapter}")
            click.echo("    Config:")
            click.echo("      Connection:")
            for conn_key, conn_value in value.config.connection.dict().items():
                click.echo(f"        {conn_key}: {conn_value}")
    click.echo("")
    click.secho("Catalogue:", fg="magenta")
    for store in catalogue.stores:
        click.echo("Data Store :" + click.style(f"{store.name}", fg="blue"))
        click.echo("  Tables:")
        for table in store.tables.values():
            click.echo("    Table: " + click.style(f"{table.name}", fg="cyan"))
            click.echo(f"    Datetime column: {table.datetime_column}")
            click.echo("    Columns:")
            for column in table.columns:
                click.echo("      " + click.style(f"{column.name}", fg="yellow"))
                click.echo("        Deidentifier:")
                for (
                    deident_key,
                    dident_value,
                ) in column.deidentifier.dict().items():
                    click.echo(f"          {deident_key}: {dident_value}")
                click.echo(f"        Period: {column.period}")
                click.echo(f"        Description: {column.description}")
            click.echo("")
        click.echo("")
    click.secho("=" * 80, fg="magenta")


if __name__ == "__main__":
    cli(auto_envvar_prefix="BLACKLINE")
