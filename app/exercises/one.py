import tkinter as tk
from tkinter import ttk

class ExerciseOneTab(ttk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.add_buttons()

    def add_buttons(self):
        self.gal_btn = ttk.Button(self, text="Konwertuj na listę sąsiedztwa", command=self.convert_to_gal)
        self.gal_btn.pack(pady = 10)

        self.gam_btn = ttk.Button(self, text="Konwertuj na macierz sąsiedztwa", command=self.convert_to_gam)
        self.gam_btn.pack(pady= 10)

        self.gim_btn = ttk.Button(self, text="Konwertuj na macierz incydencji", command=self.convert_to_gim)
        self.gim_btn.pack(pady = 10)


    def convert_to_gal(self):
        pass

    def convert_to_gam(self):
        pass

    def convert_to_gim(self):
        pass