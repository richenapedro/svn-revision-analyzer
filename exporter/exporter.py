from pathlib import Path

from exporter.file_exporter import FileExporter
from exporter.workspace import ExportWorkspace
from exporter.zip_builder import ZipBuilder
from svn.models import ChangedPath, Revision
from svn.svn_client import SvnClient


class RevisionExporter:
    def __init__(self, svn_client: SvnClient, output_dir: Path) -> None:
        self.svn_client = svn_client
        self.output_dir = output_dir

    def export(self, revision: Revision) -> Path:
        workspace = ExportWorkspace(
            output_dir=self.output_dir,
            revision=revision.revision,
        )

        workspace.prepare()

        try:
            self._export_revision_info(revision, workspace)
            self._export_diff(revision, workspace)
            self._export_changed_files(revision, workspace)

            zip_path = self.output_dir / f"Revision_{revision.revision}.zip"
            return ZipBuilder.build_zip(workspace.root_dir, zip_path)
        finally:
            workspace.cleanup()

    def _export_revision_info(
        self,
        revision: Revision,
        workspace: ExportWorkspace,
    ) -> None:
        content = self.svn_client.get_revision_info(revision.revision)
        FileExporter.write_text(workspace.info_file, content)

    def _export_diff(
        self,
        revision: Revision,
        workspace: ExportWorkspace,
    ) -> None:
        content = self.svn_client.get_revision_diff(revision.revision)
        FileExporter.write_text(workspace.diff_file, content)

    def _export_changed_files(
        self,
        revision: Revision,
        workspace: ExportWorkspace,
    ) -> None:
        for changed_path in revision.changed_paths:
            self._export_before_file(revision, changed_path, workspace)
            self._export_after_file(revision, changed_path, workspace)

    def _export_before_file(
        self,
        revision: Revision,
        changed_path: ChangedPath,
        workspace: ExportWorkspace,
    ) -> None:
        if not changed_path.exists_before:
            return

        content = self.svn_client.get_file_content(
            repository_path=changed_path.path,
            revision=revision.revision - 1,
        )

        target_path = workspace.before_dir / changed_path.relative_path
        FileExporter.write_bytes(target_path, content)

    def _export_after_file(
        self,
        revision: Revision,
        changed_path: ChangedPath,
        workspace: ExportWorkspace,
    ) -> None:
        if not changed_path.exists_after:
            return

        content = self.svn_client.get_file_content(
            repository_path=changed_path.path,
            revision=revision.revision,
        )

        target_path = workspace.after_dir / changed_path.relative_path
        FileExporter.write_bytes(target_path, content)
