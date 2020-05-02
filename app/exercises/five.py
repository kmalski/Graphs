from exercises.base import BaseTab
from structures.weighted_adjacency_list import WeightedDirectedAdjacencyList

import networkx as nx
import tkinter as tk
import collections as cs
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import ttk, messagebox


class ExerciseFiveTab(BaseTab):
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
        self.vertices_entry = ttk.Entry(gen_np_frame, width=10)
        self.vertices_entry.grid(row=1, column=0, pady=2, padx=2)

        ttk.Button(gen_np_frame, text='Generuj losową sieć przepływową', width=30, command=self.generate_network)\
            .grid(row=2, column=0, columnspan=1, pady=10)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=1, column=0, sticky='EW', pady=15)

        ttk.Button(gen_np_frame, text='Wartość maksymalnego przepływu', width=30, command=self.FordFulkenson)\
            .grid(row=3, column=0, columnspan=2, pady=10)

    def add_canvas(self, row, column):
        class CustomToolbar(NavigationToolbar2Tk):
            # only display the buttons we need
            toolitems = [t for t in NavigationToolbar2Tk.toolitems if
                         t[0] in ('Home', 'Pan', 'Zoom', 'Save')]

        frame = ttk.Frame(self)
        frame.grid(row=row, column=column, sticky='NSWE')
        frame.grid_propagate(False)

        figure = Figure(figsize=(5, 4), constrained_layout=True, frameon=False)
        self.axis = figure.add_subplot(111)
        self.axis.axis(False)
        self.canvas = FigureCanvasTkAgg(figure, master=frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = CustomToolbar(self.canvas, frame)
        self.toolbar.update()

        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas.draw()

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def generate_network(self):
        try:
            n = int(self.vertices_entry.get())
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!',
                                message='Wprowadź prawidłowe dane wejściowe!')
            return

        if n < 2:
            messagebox.showinfo(
                title='Wykrzyknik!', message='Liczba wierzchołków nie może być mniejsza niż 2!')
            return

        self.graph = WeightedDirectedAdjacencyList.init_empty()
        layers = self.graph.generate_flow_network(n)

        self.visualization = self.graph.convert_to_networkX()
        self.axis.clear()

        labels = nx.get_edge_attributes(self.visualization, 'weight')
        self.pos = nx.spring_layout(self.visualization)
        nx.draw_networkx(self.visualization, pos=self.pos, ax=self.axis)
        nx.draw_networkx_edge_labels(
            self.visualization, pos=self.pos, edge_labels=labels, ax=self.axis)

        self.canvas.draw()
        self.print_graph()

        layers_string = '\nWarstwy:\n'
        for layer, vertices in layers.items():
            layers_string += f'{layer}: {vertices}\n'

        self.append_text(layers_string)

    def BFS(self, s, t, path, matrix):

        visited = [False for _ in range(len(matrix))]
        visited[s] = True

        Q = cs.deque([])
        Q.append(s)

        while Q:
            u = Q.popleft()

            for ind, val in enumerate(matrix[u]):
                if visited[ind] == False and val > 0:
                    Q.append(ind)
                    visited[ind] = True
                    path[ind] = u

        return True if visited[t] else False

    def set_flow_labels(self, flow_matrix):
        weights = nx.get_edge_attributes(self.visualization, 'weight')
        for i, j in weights.keys():
            weights[(i, j)] = str(flow_matrix[j][i]) + '/' + str(weights[(i, j)])

        nx.draw_networkx_edge_labels(
            self.visualization, pos=self.pos, edge_labels=weights, ax=self.axis)
        self.canvas.draw()

    def FordFulkenson(self):
        s = 0
        t = len(self.graph.get_vertices())-1

        matrix = self.graph.convert_to_matrix()
        licznik = 0

        path = [-1 for _ in range(len(self.graph.get_vertices()))]
        maxFlow = 0

        while self.BFS(s, t, path, matrix):
            pathFlow = math.inf
            tmp = t

            while(tmp != s):
                pathFlow = min(pathFlow, matrix[path[tmp]][tmp])
                tmp = path[tmp]

            maxFlow += pathFlow
            v = t

            while(v != s):
                u = path[v]
                matrix[u][v] -= pathFlow
                matrix[v][u] += pathFlow
                v = path[v]

            licznik += 1

        print(abs(maxFlow))
        text = "\nMaksymalny\nprzepływ:\n"
        text += str(maxFlow)
        self.append_text(text)
        self.set_flow_labels(matrix)


