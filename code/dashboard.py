import tkinter as tk

btn_width = 20
btn_height = 2

class Dashboard(tk.Frame):
    def __init__(self, master, strings, show_frame_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(width=300, bg="lightgray")
        self.show_frame = show_frame_callback

        button = tk.Button(self, text=strings["notes"], width=btn_width, height=btn_height,
                           command=lambda: self.show_frame("notes"))
        button.grid(row=0, column=0)

        button = tk.Button(self, text=strings["todo"], width=btn_width, height=btn_height,
                           command=lambda: self.show_frame("todo"))
        button.grid(row=1, column=0)

        button = tk.Button(self, text=strings["calendar"], width=btn_width, height=btn_height,
                           command=lambda: self.show_frame("calendar"))
        button.grid(row=2, column=0)

        button = tk.Button(self, text=strings["whiteboard"], width=btn_width, height=btn_height,
                           command=lambda: self.show_frame("whiteboard"))
        button.grid(row=3, column=0)

        button = tk.Button(self, text=strings["private"], width=btn_width, height=btn_height,
                           command=lambda: self.show_frame("private"))
        button.grid(row=4, column=0)

        button = tk.Button(self, text=strings["settings"], width=btn_width, height=btn_height,
                           command=lambda: self.show_frame("settings"))
        button.grid(row=5, column=0)
