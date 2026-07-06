from pathlib import Path
import subprocess

from svn.models import Revision
from svn.parser import parse_log_xml


class SvnClient:
    def __init__(self, project_path: Path) -> None:
        self.project_path = project_path

    def is_working_copy(self) -> bool:
        result = subprocess.run(
            ["svn", "info"],
            cwd=self.project_path,
            capture_output=True,
            text=True,
        )

        return result.returncode == 0

    def get_recent_revisions(self, limit: int = 100) -> list[Revision]:
        result = subprocess.run(
            ["svn", "log", "--xml", "-v", "-l", str(limit)],
            cwd=self.project_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return parse_log_xml(result.stdout)

    def cat_file(self, repository_path: str, revision: int) -> bytes:
        result = subprocess.run(
            ["svn", "cat", "-r", str(revision), repository_path],
            cwd=self.project_path,
            capture_output=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode(errors="replace").strip())

        return result.stdout


    def get_revision_diff(self, revision: int) -> str:
        result = subprocess.run(
            ["svn", "diff", "-c", str(revision)],
            cwd=self.project_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return result.stdout


    def get_revision_info_text(self, revision: int) -> str:
        result = subprocess.run(
            ["svn", "log", "-r", str(revision), "-v"],
            cwd=self.project_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return result.stdout
