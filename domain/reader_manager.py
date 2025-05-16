from typing import Optional, Dict, List
from datetime import date
from model import *
from .storage_service import StorageService

class ReaderManager:
    def __init__(self, storage_service: Optional[StorageService] = None):
        self.storage_service = storage_service or StorageService()
        data = self.storage_service.load_library_data()
        self.readers: List[Reader] = data['readers']
        self.loans: List[Loan] = data['loans']
        self.penalties: List[Penalty] = data['penalties']

    def register_reader(self, reader: Reader) -> bool:
        if self.find_reader(reader.ticket_number):
            return False
        self.readers.append(reader)
        self._save_data()
        return True

    def update_reader(self, ticket_number: str, **kwargs) -> bool:
        reader = self.find_reader(ticket_number)
        if not reader:
            return False
        
        for key, value in kwargs.items():
            if hasattr(reader, key):
                if key == 'renewal_date' and isinstance(value, date):
                    setattr(reader, key, value)
                elif key in ['full_name', 'category']:
                    setattr(reader, key, value)
        self._save_data()
        return True

    def remove_reader(self, ticket_number: str) -> bool:
        reader = self.find_reader(ticket_number)
        if not reader:
            return False

        # Проверяем наличие невозвращенных книг
        active_loans = [loan for loan in self.loans 
                       if loan.reader.ticket_number == ticket_number and not loan.return_date]
        if active_loans:
            return False

        # Проверяем наличие неоплаченных штрафов
        unpaid_penalties = [penalty for penalty in self.penalties 
                          if penalty.reader.ticket_number == ticket_number]
        if unpaid_penalties:
            return False

        self.readers.remove(reader)
        self._save_data()
        return True

    def find_reader(self, ticket_number: str) -> Optional[Reader]:
        for reader in self.readers:
            if reader.ticket_number == ticket_number:
                return reader
        return None

    def check_reader_status(self, ticket_number: str) -> dict:
        reader = self.find_reader(ticket_number)
        if not reader:
            return {}
            
        active_loans = []
        overdue_loans = []
        returned_loans = []
        penalties = []

        for loan in self.loans:
            if loan.reader.ticket_number == ticket_number:
                loan_info = {
                    'book_title': loan.book.title,
                    'issue_date': loan.issue_date,
                    'due_date': loan.due_date
                }
                if loan.return_date:
                    loan_info['return_date'] = loan.return_date
                    returned_loans.append(loan_info)
                elif loan.is_overdue():
                    overdue_loans.append(loan_info)
                else:
                    active_loans.append(loan_info)

        for penalty in self.penalties:
            if penalty.reader.ticket_number == ticket_number:
                penalties.append({
                    'book_title': penalty.book.title,
                    'fine_amount': penalty.fine_amount,
                    'overdue_days': penalty.overdue_days
                })

        return {
            'reader_info': {
                'full_name': reader.full_name,
                'ticket_number': reader.ticket_number,
                'category': reader.category,
                'registration_date': reader.registration_date,
                'renewal_date': reader.renewal_date
            },
            'active_loans': active_loans,
            'overdue_loans': overdue_loans,
            'returned_loans': returned_loans,
            'penalties': penalties
        }
        
    def _save_data(self) -> None:
        """Сохраняет текущее состояние данных через storage_service."""
        self.storage_service.save_library_data(
            readers=self.readers,
            books=[],  # Книги управляются через LibraryCatalog
            loans=self.loans,
            penalties=self.penalties
        )

    def issue_book(self, ticket_number: str, book) -> bool:
        reader = self.find_reader(ticket_number)
        if not reader:
            return False
        if book.available_copies <= 0:
            return False  # No copies available
        loan = Loan(reader, book)
        self.loans.append(loan)
        self._save_data()
        return True

    def return_book(self, ticket_number: str, library_code: str) -> bool:
        for loan in self.loans:
            if (loan.reader.ticket_number == ticket_number and
                loan.book.library_code == library_code and
                loan.return_date is None):
                loan.return_book()
                self._save_data()
                return True
        return False