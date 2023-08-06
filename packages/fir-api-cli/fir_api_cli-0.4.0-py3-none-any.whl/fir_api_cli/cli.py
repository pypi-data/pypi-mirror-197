import json
import os
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple

import typer
from gql.transport.exceptions import TransportServerError
from rich import print

from fir_api_cli import __app_name__, version

from .config import Config
from .constants import DEFAULT_CONFIG_FILE_PATH
from .fir import FIRHandler, ProductQuery, ProductsQuery
from .utils import download_from_url, save_to_csv


class Platform(Enum):
    """
    Enum class for different satellite platforms.
    """
    S1 = "Sentinel-1"
    S2 = "Sentinel-2"
    S3 = "Sentinel-3"
    S5P = "Sentinel-5P"

    @classmethod
    def list(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))


app = typer.Typer(
    pretty_exceptions_show_locals=False,
    rich_markup_mode="rich")


def get_credentials_from_env(var_name: str) -> Tuple[str, str]:
    """Read username and password from environment variables."""

    return os.environ.get(var_name)


def get_credentials_from_file(path: Path) -> Tuple[str, str]:
    """Read username and password from a config file."""

    if path.exists():
        username, password = Config().get_config(path)
    else:
        return (None, None)

    if not username or not password:
        return (None, None)

    return username, password


def get_user_name() -> str:
    """
    Read user_name from environment variable or from config file.
    User name must be in the first row.
    """
    username = (get_credentials_from_env("FIR_API_USERNAME") or
                get_credentials_from_file(DEFAULT_CONFIG_FILE_PATH)[0])

    if not username:
        typer.secho(
            'Username not found. Please, either set it as an environment '
            'variable (["FIR_API_USERNAME"]) or run the "config" CLI command '
            'to set and save to a config file.',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


def get_password() -> str:
    """
    Read password from environment variable or from config file.
    Password must be in the second row.
    """
    password = (get_credentials_from_env("FIR_API_PASSWORD") or
                get_credentials_from_file(DEFAULT_CONFIG_FILE_PATH)[1])
    if not password:
        typer.secho(
            'Password not found. Please, either set it as an environment '
            'variable (["FIR_API_PASSWORD"]) or run the "config" CLI command '
            'to set and save to a config file.',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


def platform_callback(value: str) -> str:
    """Callback function for checking if valid platform."""
    if value not in Platform.list():
        raise typer.BadParameter(f"Invalid plaform {value}, "
                                 f"only {Platform.list()} are allowed")
    return value


def version_callback(value: bool):
    """Callback function for printing app version."""
    if value:
        typer.echo(f"{__app_name__} v{version}")
        raise typer.Exit(1)


@app.callback(invoke_without_command=True)
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True)) -> None:
    """
    [bold]Explore and download products from the FIR API.[/bold]

    ---

    :warning:
    In order to use the CLI tool, user must have a valid eFöld registration.
    Support the eFöld username and password as a cli option/argument
    for each execution or set `FIR_API_USERNAME` and `FIR_API_PASSWORD`
    as environment variables or use the 'config' command to save the
    credentials to a config file.

    ---

    [bold]Learn more at:[/bold]

    - eFöld portal: <https://efold.gov.hu>
    - GraphQL user interface: <https://api.fir.gov.hu/graphql/ui>
    """


@app.command()
def config(
    username: str = typer.Argument(...),
    password: str = typer.Argument(...),
) -> None:
    """
    [bold]Utility function to save credentials permamently to config.[/bold]
    """

    try:
        config = Config()
        path = config.set_config(username, password, DEFAULT_CONFIG_FILE_PATH)
        typer.secho(
            f"The configuration file is at {str(path)}", fg=typer.colors.GREEN)
        typer.secho("\u2757Credentials stored as plaintext.",
                    fg=typer.colors.YELLOW)
    except ValueError as exc:
        typer.secho("Failed to create configuration file.",
                    fg=typer.colors.RED)
        raise typer.Exit(1) from exc


@app.command()
def query_id(
    username: str = typer.Option(
        get_user_name,
        "--username",
        "-u",
        help="Registered eföld user's name.",
        show_default="User name extracted from env. variable "
        "['FIR_API_USERNAME'] or from config file."),
    password: str = typer.Option(
        get_password,
        "--password",
        "-pw",
        help="Registered eföld user's password.",
        show_default="Password extracted form env. variable "
        "['FIR_API_PASSWORD'] or from config file."),
    id: str = typer.Option(
        ...,
        "--id",
        "-i",
        help="Product id, e.g. fd3b0a77-6d2d-4207-9427-361bcbd9feaa."),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Path to csv to save result."),
    download: Optional[str] = typer.Option(
        None,
        "--download",
        "-d",
        help="Path to folder to save the file."),
    verbose: Optional[bool] = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Give more output.",
        show_default="False, returns short info."),
    quiet: Optional[bool] = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress the output on console.",
        show_default="False, result is printed on the console.")):
    """
    [bold]Query and/or download product based on id.[/bold]

    ---

    [bold]Examples:[/bold]

    ```
    $ fir-api query-id --id fd3b0a77-6d2d-4207-9427-361bcbd9feaa
    ```

    """

    query_obj = ProductQuery(verbose=verbose)
    fir = FIRHandler(username, password, query_obj)

    fir.create_query_parameters({'id': id})

    try:
        response = fir.query()
    except TransportServerError as exc:
        typer.secho("Authentication error - invalid username or password.",
                    fg=typer.colors.RED)
        raise typer.Exit(1) from exc

    product = response['product']

    if output:
        path_to_save = Path(output)
        try:
            save_to_csv([product], path_to_save)
        except FileNotFoundError as exc:
            typer.secho(f"Invalid output path: {output}", fg=typer.colors.RED)
            raise typer.Exit(1) from exc

    if not quiet:
        print(json.dumps(product, indent=4))

    if download:
        url = product.get('downloadUrl')
        filename = product.get('filename').split('.')[0] + '.zip'
        size = product.get('size')
        path = Path(download, filename)
        headers = fir.get_headers()
        typer.secho(f'Download {filename}', fg=typer.colors.YELLOW)
        try:
            download_from_url(url=url, headers=headers,
                              path_to_save=path, size=size)
            typer.secho(f'Finished download', fg=typer.colors.GREEN)
        except FileNotFoundError as exc:
            typer.secho(
                f"Invalid output path: {str(path)}", fg=typer.colors.RED)
            raise typer.Exit(1) from exc


@app.command()
def query(
    username: str = typer.Option(
        get_user_name,
        "--username",
        "-u",
        help="Registered eföld user's name.",
        show_default="User name extracted from env. variable "
        "['FIR_API_USERNAME'] or from config file."),
    password: str = typer.Option(
        get_password,
        "--password",
        "-pw",
        help="Registered eföld user's password.",
        show_default="Password extracted form env. variable "
        "['FIR_API_PASSWORD'] or from config file."),
    platform: str = typer.Option(
        ...,
        "--platform",
        "-p",
        help="Satellite platfrom name, e.g. Sentinel-2",
        callback=platform_callback),
    date: Tuple[str, str] = typer.Option(
        ...,
        "--date",
        "-dt",
        help="Begin and end postion date range, e.g. 2022-10-01 2022-10-10"),
    product_type: Optional[str] = typer.Option(
        None,
        "--product-type",
        "-pt",
        help="Product type for type based fitering, e.g. S2MSI2A"),
    tile: Optional[str] = typer.Option(
        None,
        "--tile",
        "-t",
        help="Tile id for tile based filtering e.g 33TYL."),
    cloud_cover: Optional[float] = typer.Option(
        None,
        "--cloud-cover",
        "-c",
        help="Max cloud cover percentage."),
    relative_orbit: Optional[int] = typer.Option(
        None,
        "--relative_orbit",
        "-ro",
        help="Relative orbit number."),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Path to csv to save results."),
    download: Optional[str] = typer.Option(
        None,
        "--download",
        "-d",
        help="Path to folder to save the files."),
    verbose: Optional[bool] = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Give more output.",
        show_default="False, returns short info."),
    quiet: Optional[bool] = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress the output on console.",
        show_default="False, result is printed on the console.")):
    """
    [bold]Query and/or download products based on query parameters.[/bold]

    ---

    [bold]Examples:[/bold]

    ```
    $ fir-api query --platform Sentinel-2 --date 2021-01-01 2021-01-05 -q False
    ```
    """

    query_obj = ProductsQuery(verbose=verbose)
    fir = FIRHandler(username, password, query_obj)

    query_dict = {
        'platform': platform,
        'begin_position': date[0],
        'end_position': date[1],
    }
    fir.create_query_parameters(query_dict)

    if tile:
        fir.create_query_parameters({'tile': tile})
    if product_type:
        fir.create_query_parameters({'product_type': product_type})
    if cloud_cover:
        fir.create_query_parameters({'cloud_cover': cloud_cover})
    if relative_orbit:
        fir.create_query_parameters({'relative_orbit': relative_orbit})

    try:
        response = fir.query()
        item = next(response, None)
    except TransportServerError as exc:
        typer.secho("Authentication error - invalid username or password.",
                    fg=typer.colors.RED)
        raise typer.Exit(1) from exc

    total_count = item.get('products').get('totalCount')
    if download:
        user_input = typer.prompt(
            "Are you sure, you want to download a total number of "
            f"{total_count} dataset? (y/n)", )
        if user_input != "y":
            raise typer.Exit(1)

    while item is not None:
        products = item.get('products').get('items')

        if output:
            path_to_save = Path(output)
            try:
                save_to_csv(products, path_to_save)
            except FileNotFoundError as exc:
                typer.secho(
                    f"Invalid output path: {output}", fg=typer.colors.RED)
                raise typer.Exit(1) from exc

        if not quiet:
            print(json.dumps(item.get('products'), indent=4))

        if download:
            for img in products:
                url = img.get('downloadUrl')
                filename = img.get('filename').split('.')[0] + '.zip'
                size = img.get('size')
                path = Path(download, filename)
                headers = fir.get_headers()
                typer.secho(f'Download {filename}', fg=typer.colors.YELLOW)
                try:
                    download_from_url(url=url, headers=headers,
                                      path_to_save=path, size=size)
                    typer.secho('Finished download', fg=typer.colors.GREEN)
                except FileNotFoundError as exc:
                    typer.secho(
                        f"Invalid output path: {str(path)}",
                        fg=typer.colors.RED)
                    raise typer.Exit(1) from exc

        item = next(response, None)
