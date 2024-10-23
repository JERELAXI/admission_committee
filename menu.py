import customtkinter as ctk
from db_tables import DBTables
from db_utils import fetch_tables, fetch_data
from db_widgets import DBView


class Menu(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky="nsew")

        self.selected_table = None

        self.add("Tables")
        self.add("Sort")
        self.add("Filter")
        self.add("Join")
        self.add("Analyze")
        self.add("Group")

        self.db_tables = DBTables(self.tab('Tables'), fetch_tables)

        self.db_tables.sidebar.bind('<<TreeviewSelect>>', self.on_table_select)

        self.add_sorting_functionality(self.tab('Sort'))
        self.add_range_selection_functionality(self.tab('Filter'))
        self.add_join_functionality(self.tab('Join'))
        self.add_analysis_functionality(self.tab('Analyze'))
        self.add_grouping_functionality(self.tab('Group'))

    def on_table_select(self, event):
        selected_item = self.db_tables.sidebar.selection()[0]
        self.selected_table = self.db_tables.sidebar.item(selected_item,
                                                          'text')
        records, columns = fetch_data(f"SELECT * FROM {self.selected_table}")
        self.master.db_view.show_data(records, columns)

    def add_sorting_functionality(self, tab):
        label = ctk.CTkLabel(tab, text="Поле для сортування:")
        label.grid(row=0, column=0, padx=10, pady=10)
        self.sort_field = ctk.CTkEntry(tab)
        self.sort_field.grid(row=0, column=1, padx=10, pady=10)

        label_order = ctk.CTkLabel(tab, text="Порядок сортування:")
        label_order.grid(row=1, column=0, padx=10, pady=10)
        self.sort_order = ctk.CTkComboBox(tab, values=["ASC", "DESC"])
        self.sort_order.grid(row=1, column=1, padx=10, pady=10)

        sort_button = ctk.CTkButton(tab, text="Сортувати",
                                    command=self.sort_records)
        sort_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def sort_records(self):
        if self.selected_table:
            field = self.sort_field.get()
            order = self.sort_order.get()
            query = f"SELECT * FROM {self.selected_table} ORDER BY {field} {order} LIMIT 10"
            records, columns = fetch_data(query)
            self.master.db_view.show_data(records, columns)

    def add_range_selection_functionality(self, tab):
        label = ctk.CTkLabel(tab, text="Поле для вибірки:")
        label.grid(row=0, column=0, padx=10, pady=10)
        self.range_field = ctk.CTkEntry(tab)
        self.range_field.grid(row=0, column=1, padx=10, pady=10)

        label_min = ctk.CTkLabel(tab, text="Мінімальне значення:")
        label_min.grid(row=1, column=0, padx=10, pady=10)
        self.range_min = ctk.CTkEntry(tab)
        self.range_min.grid(row=1, column=1, padx=10, pady=10)

        label_max = ctk.CTkLabel(tab, text="Максимальне значення:")
        label_max.grid(row=2, column=0, padx=10, pady=10)
        self.range_max = ctk.CTkEntry(tab)
        self.range_max.grid(row=2, column=1, padx=10, pady=10)

        range_button = ctk.CTkButton(tab, text="Вибрати",
                                     command=self.select_range)
        range_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def select_range(self):
        if self.selected_table:
            field = self.range_field.get()
            min_value = self.range_min.get()
            max_value = self.range_max.get()
            query = f"SELECT * FROM {self.selected_table} WHERE {field} BETWEEN {min_value} AND {max_value}"
            records, columns = fetch_data(query)
            self.master.db_view.show_data(records, columns)

    def add_join_functionality(self, tab):
        label_table2 = ctk.CTkLabel(tab, text="Друга таблиця:")
        label_table2.grid(row=0, column=0, padx=10, pady=10)
        self.table2 = ctk.CTkEntry(tab)
        self.table2.grid(row=0, column=1, padx=10, pady=10)

        label_on = ctk.CTkLabel(tab, text="Умова з’єднання:")
        label_on.grid(row=1, column=0, padx=10, pady=10)
        self.join_condition = ctk.CTkEntry(tab)
        self.join_condition.grid(row=1, column=1, padx=10, pady=10)

        join_button = ctk.CTkButton(tab, text="З’єднати",
                                    command=self.join_tables)
        join_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def join_tables(self):
        if self.selected_table:
            table2 = self.table2.get()
            condition = self.join_condition.get()
            if table2 and condition:
                query = (
                    f"SELECT {table2}.*, {self.selected_table}.* "
                    f"FROM {table2} INNER JOIN {self.selected_table} "
                    f"ON {table2}.id = {self.selected_table}.{condition}")
                print(f"Executing query: {query}")
                records, columns = fetch_data(query)
                if records and columns:
                    print(
                        f"Records: {records}")
                    self.master.db_view.show_data(records, columns)
                else:
                    print("Ніяких даних не повернуто із запиту на об'єднання!")
            else:
                print("Будь ласка, надайте другу таблицю та умову об'єднання!")

    def add_analysis_functionality(self, tab):
        label = ctk.CTkLabel(tab, text="Поле для аналізу:")
        label.grid(row=0, column=0, padx=10, pady=10)
        self.analysis_field = ctk.CTkEntry(tab)
        self.analysis_field.grid(row=0, column=1, padx=10, pady=10)

        analysis_button = ctk.CTkButton(tab, text="Аналізувати",
                                        command=self.analyze_data)
        analysis_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def analyze_data(self):
        if self.selected_table:
            field = self.analysis_field.get()
            query = f"SELECT AVG({field}), MAX({field}), MIN({field}) FROM {self.selected_table}"
            records, columns = fetch_data(query)
            self.master.db_view.show_data(records, columns)

    def add_grouping_functionality(self, tab):
        label_group = ctk.CTkLabel(tab, text="Поле для групування:")
        label_group.grid(row=0, column=0, padx=10, pady=10)
        self.group_field = ctk.CTkEntry(tab)
        self.group_field.grid(row=0, column=1, padx=10, pady=10)

        group_button = ctk.CTkButton(tab, text="Групувати",
                                     command=self.group_data)
        group_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def group_data(self):
        if self.selected_table:
            field = self.group_field.get()
            query = f"SELECT {field}, COUNT(*) FROM {self.selected_table} GROUP BY {field}"
            records, columns = fetch_data(query)
            self.master.db_view.show_data(records, columns)
