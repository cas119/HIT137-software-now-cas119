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

# Class for the output text box where the translated text will be displayed
# Single Inheritence
class TextOutput(BaseGUIComponent):
    def __init__(self, root, label_text, height=7, width=60):
        super().__init__(root)  # Initialize the base component
        # Create a frame to hold the output text
        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(fill=tk.BOTH, padx=20, pady=5, expand=True)

        # Create and configure the label for the text output
        self.label = tk.Label(self.frame, text=label_text, font=("Arial", 14), bg="#f0f0f0")
        self.label.pack(anchor="w")

        # Create and configure the output text widget (initially disabled)
        self.text_widget = tk.Text(self.frame, height=height, width=width, font=("Arial", 12), wrap="word", state='disabled')
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create and configure a scrollbar for the text output
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

    # Method to set the translated text in the output box
    def set_text(self, text):
        self.text_widget.config(state='normal')  # Enable editing
        self.text_widget.delete("1.0", tk.END)  # Clear existing text
        self.text_widget.insert(tk.END, text)  # Insert the new translated text
        self.text_widget.config(state='disabled')  # Disable editing again

    # Method to clear the text in the output box
    # Polymorphism: Overriding
    def clear_text(self):
        self.text_widget.config(state='normal')
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.config(state='disabled')

# Class for the language selection dropdown
# Single Inheritence
class LanguageSelector(BaseGUIComponent):
    def __init__(self, root, label_text, languages):
        super().__init__(root)  # Initialize the base component
        # Create a frame to hold the language selector
        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(pady=10)

        # Create and configure the label for the language selector
        self.label = tk.Label(self.frame, text=label_text, font=("Arial", 12), bg="#f0f0f0")
        self.label.grid(row=0, column=0, padx=10)

        # Create and configure the dropdown (Combobox) for language selection
        self.language_combo = ttk.Combobox(self.frame, values=languages, state='readonly', width=30)
        self.language_combo.grid(row=0, column=1, padx=10)
        self.language_combo.current(0)  # Set the default selection to the first language

    # Method to retrieve the selected language
    def get_selected_language(self):
        return self.language_combo.get().split(' ')[-1][1:-1]
