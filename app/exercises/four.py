import utils.draw
import utils.graph_utils
from exercises.base import BaseTab
from structures.adjacency_list import AdjacencyList, DirectedAdjacencyList
from structures.weighted_adjacency_list import WeightedDirectedAdjacencyList

import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict


class ExerciseFourTab(BaseTab):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.grid_columnconfigure(0, weight=0)  # menu
        self.grid_columnconfigure(1, weight=0)  # separator
        self.grid_columnconfigure(2, weight=2)  # text frame
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

        gen_np_frame = ttk.Frame(menu_frame)
        gen_np_frame.grid(row=0, column=0)

        ttk.Label(gen_np_frame, text='N').grid(row=0, column=0)
        self.verticles_entry = ttk.Entry(gen_np_frame, width=10)
        self.verticles_entry.grid(row=1, column=0, pady=2, padx=2)

        ttk.Label(gen_np_frame, text='P').grid(row=0, column=1)
        self.prob_entry = ttk.Entry(gen_np_frame, width=10)
        self.prob_entry.grid(row=1, column=1, pady=2, padx=2)

        ttk.Button(gen_np_frame, text='Generuj', width=15, command=self.gen_NP)\
            .grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=1, column=0, sticky='EW', pady=15)

        ########################### 2 ###########################

        comp_button = ttk.Button(menu_frame, width=30, text='Wyznacz silne spójne składowe', command=self.find_components)
        comp_button.grid(row=2, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=3, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 3 ###########################

        comp_button = ttk.Button(menu_frame, width=30, text='Wylosuj wagi', command=self.add_random_weights)
        comp_button.grid(row=4, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=5, column=0, columnspan=2, sticky='EW', pady=15)

    def draw_graph(self):
        if self.graph is not None:
            if isinstance(self.graph, WeightedDirectedAdjacencyList):
                utils.draw.draw_directed_graph_with_weights(self.canvas, self.graph)
            else:
                utils.draw.draw_directed_graph(self.canvas, self.graph)

    def gen_NP(self, event=None):
        try:
            n = int(self.verticles_entry.get())
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

        self.graph = utils.graph_utils.gen_rand_digraph_NP(n, p).to_directed_adjacency_list()
        self.draw_graph()
        self.print_graph()

    def find_components(self, event=None):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        graph = self.graph
        if not isinstance(self.graph, DirectedAdjacencyList):
            graph = self.graph.to_directed_adjacency_list()

        components = graph.find_components()
        grouped_comp = defaultdict(list)
        for v, nr in components.items():
            grouped_comp[nr].append(v)
        grouped_comp = dict(sorted(grouped_comp.items()))

        res_string = 'Silnie spójne składowe\n'
        for comp_nr, vertices in grouped_comp.items():
            res_string += f'{comp_nr}: {vertices}\n'

        self.result.show_normal(res_string)
        utils.draw.draw_directed_graph(self.canvas, graph, components)

    def add_random_weights(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        if not isinstance(self.graph, WeightedDirectedAdjacencyList):
            self.graph = WeightedDirectedAdjacencyList.from_directed_adj_list(self.graph, -5, 10)
        else: 
            self.graph.set_random_weights(-5, 10)

        self.draw_graph()
        self.print_graph()

