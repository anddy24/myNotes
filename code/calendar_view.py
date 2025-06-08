import tkinter as tk
import calendar
from datetime import datetime

class CalendarFrame(tk.Frame):
    def __init__(self, master, strings, theme_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme_manager = theme_manager

        self.configure(bg=self.theme_manager.get_color("background"))

        self.theme_manager.subscribe(self)

    def update_theme(self, theme):
        bg = theme.get("background", "white")
        self.configure(bg=bg)

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.header = tk.Label(self, font=("Arial", 16, "bold"), bg="white")
        self.header.pack(pady=10)

        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack()

        self.prev_button = tk.Button(nav_frame, text="<", command=self.prev_month)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = tk.Button(nav_frame, text=">", command=self.next_month)
        self.next_button.grid(row=0, column=1, padx=5)

        self.calendar_frame = tk.Frame(self, bg="white")
        self.calendar_frame.pack(pady=10)

        self.update_calendar()

    def update_calendar(self):
        # Clear current calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.header.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        # Days header
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Arial", 10, "bold"), bg="white").grid(row=0, column=i)

        # Calendar days
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self.current_year, self.current_month)

        for r, week in enumerate(month_days, 1):
            for c, day in enumerate(week):
                text = str(day) if day != 0 else ""
                tk.Label(self.calendar_frame, text=text, width=4, height=2, bg="white", font=("Arial", 10)).grid(row=r, column=c)

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()
