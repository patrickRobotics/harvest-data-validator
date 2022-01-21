"""This module provides the Python Harvest Data Validator CLI."""
# data_validator/cli.py

from pathlib import Path
import typer
from typing import Optional

from data_validator.validator import FarmDataValidator
from data_validator import (
    ERRORS, DIR_ERROR, FILES_ERROR, __app_name__, __version__
)
from data_validator.helpers.utils import (
    get_folder_files, get_data_from_json_file, get_farm_images
)

app = typer.Typer()


def _format_errors(
        file_path: str, error: str, error_msg: str
) -> str:
    path = typer.style(f'{file_path}', fg=typer.colors.BLUE, underline=True)
    error = typer.style(f'{ERRORS[error]}', fg=typer.colors.RED, bold=True)
    return f'{error_msg} {path} failed with {error}'


@app.command(name="validate")
def validate_harvest_data(
        data_directory: Path = typer.Option(
            None, "--data_directory", "-dir",
            prompt="path to unzipped data directory?", ),
) -> None:
    if not data_directory.is_dir() or not data_directory.exists():
        typer.secho(
            _format_errors(data_directory, DIR_ERROR, 'Getting data directory'),
            fg=typer.colors.RED, )
        raise typer.Exit(1)

    typer.secho(f'**************** Processing farm data start ***************',
                fg=typer.colors.BRIGHT_WHITE, underline=True)

    folder_items = get_folder_files(path=data_directory)

    if type(folder_items) == int:
        typer.secho(
            _format_errors(data_directory, FILES_ERROR, 'Getting files from'),
            fg=typer.colors.RED, )
        raise typer.Exit(1)

    farm_images = []
    with typer.progressbar(folder_items, label="Processing", length=100) as progress:
        for file in progress:
            if file.endswith(".json"):
                harvest_data = get_data_from_json_file(file)
                validator = FarmDataValidator(data=harvest_data)
                typer.secho(f'Harvest data analysis results:', fg=typer.colors.BRIGHT_GREEN)

                typer.secho(validator.validate_multiple_measurements_for_one_crop(), fg=typer.colors.MAGENTA, )
                typer.secho(validator.validate_dry_weight_deviations(), fg=typer.colors.CYAN, )
                typer.secho(validator.validate_weights(), fg=typer.colors.BRIGHT_YELLOW, )
                typer.secho(validator.validate_farm_distances(), fg=typer.colors.BRIGHT_BLUE, )
            else:
                farm_images.append(get_farm_images(file))

        image_validator = FarmDataValidator(images=farm_images)
        typer.secho(image_validator.validate_photos(), fg=typer.colors.BRIGHT_WHITE, )

    typer.secho(f'******** Farm data harvest validation completed ***********',
                fg=typer.colors.BRIGHT_WHITE, underline=True)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return
