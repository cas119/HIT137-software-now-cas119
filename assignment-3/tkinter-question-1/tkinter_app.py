import tkinter as tk
from translator import HuggingFaceTranslateService  # Import Hugging Face translator service
from translation_gui import TranslationGUI  # Import the GUI for the application

# Main function to set up and run the Tkinter application
def main():
    root = tk.Tk()  # Initialize the main Tkinter window

    # Create an instance of HuggingFaceTranslateService
    # Here we are translating from English (en) to French (fr), you can modify as needed
    translator = HuggingFaceTranslateService(src_lang="en", tgt_lang="fr")

    # Initialize the GUI, passing in the root window and the translation service
    TranslationGUI(root, translator)

    root.mainloop()  # Start the Tkinter event loop

# Entry point of the program
if __name__ == "__main__":
    main()  # Call the main function to run the app
