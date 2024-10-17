import tkinter as tk
from gui_components import TextInput, TextOutput, LanguageSelector  # Import GUI components

# GUI class to handle the translation application's interface and functionality
class TranslationGUI:
    def __init__(self, root, translator_service):
        """
        Initialize the translation GUI with the provided root window and translation service.
        """
        self.root = root  # Store the Tkinter root window
        self.translator_service = translator_service  # Store the translator service (Hugging Face)

        self.root.title("Translation App")  # Set the window title
        self.root.geometry("700x500")  # Set the default window size
        self.root.config(bg="#f0f0f0")  # Set background color

        # Create the text input box where users can input text to translate
        self.text_input = TextInput(root, "Enter Text to Translate:", height=7, width=60)

        # Create the text output box to display the translated text
        self.text_output = TextOutput(root, "Translated Text:", height=7, width=60)

        # Language options for translation (e.g., English to French, English to German)
        language_options = [
            "English to French (en-fr)",
            "English to German (en-de)",
            "French to English (fr-en)",
            "German to English (de-en)",
            # Add more language pairs as needed
        ]

        # Create the language selector dropdown
        self.language_selector = LanguageSelector(root, "Select Translation Language:", language_options)

        # Create the "Translate" button
        self.translate_button = tk.Button(
            root, text="Translate", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.translate_text
        )
        self.translate_button.pack(pady=20)  # Add padding around the button

        # Create the "Clear" button to reset both input and output boxes
        self.clear_button = tk.Button(
            root, text="Clear", font=("Arial", 14), bg="#f44336", fg="white", command=self.clear_texts
        )
        self.clear_button.pack(pady=10)  # Add padding around the button

    def translate_text(self):
        """
        Method to handle the translation when the "Translate" button is clicked.
        """
        # Retrieve the text from the input box
        text_to_translate = self.text_input.get_text()

        # Retrieve the selected source and target languages
        selected_language = self.language_selector.get_selected_language()
        src_lang, tgt_lang = selected_language.split('-')  # Split language pair (e.g., "en-fr")

        # If there is no text, do nothing
        if not text_to_translate:
            return

        # Perform the translation using the provided service
        translated_text = self.translator_service.translate(text_to_translate, src_lang=src_lang, tgt_lang=tgt_lang)

        # Set the translated text in the output box
        self.text_output.set_text(translated_text)

    def clear_texts(self):
        """
        Method to clear the text input and output boxes when the "Clear" button is clicked.
        """
        self.text_input.clear_text()  # Clear input text
        self.text_output.clear_text()  # Clear output text
