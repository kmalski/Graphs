from exercises.one import ExerciseOneTab
from exercises.two import ExerciseTwoTab


import tkinter as tk
from tkinter import ttk


class App (tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Grafy')
        self.geometry('800x600')

        self.screen_state = False

        self.bind('<F11>', self.toggle_fullscreen)
        self.bind('<Escape>', self.end_fullscreen)

        self.add_tabs()

    def add_tabs(self):
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill='both')

        exercise_1 = ExerciseOneTab(self)
        self.tabs.add(exercise_1, text='Zadanie 1')

        exercise_2 = ExerciseTwoTab(self)
        self.tabs.add(exercise_2, text='Zadanie 2')

    def toggle_fullscreen(self, event=None):
        self.screen_state = not self.screen_state
        if self.screen_state:
            self.state('zoomed')
        else:
            self.state('normal')

    def end_fullscreen(self, event=None):
        self.screen_state = False
        self.state('normal')


if (__name__ == '__main__'):
    app = App()
    app.mainloop()
