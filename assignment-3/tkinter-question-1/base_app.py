import tkinter as tk

# Base class for the GUI (Inheriting Tk)
class BaseApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Language Translation App")
        self.geometry("400x300")

    # Method to create widgets - will be overridden in subclasses
    def create_widgets(self):
        pass  # Empty method to be overridden by child classes