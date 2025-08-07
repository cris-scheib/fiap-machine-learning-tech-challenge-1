class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class BookNotFoundException(CustomException):
    def __init__(self, book_id: int = None):
        message = f"Book with ID  '{book_id}' not found."
        super().__init__(message)

class BookNotFoundInRangePriceException(CustomException):
    def __init__(self):
        message = "Minimum value must not be greater than maximum value."
        super().__init__(message)

class DatabaseException(CustomException):
    def __init__(self, original_error: Exception = None):
        self.original_error = original_error
        message = "An unexpected error occurred while accessing the database."
        super().__init__(message)