import tkinter as tk
from datetime import datetime, timedelta
from calendar_render import WeeklyCalendar
import json
from PIL import Image, ImageTk

class CalendarFrame(tk.Frame):
    def __init__(self, master, strings, theme_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.theme_manager = theme_manager
        self.configure(bg=self.theme_manager.get_color("background"))
        self.theme_manager.subscribe(self)

        self.today = datetime.today()
        self.start_of_week = self.today - timedelta(days=self.today.weekday())

        prev_img = Image.open("icons/previous.png")
        prev_img = prev_img.resize((34, 34), Image.Resampling.LANCZOS)
        self.prev_icon = ImageTk.PhotoImage(prev_img)

        next_img = Image.open("icons/next-week.png")
        next_img = next_img.resize((34, 34), Image.Resampling.LANCZOS)
        self.next_icon = ImageTk.PhotoImage(next_img)

        self._build_ui()

    def _build_ui(self):
        header_frame = tk.Frame(self, bg=self.theme_manager.get_color("background"))
        header_frame.pack(pady=10)

        self.prev_button = tk.Button(
                header_frame,
                image=self.prev_icon,
                command=self.prev_week,
                bg=self.theme_manager.get_color("background"),
                bd=0
            )
        self.prev_button.pack(side="left", padx=5)

        self.header = tk.Label(header_frame, font=("Arial", 16, "bold"),
                            bg=self.theme_manager.get_color("background"),
                            fg=self.theme_manager.get_color("foreground"))
        self.header.pack(side="left", padx=10)

        self.next_button = tk.Button(
            header_frame,
            image=self.next_icon,
            command=self.next_week,
            bg=self.theme_manager.get_color("background"),
            bd=0
        )
        self.next_button.pack(side="left", padx=5)

        self.calendar_frame = tk.Frame(self, bg=self.theme_manager.get_color("background"))
        self.calendar_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.schedule = self.load_schedule("calendar.json")
        self.update_calendar()

    def update_theme(self, theme):
        self.configure(bg=theme.get("background", "white"))
        self.update_calendar()

    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.header.config(text=f"Week of {self.start_of_week.strftime('%B %d, %Y')}")

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Day headers (row 0)
        tk.Label(self.calendar_frame, text="", bg=self.theme_manager.get_color("background")).grid(row=0, column=0)
        for col, day in enumerate(days):
            day_date = self.start_of_week + timedelta(days=col)
            tk.Label(self.calendar_frame, text=f"{day}\n{day_date.day}",
                    font=("Arial", 10, "bold"), bg=self.theme_manager.get_color("comment"),
                    fg=self.theme_manager.get_color("foreground"), width=15, height=2,
                    relief="groove", bd=1).grid(row=0, column=col+1, sticky="nsew")

        schedule = self.get_schedule_for_week()

        # For each day, create a map for quick lookup of events by start hour
        events_by_day = {}
        for day in days:
            events_by_day[day] = []
            for event in schedule.get(day, []):
                events_by_day[day].append(event)

        for hour in range(24):
            tk.Label(self.calendar_frame, text=f"{hour}:00", font=("Arial", 10),
                    bg=self.theme_manager.get_color("background"),
                    fg=self.theme_manager.get_color("foreground")).grid(row=hour+1, column=0, sticky="e")

            # Horizontal separator between hours
            separator = tk.Frame(self.calendar_frame, height=1, bg=self.theme_manager.get_color("accent2"))
            separator.grid(row=hour+1, column=1, columnspan=7, sticky="ew")

            for col, day in enumerate(days):
                block = tk.Frame(self.calendar_frame, width=100, height=25, bd=1, relief="solid")
                block.grid_propagate(False)
                block.grid(row=hour+1, column=col+1, sticky="nsew")

                # Default empty background for empty blocks
                block_bg = self.theme_manager.get_color("current_line")  # Add a lighter background color in your theme

                # Borders default color
                border_color = self.theme_manager.get_color("background")

                # Check if current hour is part of any event for this day
                # Find event which contains current hour (start <= hour < end)
                event_for_hour = None
                for event in events_by_day[day]:
                    if event["start"] <= hour < event["end"]:
                        event_for_hour = event
                        break

                if event_for_hour:
                    # Color the block background with accent1
                    block_bg = self.theme_manager.get_color("comment")

                    # Change border color for event blocks
                    border_color = self.theme_manager.get_color("background")  # Different accent color for borders

                    # Apply border color by using highlight properties of Frame
                    block.configure(bg=block_bg, bd=1)
                else:
                    # No event at this hour, just normal background and border thickness 1
                    block.configure(bg=block_bg, bd=0)

                # Add right and bottom borders as before (optional, since we set highlightthickness)
                # You can remove these if the highlight border looks good enough
                right_border = tk.Frame(block, width=1, bg=border_color)
                right_border.pack(side="right", fill="y")
                #bottom_separator = tk.Frame(block, height=1, bg=border_color)
                #bottom_separator.pack(side="bottom", fill="x")

                # Now add the label only if this is the starting hour of the event
                if event_for_hour and hour == event_for_hour["start"]:
                    tk.Label(block, text=event_for_hour["label"], bg=block_bg, fg= self.theme_manager.get_color("foreground"),
                            font=("Arial", 8, "bold"), anchor="w").pack(side="top", fill="x", padx=2, pady=1)

        for i in range(8):
            self.calendar_frame.columnconfigure(i, weight=1)
        for i in range(25):
            self.calendar_frame.rowconfigure(i, weight=1)
            
    def load_schedule(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        self.all_schedules = data.get("schedules_by_week", {})
    
    def get_schedule_for_week(self):
        week_key = self.start_of_week.strftime("%Y-%m-%d")
        return self.all_schedules.get(week_key, {day: [] for day in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]})

    def next_week(self):
        self.start_of_week += timedelta(days=7)
        self.update_calendar()

    def prev_week(self):
        self.start_of_week -= timedelta(days=7)
        self.update_calendar()
