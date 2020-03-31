import utils.draw
from exercises.base import BaseTab
from structures.adjacency_list import AdjacencyList
from utils.graph_utils import is_graphic_sequence, randomize, find_biggest_components,\
    generate_random_euler_graph, randomize_times, generate_k_regular_graph
from utils.tkinter import InfoLabel, ResizingSquareCanvas

import random
import tkinter as tk
from tkinter import ttk, messagebox

max_rand_it = 1000


class ExerciseTwoTab(BaseTab):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.grid_columnconfigure(0, weight=0)  # menu
        self.grid_columnconfigure(1, weight=0)  # separator
        self.grid_columnconfigure(2, weight=2)  # canvas

        self.grid_rowconfigure(0, weight=1)

        self.add_menu()
        self.add_vertical_separator(column=1)
        self.add_canvas(row=0, column=2)

    def add_menu(self):
        menu_frame = ttk.Frame(self)
        menu_frame.grid(row=0, column=0, sticky='N', padx=10, pady=10)

        ########################### 1 ###########################

        ttk.Label(menu_frame, text='Ciąg liczb').grid(row=0, column=0)

        self.sequence_entry = ttk.Entry(menu_frame, width=55)
        self.sequence_entry.grid(row=1, column=0, pady=3)

        sequence_button = ttk.Button(menu_frame, width=30, text='Sprawdź, czy to ciąg graficzny', command=self.check_sequence)
        sequence_button.grid(row=2, column=0, pady=3)

        self.load_result = InfoLabel(menu_frame)
        self.load_result.grid_quietly(row=3, column=0)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=4, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 2 ###########################

        ttk.Label(menu_frame, text='Liczba randomizacji').grid(row=5, column=0)

        self.randomize_entry = ttk.Entry(menu_frame, width=30)
        self.randomize_entry.grid(row=6, column=0, pady=3)

        randomize_button = ttk.Button(menu_frame, width=30, text='Randomizuj graf', command=self.randomize_graph)
        randomize_button.grid(row=7, column=0, pady=3)

        self.randomize_result = InfoLabel(menu_frame)
        self.randomize_result.grid_quietly(row=8, column=0)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=9, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 3 ###########################

        sequence_button = ttk.Button(menu_frame, width=30, text='Wyznacz spójne składowe', command=self.find_components)
        sequence_button.grid(row=10, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=11, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 4 ###########################

        ttk.Label(menu_frame, text='Liczba wierzchołków').grid(row=12, column=0)

        self.euler_entry = ttk.Entry(menu_frame, width=30)
        self.euler_entry.grid(row=13, column=0, pady=3)

        euler_button = ttk.Button(menu_frame, width=30, text='Losuj graf eulerowski', command=self.euler_graph)
        euler_button.grid(row=14, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=15, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 5 ###########################

        k_regular_frame = ttk.Frame(menu_frame)
        k_regular_frame.grid(row=16, column=0)

        ttk.Label(k_regular_frame, text='Liczba wierzch.').grid(row=0, column=0, padx=4)

        self.regular_n = ttk.Entry(k_regular_frame, width=15)
        self.regular_n.grid(row=1, column=0, pady=2, padx=4)

        ttk.Label(k_regular_frame, text='Stopień wierzch.').grid(row=0, column=1, padx=4)

        self.regular_k = ttk.Entry(k_regular_frame, width=15)
        self.regular_k.grid(row=1, column=1, pady=2, padx=4)

        ttk.Button(k_regular_frame, text='Generuj graf k-regularny', width=30, command=self.k_regular)\
            .grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=17, column=0, columnspan=2, sticky='EW', pady=15)

        ########################### 6 ###########################

        hamilton_button = ttk.Button(menu_frame, width=30, text='Szukaj cyklu Hamiltona', command=self.hamilton_graph)
        hamilton_button.grid(row=18, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=19, column=0, columnspan=2, sticky='EW', pady=15)

    def add_canvas(self, row, column):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=2, sticky='NSWE')
        frame.grid_propagate(False)

        self.canvas = ResizingSquareCanvas(frame, width=1, height=1)
        self.canvas.grid(row=0, column=0)

        results_frame = ttk.Frame(frame)
        results_frame.grid(row=1, column=0, padx=20, pady=20, sticky='W')
        self.results = InfoLabel(results_frame, font=('Roboto', 14), anchor='w', justify='left')
        self.results.grid(row=0, column=0)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def draw_graph(self, components=None):
        if self.graph is not None:
            utils.draw.draw_graph(self.canvas, self.graph, components)

    def clear_info_labels(self):
        self.randomize_result.hide()
        self.load_result.hide()
        self.results.clear()

    def check_sequence(self):
        sequence = self.sequence_entry.get()
        if not sequence:
            messagebox.showinfo(title='Wykrzyknik!', message='Musisz wprowadzić jakąś sekwencję!')
            return

        try:
            sequence = list(map(lambda x: int(x), sequence.split()))
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!', message='Sekwencja musi składać się wyłącznie z liczb!')
            return

        self.clear_info_labels()
        if is_graphic_sequence(sequence):
            self.load_result.show_success('Z podanej sekwencji MOŻNA utworzyć ciąg graficzny!')
            self.graph = AdjacencyList.from_graphic_sequence(sequence)
            self.draw_graph()
        else:
            self.load_result.show_fail('Z podanej sekwencji NIE MOŻNA utworzyć ciągu graficznego!')
            self.clear_graph()

    def randomize_graph(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        randomize_amount = self.randomize_entry.get()

        if not randomize_amount:
            messagebox.showinfo(title='Wykrzyknik!', message='Musisz wprowadzić liczbę żądanych randomizacji!')
            return

        try:
            randomize_amount = int(randomize_amount)
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!', message='Wprowadzono nieprawidłowe dane!')
            return

        if randomize_amount < 0:
            messagebox.showinfo(title='Wykrzyknik!', message='Liczba randomizacji nie może być mniejsza od 0!')
            return

        success_count = 0
        for _ in range(randomize_amount):
            if randomize(self.graph, max_it=max_rand_it):  # infinite loop break condition
                success_count += 1

        if success_count == randomize_amount:
            self.randomize_result.show_success(f'Randomizację udało się wykonać {success_count}/{randomize_amount} razy')
            self.results.clear()
            self.draw_graph()
        elif success_count > 0:
            self.randomize_result.show_warning(f'Randomizację udało się wykonać {success_count}/{randomize_amount} razy')
            self.results.clear()
            self.draw_graph()
        else:
            attempts = max_rand_it * self.graph.get_amount_of_vertices()
            self.randomize_result.show_fail(f'''Nie udało się zrandomizować grafu :(
Wykonano {attempts} prób losowania krawędzi.
Zastanów się czy zamiana krawędzi jest możliwa.''')

    def find_components(self):
        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        graph = self.graph
        if not isinstance(self.graph, AdjacencyList):
            graph = self.graph.to_adjacency_list()

        components = graph.find_components()
        biggest_comps = find_biggest_components(components)
        res_string = ',  '.join(list(map(lambda x: str(x), biggest_comps)))

        if len(biggest_comps) > 1:
            self.results.show_normal(f'Największe wspólne składowe: {res_string}')
        else:
            self.results.show_normal(f'Największa wspólna składowa: {res_string}')
        self.draw_graph(components)

    def euler_graph(self):
        self.clear_info_labels()
        verticles_amount = self.euler_entry.get()

        if not verticles_amount:
            messagebox.showinfo(title='Wykrzyknik!', message='Musisz wprowadzić liczbę wierzchołków!')
            return

        try:
            verticles_amount = int(verticles_amount)
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!', message='Wprowadzono nieprawidłowe dane!')
            return

        if verticles_amount < 3:
            messagebox.showinfo(title='Wykrzyknik!', message='Liczba wierzchołków nie może być mniejsza od 3!')
            return

        self.graph = generate_random_euler_graph(verticles_amount)

        while True:
            randomize_times(self.graph, 100)
            if self.graph.is_connected():
                break

        eulerian_path = self.graph.find_eulerian_path()
        res_string = ' - '.join(list(map(lambda x: str(x), eulerian_path)))

        self.results.show_normal(f'Kolejne wierzchołki cyklu Eulera: {res_string}')
        self.draw_graph()

    def k_regular(self):
        self.clear_info_labels()
        verticles_amount = self.regular_n.get()
        degree = self.regular_k.get()

        if not verticles_amount or not degree:
            messagebox.showinfo(title='Wykrzyknik!', message='Musisz wprowadzić liczbę wierzchołków oraz ich stopień!')
            return

        try:
            verticles_amount = int(verticles_amount)
            degree = int(degree)
        except ValueError:
            messagebox.showinfo(title='Wykrzyknik!', message='Wprowadzono nieprawidłowe dane!')
            return

        if not -1 < degree < verticles_amount:
            messagebox.showinfo(title='Wykrzyknik!', message='Liczba wierzchołków musi być większa od stopnia grafu!')
            return

        self.graph = generate_k_regular_graph(verticles_amount, degree)
        randomize_times(self.graph, 100)
        self.draw_graph()

    def hamilton_graph(self):
        self.clear_info_labels()

        if self.graph is None:
            messagebox.showinfo(title='Wykrzyknik!', message='Najpierw musisz wprowadzić graf!')
            return

        if not self.graph.is_connected():
            self.results.show_normal('Graf nie jest hamiltonowski')
            return

        hamiltonian_cycle = []

        if self.graph.is_hamiltonian(0, hamiltonian_cycle):
            res_string = '\nKolejne wierzchołki cyklu Hamiltona: '
            res_string += ' - '.join(list(map(lambda x: str(x), hamiltonian_cycle)))
        else:
            res_string = 'Graf nie jest hamiltonowski'

        self.results.show_normal(res_string)
