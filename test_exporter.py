from pathlib import Path

from exporter.exporter import RevisionExporter
from svn.svn_client import SvnClient


project_path = Path(r"C:\_Projekte\TNC7_Projekt")
output_dir = Path("output")

revision_number = 1281

client = SvnClient(project_path)
revision = client.get_revision(revision_number)

exporter = RevisionExporter(
    svn_client=client,
    output_dir=output_dir,
)

zip_path = exporter.export(revision)

print(zip_path)
