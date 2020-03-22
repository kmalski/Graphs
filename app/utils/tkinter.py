import tkinter as tk
from tkinter import ttk


class ResizingSquareCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.size = min(kwargs['height'], kwargs['width'])

        self.master.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        new_size = min(event.width, event.height)

        scale = new_size / self.size
        self.size = new_size

        self.config(width=new_size, height=new_size)
        self.scale('all', 0, 0, scale, scale)


class ScrollableFrame(ttk.Frame):
    '''
    Object itself is the outer frame containing canvas and scrollbars.
    If you wanted to use this class, remember to place things inside 
    self.scrollable_frame, and not directly into an object of this class.
    '''

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)  # canvas
        self.grid_columnconfigure(1, weight=0)  # right scrollbar
        self.grid_rowconfigure(0, weight=1)     # canvas
        self.grid_rowconfigure(1, weight=0)     # bottom scrollbar

        self.canvas = tk.Canvas(self)
        self.scrollbar_x = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.scrollbar_y = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollable_frame.bind(
            '<Configure>',
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox('all')
            )
        )

        self.canvas.grid(row=0, column=0, sticky="NSEW")
        self.scrollbar_x.grid(row=1, column=0, sticky="WE")
        self.scrollbar_y.grid(row=0, column=1, sticky="NS")

        self.scrollbar_x.bind('<MouseWheel>', self.on_horizontal_mousewheel)

    def on_vertical_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    def on_horizontal_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), 'units')

    def bind_vertical_scroll(self, key, widget):
        widget.bind_all(key, self.on_vertical_mousewheel)
        self.scrollbar_x.bindtags(self.scrollbar_x.bindtags()[:-1])

    def bind_horizontal_scroll(self, key, widget):
        widget.bind(key, self.on_horizontal_mousewheel)


class InfoLabel(ttk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.fail_color = '#FF0000'
        self.success_color = '#006400'
        self.warning_color = '#EBC52D'

    def set_fail_color(self, color):
        self.fail_color = color

    def set_success_color(self, color):
        self.success_color = color

    def show_fail(self, text):
        super().grid()
        self['text'] = text
        self['foreground'] = self.fail_color

    def show_success(self, text):
        super().grid()
        self['text'] = text
        self['foreground'] = self.success_color

    def show_warning(self, text):
        super().grid()
        self['text'] = text
        self['foreground'] = self.warning_color

    def show_normal(self, text):
        super().grid()
        self['text'] = text
        self['foreground'] = 'black'

    def grid_quietly(self, row, column):
        super().grid(row=row, column=column)
        super().grid_remove()

    def hide(self):
        super().grid_remove()

    def show(self):
        super().grid()

    def clear(self):
        self['text'] = ''


def get_root_size(widget):
    root = widget.winfo_toplevel()
    root.update_idletasks()

    return (root.winfo_width(), root.winfo_height())
