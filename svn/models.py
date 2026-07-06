from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ChangedPath:
    path: str
    action: str

    @property
    def relative_path(self) -> Path:
        return Path(self.path.lstrip("/"))

    @property
    def exists_before(self) -> bool:
        return self.action not in {"A"}

    @property
    def exists_after(self) -> bool:
        return self.action not in {"D"}


@dataclass(slots=True)
class Revision:
    revision: int
    author: str
    date: str
    message: str
    changed_paths: list[ChangedPath]
