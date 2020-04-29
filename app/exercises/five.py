from exercises.base import BaseTab
from structures.weighted_adjacency_list import WeightedDirectedAdjacencyList

import networkx as nx
import tkinter as tk

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
            messagebox.showinfo(title='Wykrzyknik!', message='Wprowadź prawidłowe dane wejściowe!')
            return

        if n < 2:
            messagebox.showinfo(title='Wykrzyknik!', message='Liczba wierzchołków nie może być mniejsza niż 2!')
            return

        self.graph = WeightedDirectedAdjacencyList.init_empty()
        layers = self.graph.generate_flow_network(n)

        self.visualization = self.graph.convert_to_networkX()
        self.axis.clear()
        
        labels = nx.get_edge_attributes(self.visualization,'weight')
        pos=nx.spring_layout(self.visualization)
        nx.draw_networkx(self.visualization, pos=pos, ax=self.axis)
        nx.draw_networkx_edge_labels(self.visualization, pos=pos, edge_labels=labels, ax=self.axis)

        self.canvas.draw()
        self.print_graph()

        layers_string = '\nWarstwy:\n'
        for layer, vertices in layers.items():
            layers_string += f'{layer}: {vertices}\n'

        self.append_text(layers_string)
        