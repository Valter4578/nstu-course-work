import json
from typing import Dict, List, Optional
from pathlib import Path
from model import *
from datetime import datetime, date

class StorageService:
    def __init__(self, storage_file: str = 'library_data.json'):
        self.storage_file = storage_file
        self.storage_path = Path(storage_file)

    def _serialize_date(self, obj: date) -> str:
        return obj.isoformat()

    def _deserialize_date(self, date_str: str) -> date:
        return datetime.fromisoformat(date_str).date()

    def _serialize_reader(self, reader: Reader) -> Dict:
        return {
            'ticket_number': reader.ticket_number,
            'full_name': reader.full_name,
            'category': reader.category,
            'registration_date': self._serialize_date(reader.registration_date),
            'renewal_date': self._serialize_date(reader.renewal_date) if reader.renewal_date else None
        }

    def _deserialize_reader(self, data: Dict) -> Reader:
        return Reader(
            ticket_number=data['ticket_number'],
            full_name=data['full_name'],
            category=data['category'],
            registration_date=self._deserialize_date(data['registration_date']),
            renewal_date=self._deserialize_date(data['renewal_date']) if data['renewal_date'] else None
        )

    def _serialize_book(self, book: Book) -> Dict:
        return {
            'library_code': book.library_code,
            'title': book.title,
            'authors': book.authors,
            'year': book.year,
            'total_copies': book.total_copies,
            'available_copies': book.available_copies,
            'publisher': book.publisher,
        }

    def _deserialize_book(self, data: Dict) -> Book:
        return Book(
            library_code=data['library_code'],
            title=data['title'],
            authors=data['authors'],
            year=data['year'],
            total_copies=data['total_copies'],

            publisher=data['publisher']
        )

    def _serialize_loan(self, loan: Loan) -> Dict:
        return {
            'reader': self._serialize_reader(loan.reader),
            'book': self._serialize_book(loan.book),
            'issue_date': self._serialize_date(loan.issue_date),
            'due_date': self._serialize_date(loan.due_date),
            'return_date': self._serialize_date(loan.return_date) if loan.return_date else None
        }

    def _deserialize_loan(self, data: Dict) -> Loan:
        return Loan(
            reader=self._deserialize_reader(data['reader']),
            book=self._deserialize_book(data['book']),
            issue_date=self._deserialize_date(data['issue_date']),
            due_date=self._deserialize_date(data['due_date']),
            return_date=self._deserialize_date(data['return_date']) if data['return_date'] else None
        )

    def _serialize_penalty(self, penalty: Penalty) -> Dict:
        return {
            'reader': self._serialize_reader(penalty.reader),
            'book': self._serialize_book(penalty.book),
            'fine_amount': penalty.fine_amount,
            'overdue_days': penalty.overdue_days
        }

    def _deserialize_penalty(self, data: Dict) -> Penalty:
        return Penalty(
            reader=self._deserialize_reader(data['reader']),
            book=self._deserialize_book(data['book']),
            fine_amount=data['fine_amount'],
            overdue_days=data['overdue_days']
        )

    def save_library_data(self, readers: List[Reader], books: List[Book],
                         loans: List[Loan], penalties: List[Penalty]) -> None:
        data = {
            'readers': [self._serialize_reader(reader) for reader in readers],
            'books': [self._serialize_book(book) for book in books],
            'loans': [self._serialize_loan(loan) for loan in loans],
            'penalties': [self._serialize_penalty(penalty) for penalty in penalties]
        }

        print(data)
        
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_library_data(self) -> Dict:
        if not self.storage_path.exists():
            return {'readers': [], 'books': [], 'loans': [], 'penalties': []}
        
        with open(self.storage_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {
            'readers': [self._deserialize_reader(r) for r in data.get('readers', [])],
            'books': [self._deserialize_book(b) for b in data.get('books', [])],
            'loans': [self._deserialize_loan(l) for l in data.get('loans', [])],
            'penalties': [self._deserialize_penalty(p) for p in data.get('penalties', [])]
        }