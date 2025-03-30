from typing import Optional, List
from .book import Book

class LibraryCatalog:
    def __init__(self):
        self.books: List[Book] = []

    def add_book(self, book: Book) -> None:
        existing_book = self.find_by_library_code(book.library_code)
        if existing_book:
            existing_book.total_copies += book.total_copies
            existing_book.available_copies += book.total_copies
        else:
            self.books.append(book)

    def remove_book(self, library_code: str) -> bool:
        book = self.find_by_library_code(library_code)
        if book and book.available_copies == book.total_copies:
            self.books.remove(book)
            return True
        return False

    def update_book(self, library_code: str, **kwargs) -> bool:
        book = self.find_by_library_code(library_code)
        if not book:
            return False
        
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        return True

	# ищет книгу по названию и возвращает объект `Book` или `None`, если книга не найдена.
    def find_by_title(self, title: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def find_by_library_code(self, library_code: str) -> Optional[Book]:
        for book in self.books:
            if book.library_code == library_code:
                return book
        return None

    def register_new_copies(self, library_code: str, count: int) -> bool:
        book = self.find_by_library_code(library_code)
        if book and count > 0:
            book.total_copies += count
            book.available_copies += count
            return True
        return False

    def get_all_books(self) -> List[Book]:
        return self.books.copy()