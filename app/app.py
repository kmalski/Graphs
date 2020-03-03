from exercises.one import ExerciseOneTab
from exercises.two import ExerciseTwoTab
from structures.adjacency_list import AdjacencyList
from structures.adjacency_matrix import AdjacencyMatrix
from structures.incidence_matrix import IncidenceMatrix

import tkinter as tk
import pathlib
from tkinter import ttk
from tkinter import filedialog


class App (tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Grafy')
        self.geometry('800x600')

        self.screen_state = False

        self.add_menu_bar()
        self.add_tabs()

        self.bind('<F11>', self.toggle_fullscreen)
        self.bind('<Escape>', self.end_fullscreen)

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
        file_path = filedialog.askopenfilename(initialdir='.', title='Wybierz plik', filetypes=[('Pliki grafów', '*.*'),
                                                                                                ('Macierz incydencji', '*.gim'),
                                                                                                ('Macierz sąsiedztwa', '*.gam'),
                                                                                                ('Lista sąsiedztwa', '*.gal')])
        with open(file_path) as file:
            extension = pathlib.Path(file_path).suffix

            if extension == '.gim':                          # incidence matrix
                self.graph = IncidenceMatrix(file_path)
                print(self.graph)
            elif extension == '.gam':                        # adjacency matrix
                self.graph = AdjacencyMatrix(file_path)
                print(self.graph)
            elif extension == '.gal':                        # adjacency list
                self.graph = AdjacencyList()
                self.graph.from_string(file.read())
                print(self.graph)

    def toggle_fullscreen(self, event=None):
        self.screen_state = not self.screen_state
        if self.screen_state:
            self.state('zoomed')
        else:
            self.state('normal')

    def end_fullscreen(self, event=None):
        self.screen_state = False
        self.state('normal')


if (__name__ == '__main__'):
    app = App()
    app.mainloop()
