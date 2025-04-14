import tkinter as tk
from tkinter import colorchooser
from drawing_stack import UndoRedoStack
from tkinter import filedialog
from PIL import Image, ImageGrab
import os

# This is a simple drawing application using Tkinter.
# It allows users to draw on a canvas, choose colors, and undo/redo actions.
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Paint Tool 🎨")

        self.color = "black"
        self.brush_size = 3
        self.last_x, self.last_y = None, None
        self.current_stroke = []
        
        self.mode = "draw"  # default mode
        self.bg_color = "white"  # eraser will draw using this background color

        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack(pady=10)

        self.stack = UndoRedoStack()

        self.canvas.bind("<Button-1>", self.set_start)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_stroke)

        self.create_ui()

    # Create UI elements
    def create_ui(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack()

        tk.Button(toolbar, text="Undo", command=self.undo).pack(side=tk.LEFT, padx=5) # Undo button
        tk.Button(toolbar, text="Redo", command=self.redo).pack(side=tk.LEFT, padx=5) # Redo button
        tk.Button(toolbar, text="Color", command=self.choose_color).pack(side=tk.LEFT, padx=5) # Color picker button
        tk.Button(toolbar, text="Save", command=self.save_canvas).pack(side=tk.LEFT, padx=5) # Save button
        tk.Button(toolbar, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5) # Clear button
        tk.Button(toolbar, text="Eraser", command=self.enable_eraser_mode).pack(side=tk.LEFT, padx=5) # Eraser button
        tk.Button(toolbar, text="Draw", command=self.enable_draw_mode).pack(side=tk.LEFT, padx=5) # Draw button

        self.brush_size_var = tk.IntVar(value=self.brush_size)
        tk.Spinbox(toolbar, from_=1, to=10, textvariable=self.brush_size_var, width=5, command=self.set_brush_size).pack(side=tk.LEFT)
    
    # Method to enable draw mode
    def enable_draw_mode(self):
        self.mode = "draw"

    # Method to enable eraser mode
    def set_start(self, event):
        self.last_x, self.last_y = event.x, event.y
        self.current_stroke = []

    # Method to set the starting point of the stroke
    def draw(self, event):
        if self.mode not in ["draw", "eraser"]:
            return

        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            color = self.bg_color if self.mode == "eraser" else self.color
            line = self.canvas.create_line(self.last_x, self.last_y, x, y, fill=color, width=self.brush_size)
            self.current_stroke.append((line, self.last_x, self.last_y, x, y, color, self.brush_size))
        self.last_x, self.last_y = x, y

    # Method to set the end point of the stroke
    def end_stroke(self, event):
        if self.current_stroke:
            # Add the whole stroke to undo stack
            self.stack.add_action(("stroke", self.current_stroke))
        self.current_stroke = []

    # Method to choose color
    def choose_color(self):
        chosen = colorchooser.askcolor(title="Pick a Color")
        if chosen[1]:
            self.color = chosen[1]

    # Method to set the brush size
    def set_brush_size(self):
        self.brush_size = self.brush_size_var.get()
    
    # Method to enable eraser mode
    def enable_eraser_mode(self):
        self.mode = "eraser"

    # Method to undo the last action
    def undo(self):
        action = self.stack.undo()
        if action and action[0] == "stroke":
            for line, *_ in action[1]:
                self.canvas.delete(line)

    # Method to redo the last undone action
    def redo(self):
        action = self.stack.redo()
        if action and action[0] == "stroke":
            new_stroke = []
            for _, x1, y1, x2, y2, color, width in action[1]:
                line = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)
                new_stroke.append((line, x1, y1, x2, y2, color, width))
            # Re-add stroke to undo stack
            self.stack.undo_stack[-1] = ("stroke", new_stroke)
    # Method to save the canvas as an image      
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
    
    # Method to clear the canvas
    def clear_canvas(self):
        self.canvas.delete("all")
        self.stack.undo_stack.clear()
        self.stack.redo_stack.clear()


# Method to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
