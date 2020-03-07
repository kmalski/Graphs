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
from math import cos, sin, pi


class ExerciseOneTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.graph = None

        self.add_canvas()
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

        ttk.Separator(menu_frame, orient='vertical')\
            .grid(row=0, column=2, rowspan=13, sticky='NS', pady=5, padx=5)

        self.graph_representation = ttk.Label(menu_frame, font=("Helvetica", 16))
        self.graph_representation.grid(row=0, column=3, rowspan=13)

    def add_canvas(self):
        self.canvas = tk.Canvas(self, width=350, height=350)
        self.canvas.grid(row=0, column=4)

    def gen_NL_callback(self, event=None):
        n = int(self.verticles_entry_1.get())
        l = int(self.edges_entry.get())
        self.graph = self.gen_randgraph_NL(n, l)

    def gen_NP_callback(self, event=None):
        n = int(self.verticles_entry_2.get())
        p = float(self.prob_entry.get())
        self.graph = self.gen_randgraph_NP(n, p)

        draw_graph_btn = ttk.Button(btn_frame, text='Rysuj graf', command=self.draw_graph)
        draw_graph_btn.grid(row=1, column=3)

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
            self.graph_representation['text'] = str(self.graph).replace('[', ' ').replace(']', ' ')
        elif extension == '.gam':                        # adjacency matrix
            self.graph = AdjacencyMatrix()
            self.graph.from_file(file_path)
            self.graph_representation['text'] = str(self.graph).replace('[', ' ').replace(']', ' ')
        elif extension == '.gal':                        # adjacency list
            self.graph = AdjacencyList()
            self.graph.from_file(file_path)
            self.graph_representation['text'] = str(self.graph)
        self.draw_graph()

    def convert_to_adj_list(self):
        if hasattr(self.graph, 'to_adjacency_list'):
            self.graph_representation['text'] = str(self.graph.to_adjacency_list())
        else:
            self.graph_representation['text'] = str(self.graph)

    def convert_to_adj_matrix(self):
        if hasattr(self.graph, 'to_adjacency_matrix'):
            self.graph_representation['text'] = str(self.graph.to_adjacency_matrix()).replace('[', ' ').replace(']', ' ')
        else:
            self.graph_representation['text'] = str(self.graph).replace('[', ' ').replace(']', ' ')

    def convert_to_inc_matrix(self):
        if hasattr(self.graph, 'to_incidence_matrix'):
            self.graph_representation['text'] = str(self.graph.to_incidence_matrix()).replace('[', ' ').replace(']', ' ')
        else:
            self.graph_representation['text'] = str(self.graph).replace('[', ' ').replace(']', ' ')

    def gen_randgraph_NL(self, N: int, L: int) -> AdjacencyMatrix:
        matrix = np.zeros((N, N), int)

        if L > (N * N - 1) // 2:
            messagebox.showinfo(title='Wykrzyknik!', message='Ilość krawędzi jest zbyt duża!')
            return matrix

        tmp = 0
        while tmp < L:
            x = random.randint(0, N - 1)
            y = random.randint(0, N - 1)
            if x != y and matrix[x][y] != 1:
                matrix[x][y] = 1
                matrix[y][x] = 1
                tmp += 1

        adj_matrix = AdjacencyMatrix()
        adj_matrix.from_matrix(matrix)
        return adj_matrix

        # TODO: sprawdzic czy wygenerowany graf może zostać poprawnie stworzony
    def gen_randgraph_NP(self, N: int, P: float) -> AdjacencyMatrix:
        matrix = np.zeros((N, N))
        for i in range(N):
            for j in range(i):
                if random.random() < P:
                    matrix[i][j] = 1
                    matrix[j][i] = 1

        adj_matrix = AdjacencyMatrix()
        adj_matrix.from_matrix(matrix)
        return adj_matrix

    def create_circle(self, canvasName, x, y, r):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1, fill="white")

    def draw_graph(self):
        if not self.graph:
            messagebox.showinfo(title='Wykrzyknik!', message='Musisz najpierw wczytać jakiś graf!')
        
        self.canvas.delete("all")

        graph_to_draw = self.graph
        if not isinstance(self.graph, AdjacencyList):
            graph_to_draw = self.graph.to_adjacency_list()

        n = len(graph_to_draw.graph)
        center = (self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2) #needed to convert from cartesian to screen coordinates
        r = min(center) / 1.5

        diff_angle = 2 * pi / n
        for i in range(n):
            #calculate node coordinates
            angle = diff_angle * i
            x = center[0] + r * cos(angle)
            y = center[1] - r * sin(angle)

            #drawing edges
            for neighbour in graph_to_draw.graph[i]:
                if neighbour <= i:
                    continue
                neighbour_angle = diff_angle * neighbour
                neighbour_x = center[0] + r * cos(neighbour_angle)
                neighbour_y = center[1] - r * sin(neighbour_angle)
                self.canvas.create_line(x, y, neighbour_x, neighbour_y)

            self.create_circle(self.canvas, x, y, r * 0.2)
            self.canvas.create_text(x, y, text=str(i))