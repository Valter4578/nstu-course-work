from datetime import date, timedelta
from typing import Optional
from .reader import Reader
from .book import Book

class Loan:
    def __init__(self, reader: Reader, book: Book):
        self.reader = reader
        self.book = book
        self.issue_date = date.today()
        self.due_date = self.issue_date + timedelta(days=14)
        self.return_date: Optional[date] = None
        book.available_copies -= 1

    def return_book(self) -> None:
        self.return_date = date.today()
        self.book.available_copies += 1

    def is_overdue(self) -> bool:
        if self.return_date:
            return False
        return date.today() > self.due_date