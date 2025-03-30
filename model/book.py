from typing import List

class Book:
    def __init__(self, title: str, authors: List[str], library_code: str,
                 year: int, publisher: str, total_copies: int):
        self.title = title
        self.authors = authors
        self.library_code = library_code
        self.year = year
        self.publisher = publisher
        self.total_copies = total_copies
        self.available_copies = total_copies

    def __str__(self) -> str:
        return f"{self.title} ({', '.join(self.authors)})"