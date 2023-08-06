import typer
from pathlib import Path
from geovisio_cli import sequence, exception, model
from rich import print
from rich.panel import Panel


app = typer.Typer(help="GeoVisio command-line client")


@app.command()
def upload(
    path: Path = typer.Option(..., help="Local path to your sequence folder"),
    api_url: str = typer.Option(..., help="GeoVisio endpoint URL"),
    user: str = typer.Option(
        default=None,
        help="""GeoVisio user name if the geovisio instance needs it.
If none is provided and the geovisio instance requires it, the username will be asked during run.
""",
        envvar="GEOVISIO_USER",
    ),
    password: str = typer.Option(
        default=None,
        help="""GeoVisio password if the geovisio instance needs it.
If none is provided and the geovisio instance requires it, the password will be asked during run.
Note: is is advised to wait for prompt without using this variable.
""",
        envvar="GEOVISIO_PASSWORD",
    ),
):
    """Processes and sends a given sequence on your GeoVisio API"""

    geovisio = model.Geovisio(url=api_url, user=user, password=password)
    try:
        sequence.upload(path, geovisio)
    except exception.CliException as e:
        print(
            Panel(
                f"{e}", title="[red]Error while importing sequence", border_style="red"
            )
        )
        return 1


@app.command()
def test_process(
    path: Path = typer.Option(..., help="Local path to your sequence folder"),
):
    """(For testing) Generates a JSON file with metadata used for upload"""

    import json
    from dataclasses import asdict

    try:
        collection = sequence.process(path)
        print(json.dumps(asdict(collection), indent=2))
    except exception.CliException as e:
        print(f"Error while importing sequence:\n{e}")
        return 1
