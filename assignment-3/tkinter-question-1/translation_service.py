from abc import ABC, abstractmethod
from transformers import pipeline
from decorators import log_execution, log_result, error_handler

# Abstract base class (ABC) for translation services
class TranslationService(ABC):

    @abstractmethod
    def load_model(self):
        """Load the translation model. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def translate(self, text: str) -> str:
        """Abstract method for translating text. Must be implemented by subclasses."""
        pass


# Concrete class for French translation
class FrenchTranslationService(TranslationService):  # Single Inheritance - inherits from TranslationService class

    def __init__(self):
        self._model = None

    @log_execution
    @error_handler
    def load_model(self):
        """Load the model for English to French translation."""
        self._model = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
        print("Loading model complete")

    @log_execution
    @error_handler
    def translate(self, text: str) -> str:
        """Translate text from English to French."""
        if not self._model:
            self.load_model()
        return self._model(text)[0]['translation_text']


# Concrete class for German translation
class GermanTranslationService(TranslationService):  # Single Inheritance - inherits from TranslationService class

    def __init__(self):
        self._model = None

    @log_execution
    @error_handler
    def load_model(self):
        """Load the model for English to German translation."""
        self._model = pipeline("translation", model="Helsinki-NLP/opus-mt-en-de")
        print("Loading model complete")

    @log_execution
    @error_handler
    def translate(self, text: str) -> str:
        """Translate text from English to German."""
        if not self._model:
            self.load_model()
        return self._model(text)[0]['translation_text']
