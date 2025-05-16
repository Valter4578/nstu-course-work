from datetime import date

class Reader:
    def __init__(
        self,
        full_name: str,
        ticket_number: str,
        category: str,
        registration_date: date = None,
        renewal_date: date = None
    ):
        self.full_name = full_name
        self.ticket_number = ticket_number
        self.category = category
        self.registration_date = registration_date if registration_date else date.today()
        self.renewal_date = renewal_date if renewal_date else date.today()

    def __str__(self) -> str:
        return f"Reader: {self.full_name} (Ticket: {self.ticket_number})"