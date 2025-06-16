import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw
from PIL import ImageTk
import os
import pickle

C = 20 #icon size
X = 6 #padding x

class WhiteboardFrame(tk.Frame):
    def __init__(self, master, strings, theme_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme_manager = theme_manager
        self.configure(bg=self.theme_manager.get_color("background"))

        self.bg_color = self.theme_manager.get_color("background")
        self.brush_color = "black"
        self.brush_size = 3
        self.cache_path = "whiteboard_cache.pkl"
        bg_color = self.theme_manager.get_color("background")
        self.current_tool = "brush"

        # Toolbar
        toolbar = tk.Frame(self, bg=bg_color)
        toolbar.pack(side="top", fill="x", pady=2)

        self.undo_icon = ImageTk.PhotoImage(Image.open("icons/undo.png").resize((C, C), Image.Resampling.LANCZOS))
        self.redo_icon = ImageTk.PhotoImage(Image.open("icons/redo.png").resize((C, C), Image.Resampling.LANCZOS))
        self.color_icon = ImageTk.PhotoImage(Image.open("icons/color-selection.png").resize((C, C), Image.Resampling.LANCZOS))
        self.save_icon = ImageTk.PhotoImage(Image.open("icons/save.png").resize((C, C), Image.Resampling.LANCZOS))
        self.export_icon = ImageTk.PhotoImage(Image.open("icons/export.png").resize((C, C), Image.Resampling.LANCZOS))
        self.erase_icon = ImageTk.PhotoImage(Image.open("icons/rubber.png").resize((C, C), Image.Resampling.LANCZOS))
        self.erase_obj_icon = ImageTk.PhotoImage(Image.open("icons/objects.png").resize((C, C), Image.Resampling.LANCZOS))

        tk.Button(toolbar, image=self.undo_icon, text=strings.get("undo", "Undo"), command=self.undo, bd=0, bg=bg_color).pack(side="left", padx=X)
        tk.Button(toolbar, image=self.redo_icon, text=strings.get("redo", "Redo"), command=self.redo, bd=0, bg=bg_color).pack(side="left", padx=X)

        self.brush_slider = tk.Scale(
            toolbar,
            from_=1,
            to=20,
            orient="horizontal",
            command=self.change_brush_size,
            bd=0,
            bg=bg_color,      # background of the widget
            troughcolor=self.theme_manager.get_color("current_line"),      # background of the trough (track)
            highlightthickness=0,      # removes highlight border
            fg=self.theme_manager.get_color("foreground")  # label/scale text color
        )
        self.brush_slider.set(self.brush_size)
        self.brush_slider.pack(side="left", padx=2)

        def on_enter_slider(event):
            self.brush_slider.configure(bg=self.theme_manager.get_color("comment"))

        def on_leave_slider(event):
            self.brush_slider.configure(bg=bg_color)
        
        self.brush_slider.bind("<Enter>", on_enter_slider)
        self.brush_slider.bind("<Leave>", on_leave_slider)

        tk.Button(toolbar, image=self.color_icon, command=self.choose_color, bd=0, bg=bg_color).pack(side="left", padx=X)
        tk.Button(toolbar, image=self.erase_icon, command=self.erase, bd=0, bg=bg_color).pack(side="left", padx=X)
        tk.Button(toolbar, image=self.erase_obj_icon, command=self.erase_object, bd=0, bg=bg_color).pack(side="left", padx=X)

        tk.Button(toolbar, image=self.save_icon, command=self.save_cache, bd=0, bg=bg_color).pack(side="right", padx=X)
        tk.Button(toolbar, image=self.export_icon, command=self.export_image, bd=0, bg=bg_color).pack(side="right", padx=X)

        # Canvas (auto-expanding)
        self.canvas = tk.Canvas(self, bg=self.bg_color)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.bind("<B1-Motion>", self.handle_draw)
        self.canvas.bind("<ButtonPress-1>", self.handle_press)

        self.image = None
        self.draw_image = None
        self.lines = []
        self.redo_stack = []
        self.current_line = []
        self.last_x = self.last_y = 0

        self.after(100, self.init_image)
        self.load_cache()

    def init_image(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.image = Image.new("RGB", (w, h), self.bg_color)
        self.draw_image = ImageDraw.Draw(self.image)

    def resize_canvas(self, event):
        # Resize image only on enlarge
        old_img = self.image
        if not old_img:
            return
        new_img = Image.new("RGB", (event.width, event.height), self.bg_color)
        new_img.paste(old_img, (0, 0))
        self.image = new_img
        self.draw_image = ImageDraw.Draw(self.image)
        self.redraw_from_lines()

    def start_draw(self, event):
        self.current_line = []
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        line_id = self.canvas.create_line(x1, y1, x2, y2,
                                          fill=self.brush_color, width=self.brush_size,
                                          capstyle=tk.ROUND, smooth=True)
        self.current_line.append((x1, y1, x2, y2, self.brush_color, self.brush_size))
        self.lines.append([(x1, y1, x2, y2, self.brush_color, self.brush_size)])
        self.draw_image.line([x1, y1, x2, y2], fill=self.brush_color, width=self.brush_size)
        self.last_x, self.last_y = x2, y2
        self.redo_stack.clear()

    def undo(self):
        if self.lines:
            last = self.lines.pop()
            self.redo_stack.append(last)
            self.redraw_from_lines()

    def redo(self):
        if self.redo_stack:
            redo_line = self.redo_stack.pop()
            self.lines.append(redo_line)
            for x1, y1, x2, y2, color, size in redo_line:
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=size, capstyle=tk.ROUND, smooth=True)
                self.draw_image.line([x1, y1, x2, y2], fill=color, width=size)

    def redraw_from_lines(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.image = Image.new("RGB", (w, h), self.bg_color)
        self.draw_image = ImageDraw.Draw(self.image)
        for line in self.lines:
            for x1, y1, x2, y2, color, size in line:
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=size, capstyle=tk.ROUND, smooth=True)
                self.draw_image.line([x1, y1, x2, y2], fill=color, width=size)

    def change_brush_size(self, val):
        self.brush_size = int(val)

    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.brush_color)
        if color[1]:
            self.brush_color = color[1]

    def save_cache(self):
        try:
            with open(self.cache_path, "wb") as f:
                pickle.dump(self.lines, f)
            messagebox.showinfo("Saved", "Drawing saved to cache.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def load_cache(self):
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "rb") as f:
                    self.lines = pickle.load(f)
                self.redraw_from_lines()
            except Exception as e:
                messagebox.showwarning("Warning", f"Could not load cache: {e}")

    def export_image(self):
        file = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG Files", "*.png")])
        if file:
            self.image.save(file)
            messagebox.showinfo("Exported", f"Image exported to {file}")

    def erase(self):
        self.current_tool = "eraser"
        self.brush_color = self.bg_color

    def erase_object(self):
        self.current_tool = "erase_object"

    def handle_press(self, event):
        if self.current_tool == "erase_object":
            self.erase_stroke_at(event.x, event.y)
        else:
            self.start_draw(event)

    def handle_draw(self, event):
        if self.current_tool in ("brush", "eraser"):
            self.draw(event)

    def erase_stroke_at(self, x, y):
        for i, stroke in enumerate(reversed(self.lines)):
            for x1, y1, x2, y2, color, size in stroke:
                # simple bounding-box hit check
                if min(x1, x2) - size <= x <= max(x1, x2) + size and min(y1, y2) - size <= y <= max(y1, y2) + size:
                    index = len(self.lines) - 1 - i
                    removed = self.lines.pop(index)
                    self.redo_stack.append(removed)
                    self.redraw_from_lines()
                    return
