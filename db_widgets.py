import customtkinter as ctk
from tkinter import ttk
from db_utils import fetch_data, fetch_tables


class DBView(ctk.CTkFrame):
    def __init__(self, parent, fetch_data):
        super().__init__(master=parent)
        self.grid(row=0, column=1, sticky="nsew")
        self.fetch_data = fetch_data

        style = ttk.Style()
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b",
                        bordercolor="#2b2b2b",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#666666')])

        self.tree = ttk.Treeview(self, show='headings', style="Treeview")
        self.tree.pack(fill='both', expand=True)

    def show_data(self, records, columns):
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, minwidth=100)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for record in records:
            self.tree.insert('', 'end', values=record)
