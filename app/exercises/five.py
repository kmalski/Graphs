from exercises.base import BaseTab
from structures.weighted_adjacency_list import DirectedWeightedAdjacencyList

import math
import networkx as nx
import tkinter as tk
import collections as cs
from tkinter import ttk, messagebox


class ExerciseFiveTab(BaseTab):
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

        ttk.Button(menu_frame, text='Generuj losową sieć przepływową', width=30, command=self.generate_network)\
            .grid(row=2, column=0, columnspan=1, pady=10)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=3, column=0, sticky='EW', pady=15)

        ########################### 2 ###########################

        ttk.Button(menu_frame, text='Wartość maksymalnego przepływu', width=30, command=self.ford_fulkenson)\
            .grid(row=4, column=0, columnspan=2, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=5, column=0, columnspan=2, sticky='EW', pady=15)

    def append_layers_info(self):
        layers_string = '\nWarstwy:\n'
        for layer, vertices in self.layers.items():
            layers_string += f'{layer}: {vertices}\n'

        self.append_text(layers_string)

    def generate_network(self):
        try:
            n = int(self.vertices_entry.get())
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!', message='Wprowadź prawidłowe dane wejściowe!')
            return

        if n < 2:
            messagebox.showinfo(title='Wykrzyknik!', message='Liczba wierzchołków nie może być mniejsza niż 2!')
            return

        self.graph = DirectedWeightedAdjacencyList.init_empty()
        self.layers = self.graph.generate_flow_network(n)

        self.visualization = self.graph.to_networkX()
        self.axis.clear()

        labels = nx.get_edge_attributes(self.visualization, 'weight')
        self.pos = nx.spring_layout(self.visualization)
        nx.draw_networkx(self.visualization, pos=self.pos, ax=self.axis)
        nx.draw_networkx_edge_labels(self.visualization, pos=self.pos, edge_labels=labels, ax=self.axis)

        self.canvas.draw()
        self.print_graph()
        self.append_layers_info()

    def bfs(self, source, target, path, matrix):
        visited = [False for _ in range(len(matrix))]
        visited[source] = True

        q = cs.deque([])
        q.append(source)

        while q:
            u = q.popleft()

            for ind, val in enumerate(matrix[u]):
                if not visited[ind] and val > 0:
                    q.append(ind)
                    visited[ind] = True
                    path[ind] = u

        return visited[target]

    def set_flow_labels(self, flow_matrix):
        weights = nx.get_edge_attributes(self.visualization, 'weight')
        for i, j in weights.keys():
            weights[(i, j)] = str(flow_matrix[j][i]) + '/' + str(weights[(i, j)])

        nx.draw_networkx_edge_labels(self.visualization, pos=self.pos, edge_labels=weights, ax=self.axis)
        self.canvas.draw()

    def ford_fulkenson(self):
        source = 0
        target = len(self.graph.get_vertices()) - 1
        matrix = self.graph.to_matrix()
        path = [-1 for _ in range(len(self.graph.get_vertices()))]
        max_flow = 0

        while self.bfs(source, target, path, matrix):
            path_flow = math.inf
            tmp = target

            while tmp != source:
                path_flow = min(path_flow, matrix[path[tmp]][tmp])
                tmp = path[tmp]

            max_flow += path_flow
            v = target

            while v != source:
                u = path[v]
                matrix[u][v] -= path_flow
                matrix[v][u] += path_flow
                v = path[v]

        self.print_graph()
        self.append_layers_info()

        text = '\nMaksymalny przepływ:\n'
        text += str(max_flow)
        self.append_text(text)
        self.set_flow_labels(matrix)
