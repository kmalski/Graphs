import utils.draw
import utils.graph_utils
from exercises.base import BaseTab
from structures.adjacency_list import AdjacencyList
from structures.adjacency_matrix import AdjacencyMatrix
from structures.incidence_matrix import IncidenceMatrix
from utils.tkinter import ResizingSquareCanvas, ScrollableFrame

import pathlib
import random
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class ExerciseOneTab(BaseTab):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        np.set_printoptions(threshold=2500, linewidth=np.inf)

        self.grid_columnconfigure(0, weight=0)  # menu
        self.grid_columnconfigure(1, weight=0)  # separator
        self.grid_columnconfigure(2, weight=2)  # graph text representation
        self.grid_columnconfigure(3, weight=0)  # separator
        self.grid_columnconfigure(4, weight=2)  # canvas

        self.grid_rowconfigure(0, weight=1)

        self.add_menu()
        self.add_vertical_separator(column=1)
        self.add_text_frame(row=0, column=2)
        self.add_vertical_separator(column=3)
        self.add_canvas(row=0, column=4)

    def add_menu(self):
        menu_frame = ttk.Frame(self)
        menu_frame.grid(row=0, column=0, sticky='N', padx=10, pady=10)

        ########################### 1 ###########################

        ttk.Button(menu_frame, text='Wczytaj graf...', width=30, command=self.load_graph)\
            .grid(row=0, column=0, pady=3, columnspan=2)
        ttk.Button(menu_frame, text='Zapisz graf...', width=30, command=self.save_graph)\
            .grid(row=1, column=0, pady=3, columnspan=2)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=2, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 2 ###########################

        ttk.Button(menu_frame, text='Konwertuj na listę sąsiedztwa', width=30, command=self.convert_to_adj_list)\
            .grid(row=3, column=0, pady=3, columnspan=2)
        ttk.Button(menu_frame, text='Konwertuj na macierz sąsiedztwa', width=30, command=self.convert_to_adj_matrix)\
            .grid(row=4, column=0, pady=3, columnspan=2)
        ttk.Button(menu_frame, text='Konwertuj na macierz incydencji', width=30, command=self.convert_to_inc_matrix)\
            .grid(row=5, column=0, pady=3, columnspan=2)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=6, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 3 ###########################

        ttk.Label(menu_frame, text='N').grid(row=7, column=0)
        self.verticles_entry_1 = ttk.Entry(menu_frame, width=10)
        self.verticles_entry_1.grid(row=8, column=0, pady=2)

        ttk.Label(menu_frame, text='L').grid(row=7, column=1)
        self.edges_entry = ttk.Entry(menu_frame, width=10)
        self.edges_entry.grid(row=8, column=1, pady=2)

        ttk.Button(menu_frame, text='Generuj', width=15, command=self.gen_NL_callback)\
            .grid(row=9, column=0, columnspan=2, pady=10)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=10, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 4 ###########################

        ttk.Label(menu_frame, text='N').grid(row=11, column=0)
        self.verticles_entry_2 = ttk.Entry(menu_frame, width=10)
        self.verticles_entry_2.grid(row=12, column=0, pady=2)

        ttk.Label(menu_frame, text='P').grid(row=11, column=1)
        self.prob_entry = ttk.Entry(menu_frame, width=10)
        self.prob_entry.grid(row=12, column=1, pady=2)

        ttk.Button(menu_frame, text='Generuj', width=15, command=self.gen_NP_callback)\
            .grid(row=13, column=0, columnspan=2, pady=10)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=14, column=0, columnspan=2, sticky='EW', pady=15)

    def load_graph(self, event=None):
        self.graph = None
        file_path = filedialog.askopenfilename(initialdir='.', title='Wybierz plik', filetypes=[('Pliki grafów', '*.*'),
                                                                                                ('Macierz incydencji', '*.gim'),
                                                                                                ('Macierz sąsiedztwa', '*.gam'),
                                                                                                ('Lista sąsiedztwa', '*.gal')])
        if file_path is None:
            return
        extension = pathlib.Path(file_path).suffix

        if extension == '.gim':
            self.graph = IncidenceMatrix.from_file(file_path)
        elif extension == '.gam':
            self.graph = AdjacencyMatrix.from_file(file_path)
        elif extension == '.gal':
            self.graph = AdjacencyList.from_file(file_path)
        else:
            return

        self.draw_graph()
        self.print_graph()

    def save_graph(self, event=None):
        file_path = filedialog.asksaveasfilename(initialdir=".", title="Wybierz plik", filetypes=[('Pliki grafów', '*.*'),
                                                                                                  ('Macierz incydencji', '*.gim'),
                                                                                                  ('Macierz sąsiedztwa', '*.gam'),
                                                                                                  ('Lista sąsiedztwa', '*.gal')])

        if not file_path or self.graph is None:
            return
        extension = pathlib.Path(file_path).suffix

        if extension == '.gim' and hasattr(self.graph, 'to_incidence_matrix'):
            self.graph.to_incidence_matrix().to_file(file_path)
        elif extension == '.gam' and hasattr(self.graph, 'to_adjacency_matrix'):
            self.graph.to_adjacency_matrix().to_file(file_path)
        elif extension == '.gal' and hasattr(self.graph, 'to_adjacency_list'):
            self.graph.to_adjacency_list().to_file(file_path)
        elif extension in ['.gim', '.gam', '.gal']:
            self.graph.to_file(file_path)
        else:
            self.graph.to_file(file_path, add_extension=True)

    def draw_graph(self):
        if self.graph is not None:
            utils.draw.draw_graph(self.canvas, self.graph)

    def convert_to_adj_list(self):
        if hasattr(self.graph, 'to_adjacency_list'):
            self.graph = self.graph.to_adjacency_list()
            self.print_graph()

    def convert_to_adj_matrix(self):
        if hasattr(self.graph, 'to_adjacency_matrix'):
            self.graph = self.graph.to_adjacency_matrix()
            self.print_graph()

    def convert_to_inc_matrix(self):
        if hasattr(self.graph, 'to_incidence_matrix'):
            self.graph = self.graph.to_incidence_matrix()
            self.print_graph()

    def gen_NL_callback(self, event=None):
        try:
            n = int(self.verticles_entry_1.get())
            l = int(self.edges_entry.get())
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!', message='Wprowadź prawidłowe dane wejściowe!')
            return

        if l < 0 or n < 0:
            messagebox.showinfo(title='Wykrzyknik!', message='Liczba wierzchołków i liczba krawędzi nie mogą być ujemne!')
            return

        if l > n * (n - 1) // 2:
            messagebox.showinfo(title='Wykrzyknik!', message='Liczba krawędzi jest zbyt duża!')
            return

        self.graph = utils.graph_utils.gen_rand_graph_NL(n, l)
        self.draw_graph()
        self.print_graph()

    def gen_NP_callback(self, event=None):
        try:
            n = int(self.verticles_entry_2.get())
            p = float(self.prob_entry.get())
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!', message='Wprowadź prawidłowe dane wejściowe!')
            return

        if n < 0:
            messagebox.showinfo(title='Wykrzyknik!', message='Liczba wierzchołków nie może być ujemna!')
            return

        if not 0 <= p <= 1:
            messagebox.showinfo(title='Wykrzyknik!', message='Prawdopodobieństwo musi być z przedziału [0, 1]!')
            return

        self.graph = utils.graph_utils.gen_rand_graph_NP(n, p)
        self.draw_graph()
        self.print_graph()
