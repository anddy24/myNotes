import tkinter as tk
import json #pentru setari
from notes import NotesFrame #frame-ul cu notepad
from todo import TodoFrame #frame-ul to-do
from calendar_view import CalendarFrame #frame-ul cu calendarul
from whiteboard import WhiteboardFrame #frame-ul cu whiteboardul
from settings import SettingsFrame
from settings import ThemeManager
from private import PrivateFrame
from titlebar import CustomTitleBar


from helpers import load_language #progamer
from helpers import load_user_language
from dashboard import Dashboard



strings = load_language("english")
theme_manager = ThemeManager()

root = tk.Tk()
root.overrideredirect(True)
root.title("myNotes")
root.geometry("1280x720")
root.configure(bg=theme_manager.get_color("background"))
#dictionary for storing frames
content_frames = {}


title_bar = CustomTitleBar(root, theme_manager)
title_bar.pack(fill=tk.X)

menu_bar_frame = tk.Frame(root, bg="#2c3e50", height=25)
menu_bar_frame.pack(fill=tk.X)

# Example menu buttons
file_btn = tk.Menubutton(menu_bar_frame, text="File", bg="#2c3e50", fg="white", activebackground="#34495e")
file_btn.pack(side=tk.LEFT, padx=5)

file_menu = tk.Menu(file_btn, tearoff=0)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_command(label="Export")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
file_btn.config(menu=file_menu)

edit_btn = tk.Menubutton(menu_bar_frame, text="Edit", bg="#2c3e50", fg="white", activebackground="#34495e")
edit_btn.pack(side=tk.LEFT, padx=5)

edit_menu = tk.Menu(edit_btn, tearoff=0)
edit_menu.add_command(label="Redo")
edit_menu.add_command(label="Undo")
edit_btn.config(menu=edit_menu)



main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)


#frame manager
def show_frame(name):
    # If frame already exists, destroy it to recreate fresh
    if name in content_frames:
        old_frame = content_frames[name]
        theme_manager.unsubscribe(old_frame)
        old_frame.destroy()
        del content_frames[name]

    # Create new frame instance
    if name == "notes":
        frame = NotesFrame(content, strings, theme_manager)
    elif name == "todo":
        frame = TodoFrame(content, strings, theme_manager)
    elif name == "calendar":
        frame = CalendarFrame(content, strings, theme_manager)
    elif name == "whiteboard":
        frame = WhiteboardFrame(content, strings, theme_manager)
    elif name == "settings":
        frame = SettingsFrame(content, strings, theme_manager)
    elif name == "private":
        frame = PrivateFrame(content, strings, theme_manager)
    else:
        frame = tk.Frame(content, bg="white")
        tk.Label(frame, text=f"{strings[name]} frame").pack(pady=20)

    frame.grid(row=0, column=0, sticky="nsew")
    content_frames[name] = frame



sidebar = Dashboard(main_frame, strings, show_frame, theme_manager)
sidebar.pack(side="left", fill="y")

content = tk.Frame(main_frame, bg="white")
content.pack(side="right", fill="both", expand=True)

#grid black magic
content.grid_rowconfigure(0, weight=1)
content.grid_columnconfigure(0, weight=1)

root.mainloop()