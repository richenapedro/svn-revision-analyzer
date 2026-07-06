from pathlib import Path
import subprocess


class SvnCommandRunner:
    def __init__(self, working_dir: Path) -> None:
        self.working_dir = working_dir

    def run_text(self, args: list[str]) -> str:
        result = subprocess.run(
            ["svn", *args],
            cwd=self.working_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())

        return result.stdout

    def run_bytes(self, args: list[str]) -> bytes:
        result = subprocess.run(
            ["svn", *args],
            cwd=self.working_dir,
            capture_output=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode(errors="replace").strip())

        return result.stdout

    def succeeds(self, args: list[str]) -> bool:
        result = subprocess.run(
            ["svn", *args],
            cwd=self.working_dir,
            capture_output=True,
            text=True,
        )

        return result.returncode == 0
