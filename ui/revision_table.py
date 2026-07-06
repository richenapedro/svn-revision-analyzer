import tkinter as tk
from collections.abc import Callable

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH

from svn.models import Revision


class RevisionTable(ttk.Treeview):
    def __init__(
        self,
        parent: tk.Widget,
        on_select: Callable[[Revision], None],
    ) -> None:
        columns = ("revision", "author", "date", "message")

        super().__init__(
            parent,
            columns=columns,
            show="headings",
            height=15,
        )

        self._revisions: list[Revision] = []
        self._on_select = on_select

        self._configure_columns()
        self.bind("<<TreeviewSelect>>", self._handle_selection)

    def set_revisions(self, revisions: list[Revision]) -> None:
        self._revisions = revisions

        self.delete(*self.get_children())

        for revision in revisions:
            self.insert(
                "",
                "end",
                values=(
                    revision.revision,
                    revision.author,
                    revision.date[:19].replace("T", " "),
                    revision.message.replace("\n", " ")[:200],
                ),
            )

    def _configure_columns(self) -> None:
        self.heading("revision", text="Rev")
        self.heading("author", text="Autor")
        self.heading("date", text="Data")
        self.heading("message", text="Mensagem")

        self.column("revision", width=80, anchor="center")
        self.column("author", width=130)
        self.column("date", width=160)
        self.column("message", width=600)

    def _handle_selection(self, _event: tk.Event) -> None:
        selected_items = self.selection()

        if not selected_items:
            return

        selected_item = selected_items[0]
        values = self.item(selected_item, "values")

        if not values:
            return

        selected_revision_number = int(values[0])

        selected_revision = next(
            (
                revision
                for revision in self._revisions
                if revision.revision == selected_revision_number
            ),
            None,
        )

        if selected_revision is None:
            return

        self._on_select(selected_revision)
