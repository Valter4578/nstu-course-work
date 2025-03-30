from datetime import date

class Reader:
    def __init__(self, full_name: str, ticket_number: str, category: str):
        self.full_name = full_name
        self.ticket_number = ticket_number
        self.registration_date = date.today()
        self.renewal_date = date.today()
        self.category = category

    def __str__(self) -> str:
        return f"Reader: {self.full_name} (Ticket: {self.ticket_number})"