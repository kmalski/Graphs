from structures.graphic_sequence import is_graphic_sequence, GraphicSequence

import tkinter as tk
from tkinter import ttk


class ExerciseTwoTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.add_menu()

    def add_menu(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0)

        self.sequence_entry = ttk.Entry(frame, width=50)
        self.sequence_entry.grid(row=0, column=0)

        sequence_button = ttk.Button(frame, width=30, command=self.check_sequence)
        sequence_button.grid(row=1, column=0)

    def check_sequence(self):
        sequence_str = self.sequence_entry.get()

        if is_graphic_sequence(sequence_str):
            print('Taaak')
        else:
            print('Nieee')