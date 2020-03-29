import utils.draw
import utils.graph_utils
from structures.adjacency_list import AdjacencyList, DirectedAdjacencyList
from utils.tkinter import ResizingSquareCanvas, ScrollableFrame, InfoLabel

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class ExerciseFourTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.graph = None

        self.grid_columnconfigure(0, weight=0)  # menu
        self.grid_columnconfigure(1, weight=0)  # separator
        self.grid_columnconfigure(2, weight=2)  # text frame
        self.grid_columnconfigure(3, weight=0)  # separator
        self.grid_columnconfigure(4, weight=2)  # canvas

        self.grid_rowconfigure(0, weight=1)

        self.add_menu()
        self.add_vertical_separator(column=1)
        self.add_text_frame()
        self.add_vertical_separator(column=3)
        self.add_canvas()

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

    def add_text_frame(self):
        frame = ScrollableFrame(self)
        frame.grid(row=0, column=2, sticky='NSWE')
        frame.grid_propagate(False)

        self.result = InfoLabel(frame.scrollable_frame, font=("Helvetica", 16))
        self.result.grid(row=1, column=0)

        frame.bind_vertical_scroll('<MouseWheel>', self)
        frame.bind_horizontal_scroll('<MouseWheel>', frame.scrollbar_x)

    def add_canvas(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=4, sticky='NSWE')
        frame.grid_propagate(False)

        self.canvas = ResizingSquareCanvas(frame, width=1, height=1)
        self.canvas.grid(row=0, column=0)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def add_vertical_separator(self, column):
        ttk.Separator(self, orient='vertical')\
            .grid(row=0, column=column, pady=5, sticky='NS')

    def draw_graph(self):
        if self.graph is not None:
            utils.draw.draw_directed_graph(self.canvas, self.graph)

    def print_graph(self):
        if self.graph is not None:
            self.result.show_normal(str(self.graph))

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
        res_string = 'Silnie spójne składowe\n'
        for comp_nr, vertices in components.items():
            res_string += f'{comp_nr}: {vertices}\n'

        self.result.show_normal(res_string)
        # self.draw_graph(components)
