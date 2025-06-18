import tkinter as tk
from tkinter import messagebox
import json
import os
from helpers import load_language
import sys

SETTINGS_FILE = "settings/settings.json"
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
        self.settings = self.load_settings()

        self.language_files = {
            "english": "english",
            "romanian": "romanian",
            "russian": "russian",
            "chinese": "chinese",
            "french": "french",
            "german": "german",
            "italian": "italian",
            "japanese": "japanese",
            "korean": "korean",
            "spanish": "spanish"
        }
        
        self.current_theme = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Setup private button
        setup_btn = tk.Button(self, text=self.strings.get("setup_private", "Set up Private Notes"),
                            command=self.open_setup_window, bd=0, width=40, height=2,
                            fg=self.theme_manager.get_color("foreground"),
                            bg=self.theme_manager.get_color("comment"))
        setup_btn.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Theme label and dropdown
        tk.Label(self, text=self.strings.get("s_theme", "Select Theme:"), bg=self.theme_manager.get_color("background"),
                fg=self.theme_manager.get_color("foreground")).grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.theme_options = self.get_available_themes()
        self.current_theme.set("Dracula")

        theme_menu = tk.OptionMenu(self, self.current_theme, *self.theme_options, command=self.apply_theme)
        theme_menu.config(bg=self.theme_manager.get_color("current_line"), bd=0, width=10, height=2,
                        fg=self.theme_manager.get_color("foreground"))
        theme_menu.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Language label and dropdown
        tk.Label(self, text=self.strings.get("s_lang","Select Language:"), bg=self.theme_manager.get_color("background"),
                fg=self.theme_manager.get_color("foreground")).grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.current_language = tk.StringVar()
        default_lang = list(self.language_files.keys())[0]
        self.current_language.set(default_lang)

        language_menu = tk.OptionMenu(self, self.current_language, *self.language_files.keys(), command=self.apply_language)
        language_menu.config(bg=self.theme_manager.get_color("current_line"), bd=0, width=10, height=2,
                            fg=self.theme_manager.get_color("foreground"))
        language_menu.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Save button
        save_btn = tk.Button(self, text=self.strings.get("sclose","Save Settings and Close App"),
                            command=self.save_current_settings, bd=0, width=20, height=3,
                            bg=self.theme_manager.get_color("comment"), fg=self.theme_manager.get_color("foreground"))
        save_btn.grid(row=3, column=0, columnspan=2, pady=15)

    def apply_language(self, selected_language):
        # Load the language XML file path by language name
        lang_file_path = self.language_files.get(selected_language)
        if lang_file_path:
            self.strings = load_language(lang_file_path)

    def load_settings(self):
            if os.path.exists(SETTINGS_FILE):
                try:
                    with open(SETTINGS_FILE, "r") as f:
                        return json.load(f)
                except json.JSONDecodeError:
                    return {}
            return {}
    def save_current_settings(self):
        selected_lang = self.current_language.get()
        self.settings["language"] = selected_lang

        selected_theme = self.current_theme.get()
        self.settings["theme"] = selected_theme

        self.save_settings(self.settings)
        messagebox.showinfo("Success", "Settings have been saved.")

        python = sys.executable
        os.execl(python, python, *sys.argv)

    def save_settings(self, settings):
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)

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
