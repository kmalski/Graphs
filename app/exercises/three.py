import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import utils.draw
import utils.graph_utils
import random
from utils.tkinter import ResizingSquareCanvas
from utils.tkinter import ScrollableFrame

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

        self.add_canvas()

    def add_menu(self):
        menu_frame = ttk.Frame(self)
        menu_frame.grid(row=0, column=0, sticky='N', padx=10, pady=10)

        ttk.Label(menu_frame, text='Liczba wierzchołków').grid(row=0, column=0)

        self.nodes_entry = ttk.Entry(menu_frame, width=30)
        self.nodes_entry.grid(row=1, column=0, pady=3)

        rand_button = ttk.Button(menu_frame, width=30, text='Generuj spójny graf ważony', command=self.generate_graph)
        rand_button.grid(row=2, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=3, column=0, columnspan=2, sticky='EW', pady=15)

        ttk.Label(menu_frame, text='Wierzchołek startowy').grid(row=4, column=0)

        self.dijkstra_entry = ttk.Entry(menu_frame, width=30)
        self.dijkstra_entry.grid(row=5, column=0, pady=3)

        dijkstra_button = ttk.Button(menu_frame, width=30, text='Szukaj najkrótszych ścieżek', command=self.initiate_protocol_dijkstra)
        dijkstra_button.grid(row=6, column=0, pady=3)

        
    def add_canvas(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=2, sticky='NSWE')
        frame.grid_propagate(False)

        self.canvas = ResizingSquareCanvas(frame, width=1, height=1)
        self.canvas.grid(row=0, column=0)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def draw_graph(self):
        if self.graph is not None:
            utils.draw.draw_graph_with_weights(self.canvas, self.graph)

    def generate_graph(self):
        try:
            n = int(self.nodes_entry.get())
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!', message='Liczba wierzchołków musi być liczbą naturalną!')
            return

        if n < 0:
            messagebox.showinfo(title='Wykrzyknik!', message='Liczba wierzchołków nie może być ujemna!')
            return

        while True:
            adj_matrix = utils.graph_utils.gen_randgraph_NP(n, 0.5)
            edges = adj_matrix.get_number_of_edges()
            weights = [random.randint(1, 10) for _ in range(edges)]

            self.graph = adj_matrix.to_adjacency_list_with_weights(weights)

            if self.graph.is_connected():
                break

        self.draw_graph()

    def initiate_protocol_dijkstra(self): 
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        try:
            vertex = int(self.dijkstra_entry.get())
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!', message='Wierzchołek musi być liczbą naturalną!')
            return

        if not self.graph.is_vertex(vertex):
            messagebox.showinfo(title='Wykrzyknik!', message='We wprowadzonym grafie nie ma takiego wierzchołka!')
            return

        #TODO pretty display
        res_string = self.graph.find_shortest_paths(vertex)
        print(res_string)
