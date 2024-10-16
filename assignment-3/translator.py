from transformers import MarianMTModel, MarianTokenizer
from decorators import log_translation, handle_errors  # Import decorators for logging and error handling
from abc import ABC, abstractmethod

# Abstract base class that defines a contract for translation services
class TranslationService(ABC):
    #abstractmethod
    @abstractmethod
    def translate(self, text, src_lang, tgt_lang):
        """
        Abstract method to translate the given text from source language (src_lang) to target language (tgt_lang).
        All subclasses must implement this method.

        :param text: The text to translate
        :param src_lang: The source language code (e.g., 'en')
        :param tgt_lang: The target language code (e.g., 'fr')
        :return: The translated text
        """
        pass

# Hugging Face MarianMT-based translation service
class HuggingFaceTranslateService(TranslationService):
    """
    Translation service using Hugging Face MarianMT models.
    """
    def __init__(self, src_lang: str = "en", tgt_lang: str = "fr"):
        # Set up the model and tokenizer with source and target language
        model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

    @log_translation  # Log the translation process
    @handle_errors  # Handle any errors during translation
    def translate(self, text: str, src_lang: str = "en", tgt_lang: str = "fr") -> str:
        # Prepare the model based on selected languages
        model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

        # Tokenize the input text for the MarianMT model
        inputs = self.tokenizer(text, return_tensors="pt", padding=True)

        # Generate translation using the model
        translated_tokens = self.model.generate(**inputs)

        # Decode the translated tokens into human-readable text
        translated_text = self.tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

        return translated_text  # Return the translated text
