import customtkinter as ctk
from menu import Menu
from db_utils import fetch_data
from db_widgets import DBView


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Управління БД Приймальної Комісії")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=6, uniform="a")

        self.menu = Menu(self)
        self.db_view = DBView(self, fetch_data)
        self.db_view.grid(row=0, column=1, sticky="nsew")

        self.mainloop()


App()
