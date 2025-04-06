import tkinter as tk
from tkinter import colorchooser
from drawing_stack import UndoRedoStack
from tkinter import filedialog
from PIL import Image, ImageGrab
import os


class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Paint Tool 🎨")

        self.color = "black"
        self.brush_size = 3
        self.last_x, self.last_y = None, None
        self.current_stroke = []

        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack(pady=10)

        self.stack = UndoRedoStack()

        self.canvas.bind("<Button-1>", self.set_start)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_stroke)

        self.create_ui()

    def create_ui(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack()

        tk.Button(toolbar, text="Undo", command=self.undo).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Redo", command=self.redo).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Color", command=self.choose_color).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Save", command=self.save_canvas).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)

        self.brush_size_var = tk.IntVar(value=self.brush_size)
        tk.Spinbox(toolbar, from_=1, to=10, textvariable=self.brush_size_var, width=5, command=self.set_brush_size).pack(side=tk.LEFT)

    def set_start(self, event):
        self.last_x, self.last_y = event.x, event.y
        self.current_stroke = []

    def draw(self, event):
        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            line = self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.color, width=self.brush_size)
            self.current_stroke.append((line, self.last_x, self.last_y, x, y, self.color, self.brush_size))
        self.last_x, self.last_y = x, y

    def end_stroke(self, event):
        if self.current_stroke:
            # Add the whole stroke to undo stack
            self.stack.add_action(("stroke", self.current_stroke))
        self.current_stroke = []

    def choose_color(self):
        chosen = colorchooser.askcolor(title="Pick a Color")
        if chosen[1]:
            self.color = chosen[1]

    def set_brush_size(self):
        self.brush_size = self.brush_size_var.get()

    def undo(self):
        action = self.stack.undo()
        if action and action[0] == "stroke":
            for line, *_ in action[1]:
                self.canvas.delete(line)

    def redo(self):
        action = self.stack.redo()
        if action and action[0] == "stroke":
            new_stroke = []
            for _, x1, y1, x2, y2, color, width in action[1]:
                line = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
                new_stroke.append((line, x1, y1, x2, y2, color, width))
            # Re-add stroke to undo stack
            self.stack.undo_stack[-1] = ("stroke", new_stroke)
            
    def save_canvas(self):
        # Ask the user where to save the image
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            # Get the widget coordinates
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()

            # Grab the canvas region
            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.stack.undo_stack.clear()
        self.stack.redo_stack.clear()



if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
