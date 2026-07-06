from pathlib import Path

from svn.svn_client import SvnClient


client = SvnClient(
    Path(r"C:\SeuProjetoSVN")
)

print(client.is_working_copy())
