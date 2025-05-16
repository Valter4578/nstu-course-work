from typing import Optional, List
from model import Book
from .storage_service import StorageService

class LibraryCatalog:
    def __init__(self, storage_service: Optional[StorageService] = None):
        self.storage_service = storage_service or StorageService()
        data = self.storage_service.load_library_data()
        self.books: List[Book] = data['books']

    def add_book(self, book: Book) -> None:
        existing_book = self.find_by_library_code(book.library_code)
        if existing_book:
            existing_book.total_copies += book.total_copies
            existing_book.available_copies += book.total_copies
        else:
            self.books.append(book)
        self._save_data()

    def remove_book(self, library_code: str) -> bool:
        book = self.find_by_library_code(library_code)
        if book and book.available_copies == book.total_copies:
            self.books.remove(book)
            self._save_data()
            return True
        return False

    def _save_data(self) -> None:
        """Сохраняет текущее состояние данных через storage_service."""
        self.storage_service.save_library_data(
            readers=[],  # Читатели управляются через ReaderManager
            books=self.books,
            loans=[],     # Займы управляются через ReaderManager
            penalties=[]  # Штрафы управляются через ReaderManager
        )

    def update_book(self, library_code: str, **kwargs) -> bool:
        book = self.find_by_library_code(library_code)
        if not book:
            return False
        
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        self._save_data()
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
            self._save_data()
            return True
        return False

    def _save_data(self) -> None:
        """Сохраняет текущее состояние данных через storage_service."""
        self.storage_service.save_library_data(
            readers=[],  # Читатели управляются через ReaderManager
            books=self.books,
            loans=[],     # Займы управляются через ReaderManager
            penalties=[]  # Штрафы управляются через ReaderManager
        )

    def get_all_books(self) -> List[Book]:
        return self.books.copy()