import tkinter as tk
import json #pentru setari
from notes import NotesFrame #frame-ul cu notepad

from helpers import load_language #progamer
from helpers import load_user_language
from dashboard import Dashboard


strings = load_language("english")

root = tk.Tk()
root.title("myNotes")
root.geometry("1280x720")

#dictionary for storing frames
content_frames = {}

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)


#frame manager
def show_frame(name):
    # Hide
    for frame in content_frames.values():
        frame.grid_forget()

    if name in content_frames:
        # Show 
        content_frames[name].grid(row=0, column=1, sticky="nsew")
    else:
        # Create
        if name == "notes":
            frame = NotesFrame(content, strings)
        else:
            frame = tk.Frame(content, bg="white")
            tk.Label(frame, text=f"{strings[name]} frame").pack(pady=20)
        frame.grid(row=0, column=1, sticky="nsew")
        content_frames[name] = frame



sidebar = Dashboard(main_frame, strings, show_frame)
sidebar.pack(side="left", fill="y")

content = tk.Frame(main_frame, bg="white")
content.pack(side="right", fill="both", expand=True)




menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)   #file
filemenu.add_command(label="New")
filemenu.add_command(label="Open")
filemenu.add_command(label="Export")
filemenu.add_separator()
filemenu.add_command(label="Exit", command = root.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = tk.Menu(menubar, tearoff=0)   #edit
editmenu.add_command(label="Redo")
editmenu.add_command(label="Undo")
menubar.add_cascade(label="Edit", menu = editmenu)




greeting = tk.Label(content, text = strings["s1"])
greeting.grid(row = 0, column = 1)



root.config(menu=menubar)
root.mainloop()