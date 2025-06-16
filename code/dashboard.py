import tkinter as tk
from PIL import Image, ImageTk

btn_width = 140
btn_height = 50

class Dashboard(tk.Frame):
    def __init__(self, master, strings, show_frame_callback, theme_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme_manager = theme_manager
        self.show_frame = show_frame_callback
        self.buttons = []
        self.indicators = {}
        self.tab_positions = {}
        self.current_tab = None
        self.expanded = True
        self.expanded_width = 170
        self.collapsed_width = 50

        self.configure(width=self.expanded_width, bg=self.theme_manager.get_color("current_line"))
        self.theme_manager.subscribe(self)

        # Menu toggle button
        menu_icon = Image.open("icons/menu.png")
        menu_icon = menu_icon.resize((24, 24), Image.Resampling.LANCZOS)
        self.menu_icon = ImageTk.PhotoImage(menu_icon)

        self.toggle_button = tk.Button(self,
                                       image=self.menu_icon,
                                       bg=self.theme_manager.get_color("current_line"),
                                       activebackground=self.theme_manager.get_color("comment"),
                                       bd=0,
                                       command=self.toggle_dashboard)
        self.toggle_button.pack(side="top", anchor="w", padx=10, pady=10)
         
        # Border on the right side
        border_frame = tk.Frame(self, width=2, bg=self.theme_manager.get_color("comment"))
        border_frame.pack(side="right", fill="y")

        # Accent indicator bar
        self.active_indicator = tk.Frame(self, width=5, bg=self.theme_manager.get_color("accent1"))
        self.active_indicator.place(x=0, y=0, height=btn_height)

        icons = {
            "notes": "sticky-note.png",
            "todo": "list.png",
            "calendar": "calendar.png",
            "whiteboard": "whiteboard.png",
            "private": "data-security.png",
            "settings": "cogwheel.png"
        }

        tab_keys = list(icons.keys())
        for i, key in enumerate(tab_keys):
            y_pos = i * btn_height + 60  # Adjust for top button height
            self.tab_positions[key] = y_pos

            pil_icon = Image.open(f"icons/{icons[key]}")
            pil_icon = pil_icon.resize((24, 24), Image.Resampling.LANCZOS)
            tk_icon = ImageTk.PhotoImage(pil_icon)

            row_frame = tk.Frame(self, bg=self.theme_manager.get_color("current_line"))
            row_frame.pack(fill="x")

            indicator = tk.Frame(row_frame, width=5, bg=self.theme_manager.get_color("current_line"))
            indicator.pack(side="left", fill="y")
            self.indicators[key] = indicator

            btn = tk.Button(row_frame,
                            text=strings[key],
                            width=btn_width,
                            height=btn_height,
                            bg=self.theme_manager.get_color("current_line"),
                            fg=self.theme_manager.get_color("foreground"),
                            image=tk_icon,
                            compound="left",
                            anchor="w",
                            padx=15,
                            bd=0,
                            command=lambda k=key: self.select_tab(k))
            btn.full_text = strings[key]
            btn.configure(text=btn.full_text)
            btn.image = tk_icon
            btn.pack(side="left", fill="x", expand=True)
            self.buttons.append(btn)

            def on_enter(e, btn=btn):
                btn.configure(bg=self.theme_manager.get_color("comment"), fg="white")

            def on_leave(e, btn=btn):
                btn.configure(bg=self.theme_manager.get_color("current_line"), fg=self.theme_manager.get_color("foreground"))

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Select default tab (first one)
        self.select_tab(tab_keys[0])

    def toggle_dashboard(self):
        self.expanded = not self.expanded
        new_width = self.expanded_width if self.expanded else self.collapsed_width
        self.configure(width=new_width)
        self.pack_propagate(False)

        for btn in self.buttons:
            if self.expanded:
                btn.configure(text=btn.full_text, anchor="w", padx=15, justify="left")
            else:
                btn.configure(text="", anchor="center", padx=0)

    def select_tab(self, key):
        if key == self.current_tab:
            return
        self.current_tab = key
        self.show_frame(key)

        for tab, indicator in self.indicators.items():
            color = self.theme_manager.get_color("accent1") if tab == key else self.theme_manager.get_color("current_line")
            indicator.configure(bg=color)

        target_y = self.tab_positions.get(key, 0)
        self.animate_indicator(current_y=self.active_indicator.winfo_y(), target_y=target_y)

    def animate_indicator(self, current_y, target_y, step=5):
        if abs(current_y - target_y) < step:
            self.active_indicator.place_configure(y=target_y)
            return
        direction = step if target_y > current_y else -step
        new_y = current_y + direction
        self.active_indicator.place_configure(y=new_y)
        self.after(10, lambda: self.animate_indicator(new_y, target_y, step))

    def update_theme(self, theme):
        bg = theme.get("current_line", "#FFFFFF")
        fg = theme.get("foreground", "#000000")
        accent = theme.get("accent1", "#FF0000")

        self.configure(bg=bg)
        self.toggle_button.configure(bg=bg, activebackground=theme.get("comment", "#CCCCCC"))

        for btn in self.buttons:
            btn.configure(bg=bg, fg=fg)

        for key, indicator in self.indicators.items():
            color = accent if key == self.current_tab else bg
            indicator.configure(bg=color)
        self.active_indicator.configure(bg=accent)
