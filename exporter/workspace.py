from pathlib import Path
import shutil


class ExportWorkspace:
    def __init__(self, output_dir: Path, revision: int) -> None:
        self.root_dir = output_dir / f"Revision_{revision}"
        self.before_dir = self.root_dir / "before"
        self.after_dir = self.root_dir / "after"
        self.diff_file = self.root_dir / "diff.patch"
        self.info_file = self.root_dir / "revision_info.txt"

    def prepare(self) -> None:
        if self.root_dir.exists():
            shutil.rmtree(self.root_dir)

        self.before_dir.mkdir(parents=True)
        self.after_dir.mkdir(parents=True)

    def cleanup(self) -> None:
        if self.root_dir.exists():
            shutil.rmtree(self.root_dir)
