import utils.draw
import utils.graph_utils
from exercises.base import BaseTab

import random
import tkinter as tk
import numpy as np
from tkinter import ttk, messagebox


class ExerciseThreeTab(BaseTab):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.grid_columnconfigure(0, weight=0)  # menu
        self.grid_columnconfigure(1, weight=0)  # separator
        self.grid_columnconfigure(2, weight=2)  # text results
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

        ttk.Label(menu_frame, text='Liczba wierzchołków').grid(row=0, column=0)

        self.nodes_entry = ttk.Entry(menu_frame, width=30)
        self.nodes_entry.grid(row=1, column=0, pady=3)

        rand_button = ttk.Button(menu_frame, width=30, text='Generuj spójny graf ważony', command=self.generate_graph)
        rand_button.grid(row=2, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=3, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 2 ###########################

        ttk.Label(menu_frame, text='Wierzchołek początkowy').grid(row=4, column=0)

        self.dijkstra_entry = ttk.Entry(menu_frame, width=30)
        self.dijkstra_entry.grid(row=5, column=0, pady=3)

        dijkstra_button = ttk.Button(menu_frame, width=30, text='Szukaj najkrótszych ścieżek', command=self.display_shortest_paths)
        dijkstra_button.grid(row=6, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=7, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 3 ###########################

        dist_matrix_button = ttk.Button(menu_frame, width=30, text='Oblicz macierz odległości', command=self.display_distance_matrix)
        dist_matrix_button.grid(row=8, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=9, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 4 ###########################

        graph_center_button = ttk.Button(menu_frame, width=30, text='Wyznacz centrum grafu', command=self.display_graph_center)
        graph_center_button.grid(row=10, column=0, pady=3)

        minimax_center_button = ttk.Button(menu_frame, width=30, text='Wyznacz centrum minimax', command=self.display_minimax_center)
        minimax_center_button.grid(row=11, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=12, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 5 ###########################

        prim_button = ttk.Button(menu_frame, width=30, text='Minimalne drzewo rozpinające', command=self.display_minimal_tree)
        prim_button.grid(row=16, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=17, column=0, columnspan=2, sticky='EW', pady=15)

    def draw_graph(self, center_indices=None, minimal_tree=None):
        if self.graph is not None:
            utils.draw.draw_graph_with_weights(self.canvas, self.graph, center_indices, minimal_tree)

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
            adj_matrix = utils.graph_utils.gen_rand_graph_NP(n, 0.5)
            edges = adj_matrix.get_number_of_edges()
            weights = [random.randint(1, 10) for _ in range(edges)]

            self.graph = adj_matrix.to_weighted_adjacency_list(weights)

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

        distance, previous = self.graph.find_shortest_paths(first_vertex)

        res_string = f'START: {first_vertex}'

        for index in sorted(self.graph.get_vertices()):
            res_string += f'\nwaga({index}) = {distance[index]} \t ==>  ['
            trail = [index]

            while previous[index] is not None:
                trail.append(previous[index])
                index = previous[index]

            res_string += ', '.join(map(lambda v: str(v), reversed(trail)))
            res_string += ']'

        self.result.show_normal(res_string)

    def display_distance_matrix(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        dist_matrix = self.graph.calculate_distance_matrix()

        # TODO make equal spaces between elements of array (like in print)
        with np.printoptions(threshold=2500, linewidth=np.inf, formatter={'all': '{0:>3d}'.format}):
            # print(str(dist_matrix).replace('[', ' ').replace(']', ' '))
            self.result.show_normal(str(dist_matrix).replace('[', ' ').replace(']', ' '))

    def display_graph_center(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        graph_center = self.graph.find_graph_center()
        res_string = ', '.join([str(center) for center in graph_center.tolist()])
        self.result.show_normal(f'Centrum grafu: {res_string}')
        self.draw_graph(graph_center)

    def display_minimax_center(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        minimax_center = self.graph.find_minimax_center()
        res_string = ', '.join([str(center) for center in minimax_center.tolist()])
        self.result.show_normal(f'Centrum minimax: {res_string}')
        self.draw_graph(minimax_center)

    def display_minimal_tree(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        minimal_tree = self.graph.find_minimal_tree()
        self.draw_graph(minimal_tree=minimal_tree)
