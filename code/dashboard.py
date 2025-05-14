import tkinter as tk

class Dashboard(tk.Frame):
    def __init__(self, master, strings, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(width=200, bg="lightgray")
        
        # Example content
        label = tk.Label(self, text=strings["s1"], bg="lightgray")
        label.pack(pady=10)

        button = tk.Button(self, text=strings["notes"])  # Like "Settings"
        button.pack(pady=5)