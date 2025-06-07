import tkinter as tk
import os

CACHE_FILE = "todo_cache.txt"

class TodoFrame(tk.Frame):
    def __init__(self, master, strings, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(bg="white")

        self.entry = tk.Entry(self, font=("Arial", 12))
        self.entry.pack(pady=10, padx=10, fill="x")

        self.add_button = tk.Button(self, text=strings.get("add", "Add"), command=self.add_task)
        self.add_button.pack(pady=5)

        self.tasks_frame = tk.Frame(self, bg="white")
        self.tasks_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tasks = []
        self._load_tasks()

    def add_task(self):
        task_text = self.entry.get().strip()
        if task_text:
            self.entry.delete(0, tk.END)
            self._create_task(task_text)
            self._save_tasks()

    def _create_task(self, text):
        var = tk.BooleanVar()
        check = tk.Checkbutton(self.tasks_frame, text=text, variable=var, font=("Arial", 12), anchor="w")
        check.pack(anchor="w", pady=2)
        self.tasks.append((text, var))

    def _save_tasks(self):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            for text, var in self.tasks:
                f.write(f"{text}\n")

    def _load_tasks(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    self._create_task(line.strip())
