from structures.adjacency_list import AdjacencyList
from structures.adjacency_matrix import AdjacencyMatrix
from structures.incidence_matrix import IncidenceMatrix

import tkinter as tk
import pathlib
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

#to generate random graph
import random 


class ExerciseOneTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.graph = None

        self.add_buttons()

    def add_buttons(self):
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=0, column=0, sticky='NSWE')

        load_graph_btn = ttk.Button(btn_frame, text='Wczytaj graf...', command=self.load_graph)
        load_graph_btn.grid(row=0, column=0, columnspan=3)

        adj_list_btn = ttk.Button(btn_frame, text='Konwertuj na listę sąsiedztwa', command=self.convert_to_adj_list)
        adj_list_btn.grid(row=1, column=0)

        adj_matrix_btn = ttk.Button(btn_frame, text='Konwertuj na macierz sąsiedztwa', command=self.convert_to_adj_matrix)
        adj_matrix_btn.grid(row=1, column=1)

        inc_matrix_btn = ttk.Button(btn_frame, text='Konwertuj na macierz incydencji', command=self.convert_to_inc_matrix)
        inc_matrix_btn.grid(row=1, column=2)

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
        except(AttributeError):
            messagebox.showinfo(title='Wykrzyknik!', message='Graf w tej formie został wczytany z pliku!')

    def convert_to_adj_matrix(self):
        try:
            print(self.graph.to_adjacency_matrix())
        except(AttributeError):
            messagebox.showinfo(title='Wykrzyknik!', message='Graf w tej formie został wczytany z pliku!')

    def convert_to_inc_matrix(self):
        try:
            print(self.graph.to_incidence_matrix())
        except(AttributeError):
            messagebox.showinfo(title='Wykrzyknik!', message='Graf w tej formie został wczytany z pliku!')

    # N - wierzcholki
    # L - krawedzie
    def gen_randgraph_NL(self,N,L): 
        temp_matrix = [[0 for q in range(N)]for e in range(N)]
        if L > (N * N-1) //2:
            print("L is too large")
        for i in range(N):
            for j in range(L):
                x = random.randint(0,N-1)
                y = random.randint(0,N-1)
                if temp_matrix[x][y] == 1 or x == y:
                    while temp_matrix[x][y] == 1 or x == y:
                        x = random.randint(0,N-1)
                        y = random.randint(0,N-1)
                    temp_matrix[x][y] = 1
                    temp_matrix[y][x] = 1
                else:
                    temp_matrix[x][y] = 1
                    temp_matrix[y][x] = 1
        return temp_matrix

        # N - wierzcholki 
        # P - prawdopodobienstwo
    def gen_randgraph_NP(self,N,P):
        temp_matrix = [[0 for q in range(N)]for e in range(N)]
        for i in range(N):
            for j in range(i):
                if random.random() < P:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        return temp_matrix