from datetime import date, timedelta
from typing import Optional
from .reader import Reader
from .book import Book

class Loan:
    def __init__(
        self,
        reader: Reader,
        book: Book,
        issue_date: Optional[date] = None,
        due_date: Optional[date] = None,
        return_date: Optional[date] = None
    ):
        self.reader = reader
        self.book = book
        self.issue_date = issue_date if issue_date else date.today()
        self.due_date = due_date if due_date else self.issue_date + timedelta(days=14)
        self.return_date: Optional[date] = return_date

        # Only decrement available_copies if this is a new loan (not when loading from storage)
        if return_date is None and (issue_date is None and due_date is None):
            book.available_copies -= 1

    def return_book(self) -> None:
        self.return_date = date.today()
        self.book.available_copies += 1

    def is_overdue(self) -> bool:
        if self.return_date:
            return False
        return date.today() > self.due_date