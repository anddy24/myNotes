import tkinter as tk
from tkinter import messagebox
import json
import os

SETTINGS_FILE = "private_settings.json"

class SettingsFrame(tk.Frame):
    def __init__(self, master, strings, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(bg="white")

        setup_btn = tk.Button(self, text=strings.get("setup_private", "Set up Private Notes"), command=self.open_setup_window)
        setup_btn.pack(pady=20)

    def open_setup_window(self):
        window = tk.Toplevel(self)
        window.title("Private Setup")
        window.geometry("300x250")

        tk.Label(window, text="Email:").pack(pady=5)
        email_entry = tk.Entry(window)
        email_entry.pack()

        tk.Label(window, text="Password:").pack(pady=5)
        password_entry = tk.Entry(window, show="*")
        password_entry.pack()

        tk.Label(window, text="Repeat Password:").pack(pady=5)
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
                json.dump({"email": email, "password": pwd1}, f)  # You may hash this in a real app

            messagebox.showinfo("Success", "Private folder credentials saved.")
            window.destroy()

        tk.Button(window, text="Save", command=save_settings).pack(pady=10)
