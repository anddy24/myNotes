import tkinter as tk
from PIL import Image, ImageTk


btn_width = 140
btn_height = 50

class Dashboard(tk.Frame):
    def __init__(self, master, strings, show_frame_callback, theme_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme_manager = theme_manager
        self.show_frame = show_frame_callback
        self.buttons = []  # Store references to buttons for theme updates

        self.configure(width=300, bg=self.theme_manager.get_color("current_line"))
        self.theme_manager.subscribe(self)

        icons = {
            "notes": "sticky-note.png",
            "todo": "list.png",
            "calendar": "calendar.png",
            "whiteboard": "whiteboard.png",
            "private": "data-security.png",
            "settings": "cogwheel.png"
        }

        for i, key in enumerate(["notes", "todo", "calendar", "whiteboard", "private", "settings"]):
            pil_icon = Image.open(f"icons/{icons[key]}")
            pil_icon = pil_icon.resize((24, 24), Image.Resampling.LANCZOS)
            tk_icon = ImageTk.PhotoImage(pil_icon)

            btn = tk.Button(self,
                            text=strings[key],
                            width=btn_width,
                            height=btn_height,
                            bg=self.theme_manager.get_color("current_line"),
                            fg=self.theme_manager.get_color("foreground"),
                            image=tk_icon,
                            compound="left",
                            command=lambda k=key: self.show_frame(k))
            btn.image = tk_icon
            btn.grid(row=i, column=0)
            self.buttons.append(btn)

    def update_theme(self, theme):
        bg = theme.get("current_line", "#FFFFFF")
        fg = theme.get("foreground", "#000000")

        self.configure(bg=bg)
        for btn in self.buttons:
            btn.configure(bg=bg, fg=fg)
