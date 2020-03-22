import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ExerciseThreeTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.graph = None

        self.grid_columnconfigure(0, weight=0)  # menu
        self.grid_columnconfigure(1, weight=0)  # separator
        self.grid_columnconfigure(2, weight=2)  # canvas

        self.grid_rowconfigure(0, weight=1)

        self.add_menu()

        ttk.Separator(self, orient='vertical')\
            .grid(row=0, column=1, pady=5, sticky='NS')

    def add_menu(self):
        menu_frame = ttk.Frame(self)
        menu_frame.grid(row=0, column=0, sticky='N', padx=10, pady=10)

        ttk.Label(menu_frame, text='Liczba wierzchołków').grid(row=0, column=0)

        self.sequence_entry = ttk.Entry(menu_frame, width=55)
        self.sequence_entry.grid(row=1, column=0, pady=3)

        sequence_button = ttk.Button(menu_frame, width=30, text='Generuj spójny graf ważony', command=self.generate_graph)
        sequence_button.grid(row=2, column=0, pady=3)

    def generate_graph(self):
        pass