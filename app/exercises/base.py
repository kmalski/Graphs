from utils.tkinter import ScrollableFrame, InfoLabel, ResizingSquareCanvas

import tkinter as tk
from abc import ABC, abstractmethod
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import ttk


class BaseTab(ttk.Frame, ABC):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.graph = None

    @abstractmethod
    def add_menu(self):
        pass

    def add_vertical_separator(self, column):
        ttk.Separator(self, orient='vertical')\
            .grid(row=0, column=column, pady=5, sticky='NS')

    def add_text_frame(self, row, column):
        frame = ScrollableFrame(self)
        frame.grid(row=row, column=column, sticky='NSWE')
        frame.grid_propagate(False)

        self.result = InfoLabel(frame.scrollable_frame, font=("Helvetica", 16))
        self.result.grid(row=1, column=0)

        frame.bind_vertical_scroll('<MouseWheel>', self)
        frame.bind_horizontal_scroll('<MouseWheel>', frame.scrollbar_x)

    def add_canvas(self, row, column, for_networkX=False):
        frame = ttk.Frame(self)
        frame.grid(row=row, column=column, sticky='NSWE')
        frame.grid_propagate(False)

        if not for_networkX:
            self.canvas = ResizingSquareCanvas(frame, width=1, height=1)
            self.canvas.grid(row=0, column=0)
        else:
            class CustomToolbar(NavigationToolbar2Tk):
                # only display the buttons we need
                toolitems = [t for t in NavigationToolbar2Tk.toolitems if
                            t[0] in ('Home', 'Pan', 'Zoom', 'Save')]

            figure = Figure(figsize=(5, 4), constrained_layout=True, frameon=False)
            self.axis = figure.add_subplot(111)
            self.axis.axis(False)
            self.canvas = FigureCanvasTkAgg(figure, master=frame)

            self.toolbar = CustomToolbar(self.canvas, frame)
            self.toolbar.update()

            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.canvas.draw()

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

    def draw_graph(self):
        pass

    def print_graph(self):
        if self.graph is not None:
            self.result.show_normal(str(self.graph))

    def clear_text(self):
        self.result.clear()

    def clear_graph(self):
        self.graph = None
        self.canvas.delete('all')

    def append_text(self, text):
        self.result.append(text)