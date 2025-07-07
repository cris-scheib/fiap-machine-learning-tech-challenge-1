class BookNotFoundException(Exception):
    def __init__(self, book_id: int):
        self.book_id = book_id