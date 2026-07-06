from pathlib import Path

from svn.command_runner import SvnCommandRunner
from svn.models import Revision
from svn.parser import parse_log_xml


class SvnClient:
    def __init__(self, project_path: Path) -> None:
        self.project_path = project_path
        self.runner = SvnCommandRunner(project_path)
        self._repository_root_url: str | None = None

    def is_working_copy(self) -> bool:
        return self.runner.succeeds(["info"])

    def get_recent_revisions(self, limit: int = 100) -> list[Revision]:
        output = self.runner.run_text(
            ["log", "--xml", "-v", "-l", str(limit)]
        )

        return parse_log_xml(output)

    def get_revision(self, revision: int) -> Revision:
        output = self.runner.run_text(
            ["log", "-r", str(revision), "--xml", "-v"]
        )

        revisions = parse_log_xml(output)

        if not revisions:
            raise RuntimeError(f"Revision {revision} was not found.")

        return revisions[0]

    def get_revision_diff(self, revision: int) -> str:
        return self.runner.run_text(
            ["diff", "-c", str(revision)]
        )

    def get_revision_info(self, revision: int) -> str:
        return self.runner.run_text(
            ["log", "-r", str(revision), "-v"]
        )

    def get_file_content(
        self,
        repository_path: str,
        revision: int,
    ) -> bytes:
        file_url = self._build_file_url(repository_path)

        return self.runner.run_bytes(
            ["cat", "-r", str(revision), file_url]
        )

    def get_repository_root_url(self) -> str:
        if self._repository_root_url is not None:
            return self._repository_root_url

        output = self.runner.run_text(
            ["info", "--show-item", "repos-root-url"]
        )

        self._repository_root_url = output.strip()

        return self._repository_root_url

    def _build_file_url(self, repository_path: str) -> str:
        repository_root_url = self.get_repository_root_url()
        normalized_path = repository_path.lstrip("/")

        return f"{repository_root_url}/{normalized_path}"
