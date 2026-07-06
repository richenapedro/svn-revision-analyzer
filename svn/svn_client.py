from pathlib import Path
import subprocess

from svn.models import Revision
from svn.parser import parse_log_xml


class SvnClient:
    def __init__(self, project_path: Path) -> None:
        self.project_path = project_path
        self._repository_root_url: str | None = None

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
        repository_root_url = self.get_repository_root_url()
        normalized_path = repository_path.lstrip("/")
        file_url = f"{repository_root_url}/{normalized_path}"

        result = subprocess.run(
            ["svn", "cat", "-r", str(revision), file_url],
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

    def get_revision(self, revision: int) -> Revision:
        result = subprocess.run(
            ["svn", "log", "-r", str(revision), "--xml", "-v"],
            cwd=self.project_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        revisions = parse_log_xml(result.stdout)

        if not revisions:
            raise RuntimeError(f"Revisão {revision} não encontrada.")

        return revisions[0]

    def get_repository_root_url(self) -> str:
        if self._repository_root_url is not None:
            return self._repository_root_url

        result = subprocess.run(
            ["svn", "info", "--show-item", "repos-root-url"],
            cwd=self.project_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        self._repository_root_url = result.stdout.strip()
        return self._repository_root_url
