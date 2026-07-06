import tkinter as tk



from svn.models import Revision


class ChangedFilesList(tk.Listbox):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, height=8)

    def set_revision(self, revision: Revision) -> None:
        self.delete(0, tk.END)

        for changed_path in revision.changed_paths:
            self.insert(
                tk.END,
                f"{changed_path.action}  {changed_path.path}",
            )
