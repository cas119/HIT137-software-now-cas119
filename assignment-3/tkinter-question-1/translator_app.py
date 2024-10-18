import tkinter as tk
from base_app import BaseApp
from model_handler import ModelHandler  # Keep ModelHandler as a parent class
from translation_service import FrenchTranslationService, GermanTranslationService

# Multiple Inheritance: TranslatorApp inherits from both BaseApp (GUI) and ModelHandler (Translation Logic)
class TranslatorApp(BaseApp, ModelHandler):
    def __init__(self):
        # Initialize both BaseApp (GUI) and ModelHandler (Model Logic)
        BaseApp.__init__(self)  # Initialize GUI setup
        ModelHandler.__init__(self)  # Initialize common model handling logic
        self._translation_service = None  # This will store the French or German service
        self.create_widgets()

    # Overriding BaseApp's create_widgets method
    def create_widgets(self):
        self.label = tk.Label(self, text="Enter text to translate:", font=("Helvetica", 12))
        self.label.pack(pady=10)

        self.text_entry = tk.Entry(self, width=50)
        self.text_entry.pack(pady=10)

        self.translate_button_french = tk.Button(self, text="Translate to French", command=self.set_french_service)
        self.translate_button_french.pack(pady=10)

        self.translate_button_german = tk.Button(self, text="Translate to German", command=self.set_german_service)
        self.translate_button_german.pack(pady=10)

        self.result_label = tk.Label(self, text="Translation will appear here.", font=("Helvetica", 12))
        self.result_label.pack(pady=20)

    # Encapsulation: Setter method for assigning the translation service to French
    def set_french_service(self):
        self._translation_service = FrenchTranslationService()  # Polymorphism: set French translation service to _translation_service variable
        self._perform_translation()

    # Encapsulation: Setter method for assigning the translation service to German
    def set_german_service(self):
        self._translation_service = GermanTranslationService()  # Polymorphism: set different German translation service to same _translation_service variable
        self._perform_translation()

    # Encapsulation: Private method to set the translation service
    def _perform_translation(self):
        """Use the current translation service to translate the input text."""
        input_text = self.text_entry.get()
        if self._translation_service:
            translation = self._translation_service.translate(input_text)  # Polymorphism: Call translate from different service based on the parameter from the same translation_service
            self.result_label.config(text=translation)
        else:
            self.result_label.config(text="No translation service selected!")

# Running the TranslatorApp
if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
