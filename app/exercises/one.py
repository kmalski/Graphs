from structures.adjacency_list import AdjacencyList
from structures.adjacency_matrix import AdjacencyMatrix
from structures.incidence_matrix import IncidenceMatrix

import tkinter as tk
import pathlib
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from math import cos, sin, pi


class ExerciseOneTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.graph = None

        self.add_buttons()
        self.add_canvas()

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

        draw_graph_btn = ttk.Button(btn_frame, text='Rysuj graf', command=self.draw_graph)
        draw_graph_btn.grid(row=1, column=3)

    def add_canvas(self):
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.grid(row=2, column=0)

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