from pathlib import Path

from svn.svn_client import SvnClient


client = SvnClient(Path(r"C:\_Projekte\TNC7_Projekt"))

revision = 1281

print(client.get_revision_info_text(revision))
print(client.get_revision_diff(revision)[:1000])
