from dataclasses import dataclass

import typer

__version__ = '1.5.0'  # must match the version in pyproject.toml


@dataclass
class AppDesc:
    app: typer.Typer
    name: str
    help: str
