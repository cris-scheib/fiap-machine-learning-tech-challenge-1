class CustomException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class BookNotFoundException(CustomException):
    def __init__(self, book_id: int = None):
        message = f"Livro com ID '{book_id}' não encontrado."
        super().__init__(message)

class BookNotFoundInRangePriceException(CustomException):
    def __init__(self):
        message = "Valor mínimo não deve ser maior que o valor máximo."
        super().__init__(message)

class DatabaseException(CustomException):
    def __init__(self, original_error: Exception = None):
        self.original_error = original_error
        message = "Ocorreu um erro inesperado ao acessar o banco de dados."
        super().__init__(message)