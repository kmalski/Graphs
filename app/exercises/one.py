from structures.adjacency_list import AdjacencyList
from structures.adjacency_matrix import AdjacencyMatrix
from structures.incidence_matrix import IncidenceMatrix

import tkinter as tk
import numpy as np
import pathlib
import random
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk


class ExerciseOneTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.graph = None

        self.add_menu()

    def add_menu(self):
        menu_frame = ttk.Frame(self)
        menu_frame.grid(row=0, column=0, sticky='NSWE')

        ttk.Button(menu_frame, text='Wczytaj graf...', command=self.load_graph)\
            .grid(row=0, column=0, pady=2, columnspan=2)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=1, column=0, columnspan=2, sticky='EW', pady=5, padx=5)

        ttk.Button(menu_frame, text='Konwertuj na listę sąsiedztwa', command=self.convert_to_adj_list)\
            .grid(row=2, column=0, pady=2, columnspan=2)
        ttk.Button(menu_frame, text='Konwertuj na macierz sąsiedztwa', command=self.convert_to_adj_matrix)\
            .grid(row=3, column=0, pady=2, columnspan=2)
        ttk.Button(menu_frame, text='Konwertuj na macierz incydencji', command=self.convert_to_inc_matrix)\
            .grid(row=4, column=0, pady=2, columnspan=2)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=5, column=0, columnspan=2, sticky='EW', pady=5, padx=5)

        ttk.Label(menu_frame, text='N').grid(row=6, column=0)
        self.verticles_entry_1 = ttk.Entry(menu_frame, width=10)
        self.verticles_entry_1.grid(row=7, column=0, pady=2)
        ttk.Label(menu_frame, text='L').grid(row=6, column=1)
        self.edges_entry = ttk.Entry(menu_frame, width=10)
        self.edges_entry.grid(row=7, column=1, pady=2)
        ttk.Button(menu_frame, text='Generuj', command=self.gen_NL_callback)\
            .grid(row=8, column=0, columnspan=2, pady=2)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=9, column=0, columnspan=2, sticky='EW', pady=5, padx=5)

        ttk.Label(menu_frame, text='N').grid(row=10, column=0)
        self.verticles_entry_2 = ttk.Entry(menu_frame, width=10)
        self.verticles_entry_2.grid(row=11, column=0, pady=2)
        ttk.Label(menu_frame, text='P').grid(row=10, column=1)
        self.prob_entry = ttk.Entry(menu_frame, width=10)
        self.prob_entry.grid(row=11, column=1, pady=2)
        ttk.Button(menu_frame, text='Generuj', command=self.gen_NP_callback)\
            .grid(row=12, column=0, columnspan=2, pady=2)

    def gen_NL_callback(self, event=None):
        n = int(self.verticles_entry_1.get())
        l = int(self.edges_entry.get())
        self.graph = self.gen_randgraph_NL(n, l)

    def gen_NP_callback(self, event=None):
        n = int(self.verticles_entry_2.get())
        p = int(self.prob_entry.get())
        self.graph = self.gen_randgraph_NP(n, p)

    def load_graph(self, event=None):
        self.graph = None
        file_path = filedialog.askopenfilename(initialdir='.', title='Wybierz plik', filetypes=[('Pliki grafów', '*.*'),
                                                                                                ('Macierz incydencji', '*.gim'),
                                                                                                ('Macierz sąsiedztwa', '*.gam'),
                                                                                                ('Lista sąsiedztwa', '*.gal')])
        extension = pathlib.Path(file_path).suffix

        if extension == '.gim':                          # incidence matrix
            self.graph = IncidenceMatrix()
            self.graph.from_file(file_path)
        elif extension == '.gam':                        # adjacency matrix
            self.graph = AdjacencyMatrix()
            self.graph.from_file(file_path)
        elif extension == '.gal':                        # adjacency list
            self.graph = AdjacencyList()
            self.graph.from_file(file_path)

    def convert_to_adj_list(self):
        try:
            print(self.graph.to_adjacency_list())
        except AttributeError:
            messagebox.showinfo(title='Wykrzyknik!', message='Graf w tej formie został wczytany z pliku!')

    def convert_to_adj_matrix(self):
        try:
            print(self.graph.to_adjacency_matrix())
        except AttributeError:
            messagebox.showinfo(title='Wykrzyknik!', message='Graf w tej formie został wczytany z pliku!')

    def convert_to_inc_matrix(self):
        try:
            print(self.graph.to_incidence_matrix())
        except AttributeError:
            messagebox.showinfo(title='Wykrzyknik!', message='Graf w tej formie został wczytany z pliku!')

    def gen_randgraph_NL(self, N: int, L: int) -> AdjacencyMatrix:
        adj_matrix = np.zeros((N, N), int)

        if L > (N * N - 1) // 2:
            messagebox.showinfo(title='Wykrzyknik!', message='Ilość krawędzi jest zbyt duża!')
            return adj_matrix

        tmp = 0
        while tmp < L:
            x = random.randint(0, N - 1)
            y = random.randint(0, N - 1)
            if x != y and adj_matrix[x][y] != 1:
                adj_matrix[x][y] = 1
                adj_matrix[y][x] = 1
                tmp += 1
        return adj_matrix

        # TODO: sprawdzic czy wygenerowany graf może zostać poprawnie stworzony
    def gen_randgraph_NP(self, N: int, P: float) -> AdjacencyMatrix:
        adj_matrix = np.zeros((N, N))
        for i in range(N):
            for j in range(i):
                if random.random() < P:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        return adj_matrix
