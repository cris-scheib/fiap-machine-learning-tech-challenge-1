class BookNotFoundException(Exception):
    def __init__(self, book_id: int):
        self.book_id = book_id
        message = f"Book with ID {book_id} not found"
        super().__init__(message)
        self.message = message