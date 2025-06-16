import tkinter as tk
import json

class WeeklyCalendar(tk.Frame):
    def __init__(self, master, schedule_path="calendar.json", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.schedule = self.load_schedule(schedule_path)
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.draw_calendar()

    def load_schedule(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        return data["schedule"]

    def draw_calendar(self):
        for col, day in enumerate(self.days):
            # Day label
            tk.Label(self, text=day, font=("Arial", 10, "bold")).grid(row=0, column=col+1, padx=2, pady=2)

        for hour in range(24):
            # Hour label (first column)
            tk.Label(self, text=f"{hour}:00", font=("Arial", 10)).grid(row=hour+1, column=0, sticky="e")

            for col, day in enumerate(self.days):
                block = tk.Frame(self, width=80, height=25, bg="white", bd=1, relief="solid")
                block.grid_propagate(False)
                block.grid(row=hour+1, column=col+1)

                # Highlight scheduled time
                for item in self.schedule.get(day, []):
                    if item["start"] <= hour < item["end"]:
                        block.configure(bg="#90cdf4")  # Light blue
                        tk.Label(block, text=item["label"], bg="#90cdf4", font=("Arial", 8)).pack()
