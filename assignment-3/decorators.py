import functools
import logging

# Configure logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Decorator for logging translation actions
def log_translation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log the source and target languages
        logging.info(f"Translating text from {kwargs.get('src_lang', 'auto')} to {kwargs.get('tgt_lang', 'en')}")
        result = func(*args, **kwargs)
        logging.info("Translation complete")  # Log when the translation is finished
        return result
    return wrapper

# Decorator for handling errors in the application
def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)  # Attempt to execute the function
        except Exception as e:
            logging.error(f"An error occurred: {e}")  # Log any errors that occur
            raise e  # Re-raise the error to ensure it gets handled
    return wrapper
