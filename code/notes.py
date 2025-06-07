import tkinter as tk
from tkinter import font, colorchooser
import os, json
from tkinter import filedialog
from docx import Document
from reportlab.pdfgen import canvas

class NotesFrame(tk.Frame):


    def __init__(self, master, strings, file_path="notes_cache.json", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.file_path = file_path
        self.configure(bg="white")
        self.cache = self.load_cache()
        self.font_size = self.cache.get("font_size", 12)  # Default font size
        self.text_font = ("Arial", self.font_size)

        self.create_toolbar()
        self.create_text_widget()
        self.load_content()

    def create_toolbar(self):
        toolbar = tk.Frame(self, bg="lightgray")
        toolbar.pack(fill="x")

        tk.Button(toolbar, text="Bold", command=self.make_bold).pack(side="left")
        tk.Button(toolbar, text="Italic", command=self.make_italic).pack(side="left")
        tk.Button(toolbar, text="Underline", command=self.make_underline).pack(side="left")
        tk.Button(toolbar, text="Text Color", command=self.choose_color).pack(side="left")
        tk.Button(toolbar, text="Save", command=self.manual_save).pack(side="right")
        
        export_btn = tk.Button(toolbar, text="Export", command=self.export_notes)
        export_btn.pack(side="left", padx=2)
        
        font_toolbar = tk.Frame(toolbar, bg="lightgray")
        font_toolbar.pack(side="left", padx=5)

        increase_btn = tk.Button(font_toolbar, text="A+", command=self.increase_font)
        increase_btn.pack(side="left")

        decrease_btn = tk.Button(font_toolbar, text="A-", command=self.decrease_font)
        decrease_btn.pack(side="left")


    def create_text_widget(self):
        self.text = tk.Text(self, wrap="word", undo=True)
        self.text.pack(fill="both", expand=True)

        # Default style tags
        self.text.tag_configure("bold", font=font.Font(weight="bold"))
        self.text.tag_configure("italic", font=font.Font(slant="italic"))
        self.text.tag_configure("underline", font=font.Font(underline=True))

        self.text.bind("<KeyRelease>", self.auto_save)

    def make_bold(self): self.apply_tag("bold")
    def make_italic(self): self.apply_tag("italic")
    def make_underline(self): self.apply_tag("underline")

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose text color")[1]
        if color:
            tag = f"color_{color}"
            if tag not in self.text.tag_names():
                self.text.tag_configure(tag, foreground=color)
            self.apply_tag(tag)

    def apply_tag(self, tag):
        try:
            start, end = self.text.index("sel.first"), self.text.index("sel.last")
            self.text.tag_add(tag, start, end)
        except tk.TclError:
            pass

    def auto_save(self, event=None):
        content = self.text.get("1.0", "end-1c")
        tags_data = []

        for tag in self.text.tag_names():
            ranges = self.text.tag_ranges(tag)
            for i in range(0, len(ranges), 2):
                start = ranges[i]
                end = ranges[i + 1]
                tags_data.append({
                    "tag": tag,
                    "start": str(start),
                    "end": str(self.text.index(end))
                })

        save_data = {
            "content": content,
            "tags": tags_data
        }

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=2)

    def manual_save(self):
        self.auto_save()

    def export_notes(self):
        filetypes = [("Text File", "*.txt"), ("Word Document", "*.docx"), ("PDF File", "*.pdf")]
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=filetypes)
    
        if not file_path:
            return  # Cancelled

        content = self.text.get("1.0", tk.END).strip()
    
        if file_path.endswith(".txt"):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        elif file_path.endswith(".docx"):
            doc = Document()
            doc.add_paragraph(content)
            doc.save(file_path)
        elif file_path.endswith(".pdf"):
            c = canvas.Canvas(file_path)
            lines = content.split("\n")
            y = 800
            for line in lines:
                c.drawString(50, y, line)
                y -= 15
            c.save()


    def load_content(self):
        if not os.path.exists(self.file_path):
            return

        with open(self.file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return

        content = data.get("content", "")
        self.text.insert("1.0", content)

        for tag_data in data.get("tags", []):
            tag = tag_data["tag"]
            start = tag_data["start"]
            end = tag_data["end"]

            # Reconfigure any custom color tags
            if tag.startswith("color_") and tag not in self.text.tag_names():
                color = tag.split("_", 1)[1]
                self.text.tag_configure(tag, foreground=color)

            self.text.tag_add(tag, start, end)

    def update_font(self):
        self.text.configure(font=("Arial", self.font_size))
        self.cache["font_size"] = self.font_size
        self.save_cache()

    def increase_font(self):
        self.font_size += 1
        self.update_font()

    def decrease_font(self):
        if self.font_size > 6:
            self.font_size -= 1
            self.update_font()

    def load_cache(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_cache(self):
        current_text = self.text.get("1.0", "end-1c")
        tags_data = []
    
        for tag in self.text.tag_names():
            ranges = self.text.tag_ranges(tag)
            for i in range(0, len(ranges), 2):
                tags_data.append({
                    "tag": tag,
                    "start": str(ranges[i]),
                    "end": str(ranges[i + 1])
                })
    
        self.cache["content"] = current_text
        self.cache["tags"] = tags_data
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2)