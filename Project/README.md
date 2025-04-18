# 🎨 Mini Paint Tool

A simple Python-based drawing app built with `tkinter`. This app allows users to draw on a canvas with customizable colors and brush sizes. It includes features like undo/redo, saving drawings as PNG files, and clearing the canvas.

## 🛠 Requirements

- Python 3.7 or higher
- Pillow (for saving the canvas as an image)

## 📦 Installing Dependencies

To install the required dependencies, follow these steps:

1. **Clone the repository** (or download the files if you have them locally).
2. Navigate to the project directory in your terminal or command prompt.
3. Run the following command to install the required packages:

```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the App
Once the dependencies are installed, you can run the app by using the following command:
```bash
python drawing_app.py
```
## 📂 File Structure
```
project/
├── drawing_app.py       # Main GUI and drawing logic
├── drawing_stack.py     # Undo/redo stack manager
├── requirements.txt     # Python dependency file
└── README.md            # This file
```

## File Descriptions:

- **drawing_app.py**: Contains the logic for the application, including the drawing canvas, undo/redo functionality, and the UI with buttons for saving, clearing, and changing the brush size and color.

- **drawing_stack.py**: Manages the undo and redo stacks for drawing actions (strokes).

- **requirements.txt**: Lists the dependencies required to run the application (currently just Pillow).

- **README.md**: This file, containing all documentation related to the project.

## 💡 Features

### Undo/Redo:
- Undo your last stroke by clicking the Undo button. You can redo strokes by clicking the Redo button.
- Undo and redo actions are maintained as full strokes, not individual lines.

### Color Picker:
- Press the Color button to choose a new color for your brush.

### Brush Size:
- Adjust the brush size using the spinbox to draw thinner or thicker lines.

### Save:
- Export your drawing as a .png image by clicking the Save button.

### Clear:
- Clear the entire canvas and reset all drawing actions by clicking the Clear button.


## 📝 How It Works

### Drawing:
- Press and hold the left mouse button to draw on the canvas. The mouse movement will create a continuous line.
- When you release the mouse button, the drawn path is saved as a "stroke" and can be undone or redone as a whole.

### Undo:
- After drawing, you can undo your most recent stroke by clicking the Undo button. Each click removes one entire stroke.

### Redo:
- Press the Redo button to bring back the last undone stroke. You can redo multiple strokes until the redo stack is empty.

### Saving:
- To save your artwork, click the Save button and select the file location. The canvas will be saved as a .png image.

### Clearing:
- To clear your entire drawing and reset everything, click the Clear button. This will remove all strokes from the canvas and reset the undo/redo history.
