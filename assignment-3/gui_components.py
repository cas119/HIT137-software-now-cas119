import tkinter as tk
from tkinter import ttk

# Base class for GUI components, providing a common constructor
class BaseGUIComponent:
    def __init__(self, root):
        self.root = root  # Store the Tkinter root window
    
    # Method to clear text (can be overridden)
    def clear_text(self):
        print("Base Class: Text Cleared!")

    # Method to initialize the component (can be overridden)
    def initialize(self):
        print("Base Class: Initialization Done!")

# Class for the input text box where the user enters the text to be translated
# Single Inheritence
class TextInput(BaseGUIComponent):
    def __init__(self, root, label_text, height=7, width=60):
        super().__init__(root)  # Initialize the base component
        # Create a frame to hold the text input
        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(fill=tk.BOTH, padx=20, pady=5, expand=True)

        # Create and configure the label for the text input
        self.label = tk.Label(self.frame, text=label_text, font=("Arial", 14), bg="#f0f0f0")
        self.label.pack(anchor="w")

        # Create and configure the text input widget
        self.text_widget = tk.Text(self.frame, height=height, width=width, font=("Arial", 12), wrap="word")
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create and configure a scrollbar for the text input
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

    # Method to retrieve the text from the input box
    def get_text(self):
        return self.text_widget.get("1.0", tk.END).strip()

    # Method to clear the text in the input box
    # Polymorphism: Overriding
    def clear_text(self):
        self.text_widget.delete("1.0", tk.END)