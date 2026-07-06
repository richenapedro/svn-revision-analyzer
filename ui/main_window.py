from pathlib import Path
import tkinter as tk
from tkinter import filedialog

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, X, LEFT


class MainWindow:
    def __init__(self) -> None:
        self.root = ttk.Window(
            title="SVN Revision Analyzer",
            themename="flatly",
            size=(1000, 700),
        )

        self.project_path_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pronto.")

        self._build_layout()

    def run(self) -> None:
        self.root.mainloop()

    def _build_layout(self) -> None:
        main_frame = ttk.Frame(self.root, padding=12)
        main_frame.pack(fill=BOTH, expand=True)

        self._build_project_selector(main_frame)
        self._build_revision_area(main_frame)
        self._build_changed_files_area(main_frame)
        self._build_actions(main_frame)
        self._build_status_bar(main_frame)

    def _build_project_selector(self, parent: ttk.Frame) -> None:
        frame = ttk.Labelframe(parent, text="Projeto SVN", padding=10)
        frame.pack(fill=X, pady=(0, 10))

        entry = ttk.Entry(frame, textvariable=self.project_path_var)
        entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 8))

        browse_button = ttk.Button(
            frame,
            text="Selecionar...",
            command=self._select_project_folder,
        )
        browse_button.pack(side=LEFT)

        load_button = ttk.Button(
            frame,
            text="Carregar Revisões",
            bootstyle="primary",
            command=self._load_revisions,
        )
        load_button.pack(side=LEFT, padx=(8, 0))

    def _build_revision_area(self, parent: ttk.Frame) -> None:
        frame = ttk.Labelframe(parent, text="Revisões", padding=10)
        frame.pack(fill=BOTH, expand=True, pady=(0, 10))

        columns = ("revision", "author", "date", "message")

        self.revision_table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=15,
        )

        self.revision_table.heading("revision", text="Rev")
        self.revision_table.heading("author", text="Autor")
        self.revision_table.heading("date", text="Data")
        self.revision_table.heading("message", text="Mensagem")

        self.revision_table.column("revision", width=80, anchor="center")
        self.revision_table.column("author", width=130)
        self.revision_table.column("date", width=160)
        self.revision_table.column("message", width=600)

        self.revision_table.pack(fill=BOTH, expand=True)

    def _build_changed_files_area(self, parent: ttk.Frame) -> None:
        frame = ttk.Labelframe(parent, text="Arquivos alterados", padding=10)
        frame.pack(fill=BOTH, expand=True, pady=(0, 10))

        self.changed_files_list = tk.Listbox(frame, height=8)
        self.changed_files_list.pack(fill=BOTH, expand=True)

    def _build_actions(self, parent: ttk.Frame) -> None:
        frame = ttk.Frame(parent)
        frame.pack(fill=X, pady=(0, 10))

        export_button = ttk.Button(
            frame,
            text="Exportar Revisão",
            bootstyle="success",
            command=self._export_revision,
        )
        export_button.pack(side=LEFT)

    def _build_status_bar(self, parent: ttk.Frame) -> None:
        status_label = ttk.Label(
            parent,
            textvariable=self.status_var,
            anchor="w",
            bootstyle="secondary",
        )
        status_label.pack(fill=X)

    def _select_project_folder(self) -> None:
        selected_path = filedialog.askdirectory(
            title="Selecionar pasta do projeto SVN"
        )

        if not selected_path:
            return

        self.project_path_var.set(str(Path(selected_path)))
        self.status_var.set("Pasta SVN selecionada.")

    def _load_revisions(self) -> None:
        project_path = self.project_path_var.get()

        if not project_path:
            self.status_var.set("Selecione uma pasta SVN primeiro.")
            return

        self.status_var.set("Carregar revisões ainda será implementado.")

    def _export_revision(self) -> None:
        self.status_var.set("Exportação ainda será implementada.")
