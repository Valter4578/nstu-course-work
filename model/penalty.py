from .reader import Reader
from .book import Book

class Penalty:
    def __init__(self, reader: Reader, book: Book, overdue_days: int):
        self.reader = reader
        self.book = book
        self.overdue_days = overdue_days
        self.fine_amount = self.calculate_fine()

    def calculate_fine(self) -> float:
        # Простой расчет штрафа: 10 рублей за каждый день просрочки
        return self.overdue_days * 10.0

    def __str__(self) -> str:
        return f"Штраф для {self.reader.full_name}: {self.fine_amount} руб. за книгу {self.book.title}"