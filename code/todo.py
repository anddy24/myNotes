import tkinter as tk
import os
import customtkinter as ctk

CACHE_FILE = "todo_cache.txt"

class TodoFrame(tk.Frame):
    def __init__(self, master, strings, theme_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme_manager = theme_manager
        self.configure(bg=self.theme_manager.get_color("background"))

        self.entry = tk.Entry(self, bg =self.theme_manager.get_color("current_line"), font=("Arial", 12),
                              fg = self.theme_manager.get_color("foreground"))
        self.entry.pack(pady=10, padx=10, fill="x")

        self.entry.bind("<Return>", lambda event: self.add_task())

        button_frame = tk.Frame(self, bg=self.theme_manager.get_color("background"))
        button_frame.pack(fill="x", padx=10, pady=5)

        self.add_button = ctk.CTkButton(button_frame, text="Add", corner_radius=10, command=self.add_task,
                                        fg_color=self.theme_manager.get_color("comment"))
        self.add_button.grid(row=0, column=0, sticky="w")

        self.delete_button = ctk.CTkButton(button_frame, text="Delete Completed", corner_radius=10, command=self.delete_completed,
                                           fg_color=self.theme_manager.get_color("comment"))
        self.delete_button.grid(row=0, column=1, sticky="e")

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.tasks_frame = tk.Frame(self, bg=self.theme_manager.get_color("background"))
        self.tasks_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tasks = []
        self._load_tasks()
    
    def delete_completed(self):
        to_keep = []
        for text, var, check in self.tasks:
            if var.get():
                check.destroy()  # Remove widget from UI
            else:
                to_keep.append((text, var, check))
        self.tasks = to_keep
        self._save_tasks()

    def add_task(self):
        task_text = self.entry.get().strip()
        if task_text:
            self.entry.delete(0, tk.END)
            self._create_task(task_text)
            self._save_tasks()

    def _create_task(self, text):
        var = tk.BooleanVar()
        check = tk.Checkbutton(
            self.tasks_frame,
            text=text,
            variable=var,
            font=("Arial", 12),
            anchor="w",
            bg=self.theme_manager.get_color("background"),
            fg=self.theme_manager.get_color("foreground"),
            selectcolor=self.theme_manager.get_color("background")  # Important for the checked box bg
        )
        check.pack(anchor="w", pady=2)
        self.tasks.append((text, var, check))

    def _save_tasks(self):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            for text, var, _ in self.tasks:  # unpacking 3 values
                f.write(f"{text}\n")

    def _load_tasks(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    self._create_task(line.strip())
