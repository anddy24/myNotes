# notes.py
import tkinter as tk
import os

CACHE_FILE = "notes_cache.txt"

class NotesFrame(tk.Frame):
    def __init__(self, master, strings, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(bg="white")

        self.text_area = tk.Text(self, wrap="word", font=("Arial", 12))
        self.text_area.pack(fill="both", expand=True, padx=10, pady=10)

        self.text_area.bind("<<Modified>>", self.auto_save)

        self._load_cached_text()

    def auto_save(self, event=None):
        self.text_area.edit_modified(False)  # Reset modified flag
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            f.write(self.text_area.get("1.0", tk.END).strip())

    def _load_cached_text(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_area.insert("1.0", content)
