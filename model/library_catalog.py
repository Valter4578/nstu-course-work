from typing import Optional, List
from .book import Book

class LibraryCatalog:
    def __init__(self):
        self.books: List[Book] = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def find_by_title(self, title: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def get_all_books(self) -> List[Book]:
        return self.books.copy()