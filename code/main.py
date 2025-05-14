import tkinter as tk
import json #pentru setari

from helpers import load_language #progamer
from helpers import load_user_language
from dashboard import Dashboard

def open_dashboard():
    dashboard = Dashboard(root, strings)


strings = load_language("english")

root = tk.Tk()
root.title("myNotes")
root.geometry("1280x720")


main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

sidebar = Dashboard(main_frame, strings)
sidebar.pack(side="left", fill="y")

content = tk.Frame(main_frame, bg="white")
content.pack(side="right", fill="both", expand=True)




menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New")
filemenu.add_command(label="Open")
filemenu.add_command(label="Export")
filemenu.add_separator()
filemenu.add_command(label="Exit", command = root.quit)
menubar.add_cascade(label="File", menu=filemenu)



greeting = tk.Label(content, text = strings["s1"])
greeting.grid(row = 0, column = 1)


btn_open = tk.Button(content, text = "Dashboard", command = open_dashboard)
btn_open.grid(row = 0, column = 0)

root.config(menu=menubar)
root.mainloop()