import tkinter


class ResizingSquareCanvas(tkinter.Canvas):
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


def get_root_size(widget):
    root = widget.winfo_toplevel()
    root.update_idletasks()

    return (root.winfo_width(), root.winfo_height())
