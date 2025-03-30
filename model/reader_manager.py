from typing import Optional, Dict, List
from datetime import date
from .reader import Reader
from .loan import Loan
from .penalty import Penalty
from .book import Book

class ReaderManager:
    def __init__(self):
        self.readers: List[Reader] = []
        self.loans: List[Loan] = []
        self.penalties: List[Penalty] = []

    def register_reader(self, reader: Reader) -> bool:
        if self.find_reader(reader.ticket_number):
            return False
        self.readers.append(reader)
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