import tkinter as tk
from tkinter import ttk

class LogView:
    """Dialog to display user action logs."""
    def __init__(self, parent, data_storage):
        self.parent = parent
        self.ds = data_storage
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Action Logs")
        self.dialog.geometry("600x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self._build()

    def _build(self):
        cols = ("timestamp", "user", "action")
        tree = ttk.Treeview(self.dialog, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.title())
            tree.column(c, width=200 if c=="action" else 100, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)

        for ts, user, act in self.ds.load_logs():
            tree.insert("", tk.END, values=(ts, user, act))

        ttk.Button(self.dialog, text="Close", command=self.dialog.destroy).pack(pady=10)
