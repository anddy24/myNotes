import tkinter as tk

class CustomTitleBar(tk.Frame):
    def __init__(self, master, theme_manager, *args, **kwargs):
        self.theme_manager = theme_manager
        bg_color = self.theme_manager.get_color("background")
        fg_color = self.theme_manager.get_color("foreground")
        super().__init__(master, bg=bg_color, height=30, *args, **kwargs)

        self.master = master
        self.bg_color = bg_color
        self.fg_color = fg_color

        # Title label
        self.title_label = tk.Label(self, text="myNotes", bg=bg_color, fg=fg_color)
        self.title_label.pack(side=tk.LEFT, padx=10)

        # Minimize button
        self.btn_min = tk.Button(self, text="—", bg=bg_color, fg=fg_color, bd=0, command=self.minimize)
        self.btn_min.pack(side=tk.RIGHT, padx=5)

        # Maximize/Restore button
        self.btn_max = tk.Button(self, text="❐", bg=bg_color, fg=fg_color, bd=0, command=self.maximize_restore)
        self.btn_max.pack(side=tk.RIGHT, padx=5)

        # Close button
        self.btn_close = tk.Button(self, text="✕", bg=bg_color, fg=fg_color, bd=0, command=self.close)
        self.btn_close.pack(side=tk.RIGHT, padx=5)

        # Bind events for dragging window
        self.bind_events()

        self.is_maximized = False
        self._geom = None

        # Subscribe to theme changes
        self.theme_manager.subscribe(self)

    def update_theme(self, theme):
        bg = theme.get("background", "#1abc9c")
        fg = theme.get("foreground", "white")
        self.configure(bg=bg)
        self.title_label.configure(bg=bg, fg=fg)
        self.btn_min.configure(bg=bg, fg=fg)
        self.btn_max.configure(bg=bg, fg=fg)
        self.btn_close.configure(bg=bg, fg=fg)

    def bind_events(self):
        for widget in (self, self.title_label):
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)
            widget.bind("<Double-Button-1>", self.maximize_restore)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        if self.is_maximized:
            return
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay
        self.master.geometry(f"+{x}+{y}")

    def minimize(self):
        self.master.iconify()

    def maximize_restore(self, event=None):
        if not self.is_maximized:
            self._geom = self.master.geometry()
            self.master.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}+0+0")
            self.is_maximized = True
            self.btn_max.config(text="❐")
        else:
            if self._geom:
                self.master.geometry(self._geom)
            self.is_maximized = False
            self.btn_max.config(text="❐")

    def close(self):
        self.master.destroy()