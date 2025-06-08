import tkinter as tk
from tkinter import messagebox
import json
import os

SETTINGS_FILE = "private_settings.json"
THEME_FILE = "themes/themes.json"

class ThemeManager:
    def __init__(self):
        self._load_themes()
        self.active_theme_name = self._load_selected_theme()
        self.active_theme = self.themes.get(self.active_theme_name, {})
        self._subscribers = []

    def _load_themes(self):
        if os.path.exists(THEME_FILE):
            with open(THEME_FILE, "r") as f:
                self.themes = json.load(f)
        else:
            self.themes = {}

    def _load_selected_theme(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                try:
                    return json.load(f).get("theme", "Dracula")
                except json.JSONDecodeError:
                    return "Dracula"
        return "Dracula"

    def save_selected_theme(self):
        settings = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                try:
                    settings = json.load(f)
                except json.JSONDecodeError:
                    settings = {}
        settings["theme"] = self.active_theme_name
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)

    def subscribe(self, widget):
        """Register a widget/frame to get notified on theme changes."""
        if widget not in self._subscribers:
            self._subscribers.append(widget)

    def unsubscribe(self, widget):
        if widget in self._subscribers:
            self._subscribers.remove(widget)

    def apply_theme(self, theme_name):
        if theme_name not in self.themes:
            return  # invalid theme

        self.active_theme_name = theme_name
        self.active_theme = self.themes[theme_name]
        self.save_selected_theme()

        # Notify all subscribers to update their colors
        for widget in self._subscribers:
            if hasattr(widget, "update_theme"):
                widget.update_theme(self.active_theme)

    def get_color(self, key):
        return self.active_theme.get(key, "#FFFFFF")

class SettingsFrame(tk.Frame):
    def __init__(self, master, strings, theme_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.strings = strings
        self.theme_manager = theme_manager
        self.theme_manager.subscribe(self)
        self.configure(bg=self.theme_manager.get_color("background"))
        
        self.current_theme = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Setup private button
        setup_btn = tk.Button(self, text=self.strings.get("setup_private", "Set up Private Notes"),
                              command=self.open_setup_window, bg=self.theme_manager.get_color("button_bg"))
        setup_btn.pack(pady=20)

        # Theme dropdown
        tk.Label(self, text="Select Theme:", bg=self.theme_manager.get_color("background"), 
                 fg=self.theme_manager.get_color("foreground")).pack()

        self.theme_options = self.get_available_themes()
        self.current_theme.set("Monokai")

        theme_menu = tk.OptionMenu(self, self.current_theme, *self.theme_options, command=self.apply_theme)
        theme_menu.pack(pady=10)

    def get_available_themes(self):
        if os.path.exists(THEME_FILE):
            with open(THEME_FILE, "r") as f:
                return list(json.load(f).keys())
        return []

    def load_theme(self, theme_name):
        if not os.path.exists(THEME_FILE):
            return
        with open(THEME_FILE, "r") as f:
            themes = json.load(f)
        self.theme = themes.get(theme_name, {})

    def apply_theme(self, theme_name):
        self.theme_manager.apply_theme(theme_name)
    
    def update_theme(self, theme):
        self.configure(bg=self.theme_manager.get_color("background"))
        for widget in self.winfo_children():
            try:
                widget.configure(
                    bg=self.theme_manager.get_color("background"),
                    fg=self.theme_manager.get_color("foreground")
                )
            except:
                pass


    def open_setup_window(self):
        window = tk.Toplevel(self)
        window.title("Private Setup")
        window.geometry("300x250")
        window.configure(bg=self.theme_manager.get_color("background"))

        def styled_label(text):
            return tk.Label(window, text=text, bg=self.theme_manager.get_color("background"), fg=self.theme_manager.get_color("foreground"))

        styled_label("Email:").pack(pady=5)
        email_entry = tk.Entry(window)
        email_entry.pack()

        styled_label("Password:").pack(pady=5)
        password_entry = tk.Entry(window, show="*")
        password_entry.pack()

        styled_label("Repeat Password:").pack(pady=5)
        confirm_entry = tk.Entry(window, show="*")
        confirm_entry.pack()

        def save_settings():
            email = email_entry.get()
            pwd1 = password_entry.get()
            pwd2 = confirm_entry.get()

            if not email or not pwd1 or not pwd2:
                messagebox.showerror("Error", "All fields are required.")
                return

            if pwd1 != pwd2:
                messagebox.showerror("Error", "Passwords do not match.")
                return

            with open(SETTINGS_FILE, "w") as f:
                json.dump({"email": email, "password": pwd1}, f)

            messagebox.showinfo("Success", "Private folder credentials saved.")
            window.destroy()

        tk.Button(window, text="Save", command=save_settings,
                  bg=self.theme_manager.get_color("button_bg")).pack(pady=10)
