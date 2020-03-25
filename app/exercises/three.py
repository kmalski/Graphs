import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import utils.draw
import utils.graph_utils
import random
import numpy as np
from utils.tkinter import ResizingSquareCanvas
from utils.tkinter import ScrollableFrame

class ExerciseThreeTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.graph = None

        self.grid_columnconfigure(0, weight=0)  # menu
        self.grid_columnconfigure(1, weight=0)  # separator
        self.grid_columnconfigure(2, weight=2)  # text results
        self.grid_columnconfigure(3, weight=0)  # separator
        self.grid_columnconfigure(4, weight=2)  # canvas

        self.grid_rowconfigure(0, weight=1)

        self.add_menu()
        self.add_vertical_separator(column=1)
        self.add_canvas()
        self.add_vertical_separator(column=3)
        self.add_text_frame()

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

        ttk.Label(menu_frame, text='Wierzchołek początkowy').grid(row=4, column=0)

        self.dijkstra_entry = ttk.Entry(menu_frame, width=30)
        self.dijkstra_entry.grid(row=5, column=0, pady=3)

        dijkstra_button = ttk.Button(menu_frame, width=30, text='Szukaj najkrótszych ścieżek', command=self.display_shortest_paths)
        dijkstra_button.grid(row=6, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=7, column=0, columnspan=2, sticky='EW', pady=15)

        dist_matrix_button = ttk.Button(menu_frame, width=30, text='Oblicz macierz odległości', command=self.display_distance_matrix)
        dist_matrix_button.grid(row=8, column=0, pady=3)
        
        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=9, column=0, columnspan=2, sticky='EW', pady=15)

        graph_center_button = ttk.Button(menu_frame, width=30, text='Wyznacz centrum grafu', command=self.display_graph_center)
        graph_center_button.grid(row=10, column=0, pady=3)
        
        minimax_center_button = ttk.Button(menu_frame, width=30, text='Wyznacz centrum minimax', command=self.display_minimax_center)
        minimax_center_button.grid(row=11, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=12, column=0, columnspan=2, sticky='EW', pady=15)

    def add_canvas(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=4, sticky='NSWE')
        frame.grid_propagate(False)

        self.canvas = ResizingSquareCanvas(frame, width=1, height=1)
        self.canvas.grid(row=0, column=0)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def add_text_frame(self):
        frame = ScrollableFrame(self)
        frame.grid(row=0, column=2, sticky='NSWE')
        frame.grid_propagate(False)

        self.result = ttk.Label(frame.scrollable_frame, font=("Helvetica", 16))
        self.result.grid(row=1, column=0)

        frame.bind_vertical_scroll('<MouseWheel>', self)
        frame.bind_horizontal_scroll('<MouseWheel>', frame.scrollbar_x)

    def clear_text(self):
        self.result['text'] = ''

    def add_vertical_separator(self, column):
        ttk.Separator(self, orient='vertical')\
            .grid(row=0, column=column, pady=5, sticky='NS')

    def draw_graph(self, center=None):
        if self.graph is not None:
            utils.draw.draw_graph_with_weights(self.canvas, self.graph, center)

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

        self.clear_text()
        self.draw_graph()

    def display_shortest_paths(self): 
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        try:
            first_vertex = int(self.dijkstra_entry.get())
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!', message='Numer wierzchołka musi być liczbą naturalną!')
            return

        if not self.graph.has_vertex(first_vertex):
            messagebox.showinfo(title='Wykrzyknik!', message='We wprowadzonym grafie nie ma takiego wierzchołka!')
            return

        weights, previous = self.graph.find_shortest_paths(first_vertex)
        
        res_string = f'START: {first_vertex}'

        for index in sorted(self.graph.get_vertices()):
            res_string += f'\nwaga({index}) = {weights[index]} \t ==>  ['
            trail = [index]
            
            while previous[index] is not None:
                trail.append(previous[index])
                index = previous[index]
            
            res_string += ', '.join(map(lambda v: str(v), reversed(trail)))
            res_string += ']'

        self.result['text'] = res_string

    def display_distance_matrix(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return
        
        dist_matrix = self.graph.calculate_distance_matrix()
        
        #TODO make equal spaces between elements of array (like in print)
        with np.printoptions(threshold=2500, linewidth=np.inf, formatter={'all': '{0:>3d}'.format}):
            # print(str(dist_matrix).replace('[', ' ').replace(']', ' '))
            self.result['text'] = str(dist_matrix).replace('[', ' ').replace(']', ' ')

    def display_graph_center(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        graph_center = self.graph.find_graph_center()
        res_string = ', '.join([str(center) for center in graph_center.tolist()])
        self.result['text'] = f'Centrum grafu: {res_string}'
        self.draw_graph(graph_center)

    def display_minimax_center(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return
        
        minimax_center = self.graph.find_minimax_center()
        res_string = ', '.join([str(center) for center in minimax_center.tolist()])
        self.result['text'] = f'Centrum minimax: {res_string}'
        self.draw_graph(minimax_center)