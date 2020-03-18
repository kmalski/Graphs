from utils.graphic_sequence import is_graphic_sequence
from utils.tkinter import ResizingSquareCanvas
from structures.adjacency_list import AdjacencyList

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ExerciseTwoTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.add_menu()

    def add_menu(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0)

        self.sequence_entry = ttk.Entry(frame, width=50)
        self.sequence_entry.grid(row=0, column=0)

        sequence_button = ttk.Button(frame, width=30, text='Sprawdź, czy to ciąg graficzny', command=self.check_sequence)
        sequence_button.grid(row=1, column=0)

        self.result = ttk.Label(frame)
        self.result.grid(row=2, column=0)

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
            graph = AdjacencyList.from_graphic_sequence(sequence)
            print(graph) #TO DO: Replace by drawing canvas
        else:
            self.result['text'] = 'Z podanej sekwencji NIE MOŻNA utworzyć ciągu graficznego!'
            self.result['foreground'] = '#FF0000'
        
