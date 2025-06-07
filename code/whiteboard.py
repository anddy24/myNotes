import tkinter as tk

class WhiteboardFrame(tk.Frame):
    def __init__(self, master, strings, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.lines = []  # stores all lines
        self.redo_stack = []  # stores lines that were undone

        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)

        # Add Undo/Redo buttons
        toolbar = tk.Frame(self)
        toolbar.pack(side="top", fill="x")

        undo_btn = tk.Button(toolbar, text=strings.get("undo", "Undo"), command=self.undo)
        undo_btn.pack(side="left")

        redo_btn = tk.Button(toolbar, text=strings.get("redo", "Redo"), command=self.redo)
        redo_btn.pack(side="left")

        self.current_line = None

    def start_draw(self, event):
        self.current_line = [self.canvas.create_line(event.x, event.y, event.x, event.y, fill="black", width=2)]
        self.lines.append(self.current_line)
        self.redo_stack.clear()  # clear redo stack after new drawing

    def draw(self, event):
        line_id = self.current_line[-1]
        coords = self.canvas.coords(line_id)
        new_line = self.canvas.create_line(coords[2], coords[3], event.x, event.y, fill="black", width=2)
        self.current_line.append(new_line)

    def undo(self):
        if self.lines:
            last_line = self.lines.pop()
            for line_id in last_line:
                self.canvas.delete(line_id)
            self.redo_stack.append(last_line)

    def redo(self):
        if self.redo_stack:
            line_to_redraw = self.redo_stack.pop()
            new_line_ids = []
            for line_id in line_to_redraw:
                coords = self.canvas.coords(line_id)
                new_id = self.canvas.create_line(*coords, fill="black", width=2)
                new_line_ids.append(new_id)
            self.lines.append(new_line_ids)
