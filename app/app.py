import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class App (tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Grafy')
        self.geometry('1080x720')

        self.add_menu_bar()
        self.add_tabs()

    def add_tabs(self):
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill='both')

        exercise_1 = ttk.Frame(self.tabs)
        self.tabs.add(exercise_1, text='Zadanie 1')

        exercise_2 = ttk.Frame(self.tabs)
        self.tabs.add(exercise_2, text='Zadanie 2')

    def add_menu_bar(self):
        self.menu_bar = tk.Menu(self)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label='Load graph...', command=self.load_graph)
        self.menu_bar.add_cascade(label='File', menu=file_menu)

        self.config(menu=self.menu_bar)

    def load_graph(self, event=None):
        file_path = filedialog.askopenfilename(initialdir='/', title='Wybierz plik', filetypes=[('Graph files', '*.gph')])


if (__name__ == '__main__'):
    app = App()
    app.mainloop()
