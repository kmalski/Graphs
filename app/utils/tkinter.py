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
        self.scale("all", 0, 0, scale, scale)


# ScrollableFrame's object itself is the outer frame containing canvas and scrollbars
# If you wanted to use this class, remember to place things inside self.scrollable_frame, and not directly into an object of this class
class ScrollableFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1) # canvas
        self.grid_columnconfigure(1, weight=0) # right scrollbar
        self.grid_rowconfigure(0, weight=1) # canvas
        self.grid_rowconfigure(1, weight=0) # bottom scrollbar

        canvas = tk.Canvas(self)
        scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar_x.set)
        canvas.configure(yscrollcommand=scrollbar_y.set)

        self.scrollable_frame.bind(  
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.grid(row=0, column=0, sticky="NSEW")
        scrollbar_x.grid(row=1, column=0, sticky="WE")
        scrollbar_y.grid(row=0, column=1, sticky="NS")

def get_root_size(widget):
    root = widget.winfo_toplevel()
    root.update_idletasks()

    return (root.winfo_width(), root.winfo_height())
