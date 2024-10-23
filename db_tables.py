import customtkinter as ctk
from tkinter import ttk


class DBTables(ctk.CTkFrame):
    def __init__(self, parent, fetch_tables):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky="ns")
        self.fetch_tables = fetch_tables

        style = ttk.Style()
        style.configure("Tables.Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b",
                        bordercolor="#2b2b2b",
                        borderwidth=0)
        style.map('Tables.Treeview', background=[('selected', '#666666')])

        self.sidebar = ttk.Treeview(self, style="Tables.Treeview", show='tree')
        self.sidebar.pack(fill='y', expand=True)

        self.load_tables()

    def load_tables(self):
        tables = self.fetch_tables()
        if tables is None:
            tables = []
        for table in tables:
            self.sidebar.insert('', 'end', text=table, values=(table,))
