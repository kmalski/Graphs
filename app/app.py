from exercises.one import ExerciseOneTab
from exercises.two import ExerciseTwoTab
from structures.adjacency_list import AdjacencyList
from structures.adjacency_matrix import AdjacencyMatrix
from structures.incidental_matrix import IncidentalMatrix

import tkinter as tk
import os.path
from tkinter import ttk
from tkinter import filedialog


class App (tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Grafy')
        self.geometry('1080x720')

        self.add_menu_bar()
        self.add_tabs()

    def add_tabs(self):
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill='both')

        exercise_1 = ExerciseOneTab(self)
        self.tabs.add(exercise_1, text='Zadanie 1')

        exercise_2 = ExerciseTwoTab(self)
        self.tabs.add(exercise_2, text='Zadanie 2')

    def add_menu_bar(self):
        self.menu_bar = tk.Menu(self)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label='Wczytaj graf...', command=self.load_graph)
        self.menu_bar.add_cascade(label='Plik', menu=file_menu)

        self.config(menu=self.menu_bar)

    def load_graph(self, event=None):
        self.graph = None
        file_path = filedialog.askopenfilename(initialdir='/', title='Wybierz plik', filetypes=[('Pliki grafów', '*.*'),
                                                                                                ('Macierz incydencji', '*.gim'),
                                                                                                ('Macierz sąsiedztwa', '*.gam'),
                                                                                                ('Lista sąsiedztwa', '*.gal')])
        with open(file_path) as file:
            extension = os.path.basename(file_path)
            if extension == 'gim':      # incidence matrix
                self.graph = IncidentalMatrix(file.read())
            elif extension == 'gam':    # adjacency matrix
                self.graph = AdjacencyMatrix(file.read())
            elif extension == 'gal':    # adjacency list
                self.graph = AdjacencyList(file.read())


if (__name__ == '__main__'):
    app = App()
    app.mainloop()
