from dataclasses import dataclass


@dataclass(slots=True)
class ChangedPath:
    path: str
    action: str


@dataclass(slots=True)
class Revision:
    revision: int
    author: str
    date: str
    message: str
    changed_paths: list[ChangedPath]
