# This module implements a stack for managing undo and redo actions in the Mini Paint App.
class UndoRedoStack:
    # Initialize the stack with empty undo and redo stacks
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    # Add an action to the undo stack and clear the redo stack of that action if it's in it
    # This ensures that the redo stack only contains actions that have been undone
    def add_action(self, action):
        self.undo_stack.append(action)
        self.redo_stack.clear()

    # Undo the last action by popping from the undo stack and pushing it to the redo stack
    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            self.redo_stack.append(action)
            return action
        return None

    # Redo the last undone action by popping from the redo stack and pushing it to the undo stack
    # This allows the user to redo an action that was previously undone
    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            self.undo_stack.append(action)
            return action
        return None

    # Getters for the undo and redo stacks
    # These methods allow access to the current state of the stacks without modifying them
    def get_undo_stack(self):
        return self.undo_stack

    def get_redo_stack(self):
        return self.redo_stack
