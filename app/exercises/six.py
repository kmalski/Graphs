from exercises.base import BaseTab
from utils.graph_utils import generate_pagerank_graph
from structures.adjacency_list import DirectedAdjacencyList

import networkx as nx
import tkinter as tk
import random
from tkinter import ttk, messagebox


class ExerciseSixTab(BaseTab):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.grid_columnconfigure(0, weight=0)  # menu
        self.grid_columnconfigure(1, weight=0)  # separator
        self.grid_columnconfigure(2, weight=4)  # text frame
        self.grid_columnconfigure(3, weight=0)  # separator
        self.grid_columnconfigure(4, weight=2)  # canvas

        self.grid_rowconfigure(0, weight=1)

        self.add_menu()
        self.add_vertical_separator(column=1)
        self.add_text_frame(row=0, column=2)
        self.add_vertical_separator(column=3)
        self.add_canvas(row=0, column=4, for_networkX=True)

    def add_menu(self):
        menu_frame = ttk.Frame(self)
        menu_frame.grid(row=0, column=0, sticky='N', padx=10, pady=10)

        ########################### 1 ###########################

        ttk.Label(menu_frame, text='N').grid(row=0, column=0)
        self.vertices_entry = ttk.Entry(menu_frame, width=10)
        self.vertices_entry.grid(row=1, column=0, pady=2, padx=2)

        ttk.Button(menu_frame, text='Generuj losowy graf', width=30, command=self.generate_graph)\
            .grid(row=2, column=0, columnspan=1, pady=10)

        ttk.Label(menu_frame, text='Wyznacz wartości PageRank:').grid(row=3, column=0)

        ttk.Button(menu_frame, text='Metodą błądzenia przypadkowego', width=30, command=self.random_walk_pagerank)\
            .grid(row=4, column=0, columnspan=1, pady=3)
    
        ttk.Button(menu_frame, text='Metodą iteracyjną', width=30, command=self.iterative_pagerank)\
            .grid(row=5, column=0, columnspan=1, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=6, column=0, sticky='EW', pady=15)
        
        ########################### 2 ###########################

        ttk.Button(menu_frame, text='Wczytaj plik...', width=30, command=self.load_file)\
            .grid(row=7, column=0, columnspan=2, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=8, column=0, columnspan=2, sticky='EW', pady=15)

    def generate_graph(self):
        try:
            n = int(self.vertices_entry.get())
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!', message='Wprowadź prawidłowe dane wejściowe!')
            return

        if n < 2:
            messagebox.showinfo(title='Wykrzyknik!', message='Liczba wierzchołków nie może być mniejsza niż 2!')
            return

        self.graph = generate_pagerank_graph(n)

        self.visualization = self.graph.to_networkX()
        self.axis.clear()

        self.pos = nx.spring_layout(self.visualization)
        nx.draw_networkx(self.visualization, pos=self.pos, ax=self.axis)

        self.canvas.draw()
        self.print_graph()

    def append_pagerank_info(self, pagerank):
        pagerank_string = '\nPageRank:\n'
        for index, pr in sorted(pagerank.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
            pagerank_string += f'{index}: {pr}\n'

        self.append_text(pagerank_string)

    def random_walk_pagerank(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return
        
        pagerank = self.graph.random_walk_pagerank(10000)

        self.print_graph()
        self.append_pagerank_info(pagerank)

    def iterative_pagerank(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        adjacency_matrix = self.graph.to_adjacency_matrix()

        pagerank = adjacency_matrix.iterative_pagerank()

        self.print_graph()
        self.append_pagerank_info(pagerank)

    def load_file(self):
        pass