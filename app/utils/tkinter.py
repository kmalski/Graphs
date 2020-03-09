import tkinter


class ResizingCanvas(tkinter.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.height = kwargs['height']
        self.width = kwargs['width']
        self.master.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        new_width = event.width
        new_height = event.height
        wscale = new_width / self.width
        hscale = new_height / self.height
        
        self.width = new_width
        self.height = new_height

        self.config(width=self.width, height=self.height)
        self.scale("all", 0, 0, wscale, hscale)


def get_root_size(widget):
    root = widget.winfo_toplevel()
    root.update_idletasks()

    return (root.winfo_width(), root.winfo_height())
