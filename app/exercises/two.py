import utils.draw
from structures.adjacency_list import AdjacencyList
from utils.graph_utils import is_graphic_sequence
from utils.graph_utils import randomize
from utils.tkinter import ResizingSquareCanvas
from utils.tkinter import ScrollableFrame

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ExerciseTwoTab(ttk.Frame):
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

        ttk.Label(menu_frame, text='Ciąg liczb').grid(row=0, column=0)

        self.sequence_entry = ttk.Entry(menu_frame, width=55)
        self.sequence_entry.grid(row=1, column=0, pady=3)

        sequence_button = ttk.Button(menu_frame, width=30, text='Sprawdź, czy to ciąg graficzny', command=self.check_sequence)
        sequence_button.grid(row=2, column=0, pady=3)

        self.result = ttk.Label(menu_frame)
        self.result.grid(row=3, column=0)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=4, column=0, columnspan=2, sticky='EW', pady=15)

        ttk.Label(menu_frame, text='Ilość randomizacji').grid(row=5, column=0)

        self.randomize_entry = ttk.Entry(menu_frame, width=30)
        self.randomize_entry.grid(row=6, column=0, pady=3)

        randomize_button = ttk.Button(menu_frame, width=30, text='Randomizuj graf', command=self.randomize_graph)
        randomize_button.grid(row=7, column=0, pady=3)

        ttk.Separator(menu_frame, orient='horizontal')\
            .grid(row=8, column=0, columnspan=2, sticky='EW', pady=15)

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

        if is_graphic_sequence(sequence):
            self.result['text'] = 'Z podanej sekwencji MOŻNA utworzyć ciąg graficzny!'
            self.result['foreground'] = '#006400'
            self.graph = AdjacencyList.from_graphic_sequence(sequence)
            self.draw_graph()
        else:
            self.result['text'] = 'Z podanej sekwencji NIE MOŻNA utworzyć ciągu graficznego!'
            self.result['foreground'] = '#FF0000'
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

        for _ in range(randomize_amount):
            randomize(self.graph)

        self.draw_graph()

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
            utils.draw.draw_graph(self.canvas, self.graph)
    
    def clear_graph(self):
        self.canvas.delete('all')
        
