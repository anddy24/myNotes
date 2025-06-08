import tkinter as tk
from tkinter import messagebox
import json
import os
from notes import NotesFrame  

SETTINGS_FILE = "private_settings.json"
PRIVATE_NOTE_FILE = "private_note.txt"

class PrivateFrame(tk.Frame):
    def __init__(self, master, strings, theme_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.strings = strings
        self.master = master
        self.theme_manager = theme_manager

        self.configure(bg=self.theme_manager.get_color("background"))

        self.password_prompt()

    def password_prompt(self):
        self.clear_widgets()

        tk.Label(self, text=self.strings.get("enter_password", "Enter Password:"), bg="white").pack(pady=10)
        self.pwd_entry = tk.Entry(self, show="*")
        self.pwd_entry.pack()
        tk.Button(self, text="Unlock", command=self.verify_password).pack(pady=10)

    def verify_password(self):
        pwd = self.pwd_entry.get()
        if not os.path.exists(SETTINGS_FILE):
            messagebox.showerror("Error", "Private settings not found.")
            return

        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)

        if pwd == settings.get("password"):
            self.load_private_editor()
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def load_private_editor(self):
        self.clear_widgets()

        # Reuse the NotesFrame, but store in a different file
        self.notes = NotesFrame(self, self.strings, self.theme_manager, file_path=PRIVATE_NOTE_FILE)
        self.notes.pack(fill="both", expand=True)

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
