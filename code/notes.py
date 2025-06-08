import tkinter as tk
from tkinter import font, colorchooser
import os, json
from tkinter import filedialog
from docx import Document
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk


class NotesFrame(tk.Frame):


    def __init__(self, master, strings, theme_manager, file_path="notes_cache.json", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.file_path = file_path
        self.theme_manager = theme_manager
        self.configure(bg=self.theme_manager.get_color("background"))
        self.cache = self.load_cache()
        self.font_size = self.cache.get("font_size", 12)  # Default font size
        self.text_font = ("Arial", self.font_size)

        self.create_toolbar()
        self.create_text_widget()
        self.load_content()
        self.theme_manager.subscribe(self)
    
    def update_theme(self, theme):
        bg = theme.get("background", "#FFFFFF")
        self.configure(bg=bg)

    def create_toolbar(self):
        toolbar = tk.Frame(self, bg=self.theme_manager.get_color("background"), pady=5)
        toolbar.pack(fill="x")

        # Font family dropdown
        font_var = tk.StringVar(value="Calibri (Body)")
        font_dropdown = tk.OptionMenu(toolbar, font_var, "Arial", "Calibri", "Times New Roman", "Courier New")
        font_dropdown.config(bg=self.theme_manager.get_color("background"), fg=self.theme_manager.get_color("foreground"), highlightthickness=0, bd=0)
        font_dropdown["menu"].config(bg=self.theme_manager.get_color("current_line"), fg=self.theme_manager.get_color("foreground"),bd=0)
        font_dropdown.pack(side="left", padx=2)


        # Font size dropdown
        size_var = tk.StringVar(value="10")
        size_dropdown = tk.OptionMenu(toolbar, size_var, *map(str, range(8, 33)))
        size_dropdown.config(bg=self.theme_manager.get_color("background"), fg=self.theme_manager.get_color("foreground"), highlightthickness=0, bd=0)
        size_dropdown["menu"].config(bg=self.theme_manager.get_color("current_line"), fg=self.theme_manager.get_color("foreground"), bd=0)
        size_dropdown.pack(side="left", padx=2)

        def load_icon(path, size=(16, 16)):
            pil_img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(pil_img)

        def apply_hover_effect(button, hover_bg=self.theme_manager.get_color("current_line"), normal_bg=None):
            if normal_bg is None:
                normal_bg = button["bg"]

            def on_enter(e):
                e.widget["bg"] = hover_bg

            def on_leave(e):
                e.widget["bg"] = normal_bg

            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

        # Preload all icons
        font_up = load_icon("icons/font-size.png")
        font_down = load_icon("icons/font-size(1).png")
        font_bold = load_icon("icons/bold.png")
        font_italic = load_icon("icons/italic.png")
        font_underline = load_icon("icons/underline.png")
        font_bg = load_icon("icons/highlighter.png")
        font_color = load_icon("icons/text.png")
        font_plus = load_icon("icons/superscript.png")
        font_minus = load_icon("icons/subscript.png")
        save = load_icon("icons/save.png")
        export = load_icon("icons/export.png")

        # A+ (Increase font)
        btn_increase = tk.Button(toolbar, image=font_up, bg=self.theme_manager.get_color("background"),
                                fg=self.theme_manager.get_color("foreground"), command=self.increase_font,
                                bd=0, highlightthickness=0)
        btn_increase.image = font_up
        btn_increase.pack(side="left", padx=6)
        apply_hover_effect(btn_increase, hover_bg=self.theme_manager.get_color("current_line"))

        # A- (Decrease font)
        btn_decrease = tk.Button(toolbar, image=font_down, bg=self.theme_manager.get_color("background"),
                                fg=self.theme_manager.get_color("foreground"), command=self.decrease_font,
                                bd=0, highlightthickness=0)
        btn_decrease.image = font_down
        btn_decrease.pack(side="left", padx=6)
        apply_hover_effect(btn_decrease, hover_bg=self.theme_manager.get_color("current_line"))


        # Formatting buttons
        btn_bold = tk.Button(toolbar, image=font_bold, bg=self.theme_manager.get_color("background"),
                            fg=self.theme_manager.get_color("foreground"), command=self.make_bold,
                            bd=0, highlightthickness=0)
        btn_bold.image = font_bold
        btn_bold.pack(side="left", padx=6)
        apply_hover_effect(btn_bold, hover_bg=self.theme_manager.get_color("current_line"))

        btn_italic = tk.Button(toolbar, image=font_italic, bg=self.theme_manager.get_color("background"),
                            fg=self.theme_manager.get_color("foreground"), command=self.make_italic,
                            bd=0, highlightthickness=0)
        btn_italic.image = font_italic
        btn_italic.pack(side="left", padx=6)
        apply_hover_effect(btn_italic, hover_bg=self.theme_manager.get_color("current_line"))

        btn_underline = tk.Button(toolbar, image=font_underline, bg=self.theme_manager.get_color("background"),
                                fg=self.theme_manager.get_color("foreground"), command=self.make_underline,
                                bd=0, highlightthickness=0)
        btn_underline.image = font_underline 
        btn_underline.pack(side="left", padx=6)
        apply_hover_effect(btn_underline, hover_bg=self.theme_manager.get_color("current_line"))

        # Superscript
        btn_sup = tk.Button(toolbar, image=font_plus, bg=self.theme_manager.get_color("background"),
                            fg=self.theme_manager.get_color("foreground"), command=self.apply_superscript,
                            bd=0, highlightthickness=0)
        btn_sup.image = font_plus
        btn_sup.pack(side="left", padx=6)
        apply_hover_effect(btn_sup, hover_bg=self.theme_manager.get_color("current_line"))
        

        # Subscript
        btn_sub = tk.Button(toolbar, image=font_minus, bg=self.theme_manager.get_color("background"),
                            fg=self.theme_manager.get_color("foreground"), command=self.apply_subscript,
                            bd=0, highlightthickness=0)
        btn_sub.image = font_minus
        btn_sub.pack(side="left", padx=6)
        apply_hover_effect(btn_sub, hover_bg=self.theme_manager.get_color("current_line"))

        # Font color
        btn_color = tk.Button(toolbar, image=font_color, bg=self.theme_manager.get_color("background"),
                            fg=self.theme_manager.get_color("foreground"), command=self.choose_color,
                            bd=0, highlightthickness=0)
        btn_color.image = font_color
        btn_color.pack(side="left", padx=6)
        apply_hover_effect(btn_color, hover_bg=self.theme_manager.get_color("current_line"))

        # Highlight
        btn_highlight = tk.Button(toolbar, image=font_bg, bg=self.theme_manager.get_color("background"),
                                fg=self.theme_manager.get_color("foreground"), command=self.highlight_text,
                                bd=0, highlightthickness=0)
        btn_highlight.image = font_bg
        btn_highlight.pack(side="left", padx=6)
        apply_hover_effect(btn_highlight, hover_bg=self.theme_manager.get_color("current_line"))


        btn_save = tk.Button(toolbar, image=save, bg=self.theme_manager.get_color("background"),
                            fg=self.theme_manager.get_color("foreground"), command=self.manual_save,
                            bd=0, highlightthickness=0)
        btn_save.image = save
        btn_save.pack(side="right", padx=6)
        apply_hover_effect(btn_save, hover_bg=self.theme_manager.get_color("current_line"))

        btn_export = tk.Button(toolbar, image=export, bg=self.theme_manager.get_color("background"),
                            fg=self.theme_manager.get_color("foreground"), command=self.export_notes,
                            bd=0, highlightthickness=0)
        btn_export.image = export
        btn_export.pack(side="right", padx=6)
        apply_hover_effect(btn_export, hover_bg=self.theme_manager.get_color("current_line"))



    def create_text_widget(self):
        self.text = tk.Text(self, wrap="word", undo=True)
        self.text.pack(fill="both", expand=True)
        self.text.configure(bg=self.theme_manager.get_color("background"),
                            fg=self.theme_manager.get_color("foreground"))

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

    
    def highlight_text(self):
        try:
            start = self.text.index("sel.first")
            end = self.text.index("sel.last")
        except tk.TclError:
            return
        
        color_code = colorchooser.askcolor(title="Choose highlight color")[1]
        if not color_code:
            return
        
        tag_name = f"highlight_{color_code}"
        if tag_name not in self.text.tag_names():
            self.text.tag_configure(tag_name, background=color_code)
        self.text.tag_add(tag_name, start, end)


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

        self.text.tag_configure("bold", font=("Arial", self.font_size, "bold"))
        self.text.tag_configure("italic", font=("Arial", self.font_size, "italic"))
        self.text.tag_configure("underline", font=("Arial", self.font_size, "underline"))

        self.cache["font_size"] = self.font_size
        self.save_cache()

    def apply_composite_font(self, start, end, size=None):
        current_tags = self.text.tag_names(start)

        # Defaults
        font_props = {
            "family": "Arial",
            "size": size if size else self.font_size,
            "weight": "normal",
            "slant": "roman",
            "underline": 0
        }

        # Read current styles
        for tag in current_tags:
            try:
                fnt = font.Font(font=self.text.tag_cget(tag, "font"))
                font_props.update({
                    "size": size if size else fnt.actual()["size"],
                    "weight": fnt.actual()["weight"],
                    "slant": fnt.actual()["slant"],
                    "underline": fnt.actual()["underline"]
                })
            except:
                continue

        # New tag name
        tag_name = f'font_{font_props["size"]}_{font_props["weight"]}_{font_props["slant"]}_{font_props["underline"]}'
        if tag_name not in self.text.tag_names():
            self.text.tag_configure(tag_name, font=font.Font(**font_props))

        # Remove old font_* tags
        for tag in current_tags:
            if tag.startswith("font_"):
                self.text.tag_remove(tag, start, end)

        self.text.tag_add(tag_name, start, end)

    def increase_font(self):
        try:
            start, end = self.text.index("sel.first"), self.text.index("sel.last")
            self.apply_composite_font(start, end, size=self.get_current_font_size(start) + 1)
        except tk.TclError:
            pass

    def decrease_font(self):
        try:
            start, end = self.text.index("sel.first"), self.text.index("sel.last")
            new_size = max(6, self.get_current_font_size(start) - 1)
            self.apply_composite_font(start, end, size=new_size)
        except tk.TclError:
            pass   

    def get_current_font_size(self, index):
            tags = self.text.tag_names(index)
            for tag in tags:
                if tag.startswith("font_"):
                    parts = tag.split("_")
                    return int(parts[1])
            return self.font_size
    def load_cache(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def apply_superscript(self):
        try:
            start = self.text.index("sel.first")
            end = self.text.index("sel.last")
        except tk.TclError:
            return
        self.text.tag_add("superscript", start, end)
    
    def apply_subscript(self):
        try:
            start = self.text.index("sel.first")
            end = self.text.index("sel.last")
        except tk.TclError:
            return
        self.text.tag_add("subscript", start, end)




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