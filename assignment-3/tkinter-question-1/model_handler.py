from transformers import pipeline
from decorators import log_execution, log_result, error_handler

# Encapsulation: ModelHandler handles model loading and translation logic internally
class ModelHandler:
    def __init__(self):
        self._model = None  # Private attribute

    @log_execution  # Logging when the model is loaded
    @error_handler  # Handling any errors during model loading
    def load_model(self, model_name: str):
        if model_name == "translation_en_to_fr":
            self._model = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
        elif model_name == "translation_en_to_de":
            self._model = pipeline("translation", model="Helsinki-NLP/opus-mt-en-de")
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    @log_execution  # Logging when translation is executed
    @log_result  # Logging the result of translation
    @error_handler  # Handling any errors during translation
    def translate(self, text: str) -> str:
        """Translate the given text using the loaded model."""
        if self._model:
            return self._model(text)[0]['translation_text']
        else:
            raise RuntimeError("No model loaded!")
