from pathlib import Path
from dataclasses import dataclass, field
from typing import List
import requests
from rich import print
from rich.markup import escape
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    BarColumn,
    RenderableColumn,
)
from rich.syntax import Syntax
from rich.panel import Panel
from rich.console import Group
from rich.live import Live
import json
from geovisio_cli.exception import CliException
from geovisio_cli.auth import login
from geovisio_cli.model import Geovisio


@dataclass
class Picture:
    path: str


@dataclass
class Sequence:
    title: str
    pictures: List[Picture] = field(default_factory=lambda: [])


@dataclass
class UploadError:
    position: int
    picture_path: str
    error: str
    status_code: int


@dataclass
class UploadedPicture:
    path: str
    location: str


@dataclass
class UploadReport:
    location: str
    uploaded_pictures: List[UploadedPicture] = field(default_factory=lambda: [])
    errors: List[UploadError] = field(default_factory=lambda: [])


def process(path: Path) -> Sequence:
    sequence = _read_sequence(path)
    _check_sequence(sequence)
    return sequence


def upload(path: Path, geovisio: Geovisio) -> UploadReport:
    # early test that the given url is correct
    _test_geovisio_url(geovisio.url)

    sequence = process(path)

    return _publish(sequence, geovisio)


def _publish(sequence: Sequence, geovisio: Geovisio) -> UploadReport:
    print(f'📂 Publishing "{sequence.title}"')

    data = {}
    if sequence.title:
        data["title"] = sequence.title

    with requests.session() as s:
        seq = s.post(f"{geovisio.url}/api/collections", data=data)
        if seq.status_code == 401:
            login(s, geovisio)
            seq = s.post(f"{geovisio.url}/api/collections", data=data)
        seq.raise_for_status()

        seq_location = seq.headers["Location"]
        print(f"✅ Created sequence {seq_location}")
        report = UploadReport(location=seq_location)

        uploading_progress = Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            TextColumn("[{task.completed}/{task.total}]"),
        )
        current_pic_progress = Progress(
            TextColumn("📷 Processing [bold purple]{task.fields[file]}"),
            SpinnerColumn("simpleDots"),
        )
        error_progress = Progress(TextColumn("{task.description}"))

        last_error = Progress(
            TextColumn("🔎 Last error 🔎\n{task.description}"),
        )
        error_panel = Panel(Group(error_progress, last_error), title="Errors")
        uploading_task = uploading_progress.add_task(
            f"[green] 🚀 Uploading pictures...",
            total=len(sequence.pictures),
        )
        current_pic_task = current_pic_progress.add_task("", file="")
        progress_group = Group(
            uploading_progress,
            current_pic_progress,
            error_panel,
        )
        error_task = error_progress.add_task("[green]No errors")
        last_error_task = last_error.add_task("", visible=False)
        with Live(progress_group):
            for i, p in enumerate(sequence.pictures, start=1):
                uploading_progress.advance(uploading_task)
                current_pic_progress.update(
                    current_pic_task, file=p.path.split("/")[-1]
                )
                picture_response = s.post(
                    f"{seq_location}/items",
                    files={"picture": open(p.path, "rb")},
                    data={"position": i},
                )
                if picture_response.status_code >= 400:
                    body = (
                        picture_response.json()
                        if picture_response.headers.get("Content-Type")
                        == "application/json"
                        else picture_response.text
                    )
                    report.errors.append(
                        UploadError(
                            position=i,
                            picture_path=p.path,
                            status_code=picture_response.status_code,
                            error=body,
                        )
                    )

                    error_progress.update(
                        error_task,
                        description=f"[bold red]{len(report.errors)} errors",
                    )
                    last_error.update(last_error_task, description=body, visible=True)
                else:
                    report.uploaded_pictures.append(
                        UploadedPicture(
                            path=p.path,
                            location=picture_response.headers["Location"],
                        )
                    )

        if not report.uploaded_pictures:
            print(
                f"[red]💥 All pictures upload of sequence {sequence.title} failed! 💥[/red]"
            )
        else:
            print(
                f"🎉 Uploaded [bold green]{len(report.uploaded_pictures)}[/bold green] pictures"
            )
            # for uploaded_pic in report.uploaded_pictures:
            # print(f" * {uploaded_pic.path} -> {uploaded_pic.location}")
        if report.errors:
            print(f"[bold red]{len(report.errors)}[/bold red] pictures not uploaded:")
            for e in report.errors:
                msg = escape(e.error.replace("\n", "\\n"))
                print(f" - {e.picture_path} (status [bold]{e.status_code}[/]): {msg}")

        return report


def _check_sequence(sequence: Sequence):
    if not sequence.pictures:
        raise CliException(f"No pictures to upload for sequence {sequence.title}")


def _read_sequence(path: Path) -> Sequence:
    if not path.is_dir():
        raise CliException(f"{path} is not a directory, cannot read pictures")

    s = Sequence(title=path.name)

    for f in path.iterdir():
        if not f.is_file():
            continue
        if f.suffix.lower() not in [".jpg", "jpeg"]:
            continue
        s.pictures.append(Picture(path=str(f)))

    return s


def _test_geovisio_url(geovisio: str):
    full_url = f"{geovisio}/api/collections"
    try:
        r = requests.get(full_url)
    except requests.ConnectionError as e:
        raise CliException(f"Impossible to query geovisio base url:\n\t{e}")
    if r.status_code >= 400:
        raise CliException(f"Impossible to query geovisio: {r.status_code}:\n {r.text}")


def get_collection_status(collection) -> dict:
    status = requests.get(f"{collection}/geovisio_status")
    status.raise_for_status()
    return status.json()
