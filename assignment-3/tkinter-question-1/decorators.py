import functools
import logging

# Multiple Decorators for logging and error handling

# Decorator for logging translation actions
def log_execution(func):
    """Decorator for logging execution of methods."""
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}...")
        return func(*args, **kwargs)
    return wrapper

def log_result(func):
    """Decorator for logging the result of a method."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Result of {func.__name__}: {result}")
        return result
    return wrapper

# Decorator for handling errors in the application
def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)  # Attempt to execute the function
        except Exception as e:
            logging.error(f"An error occurred: {e}")  # Log any errors that occur
            raise e  # Re-raise the error to ensure it gets handled
    return wrapper
