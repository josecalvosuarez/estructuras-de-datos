"""Domain model for a single library book loan."""

from datetime import date, datetime


class BookLoan:
    """Represents a single book checked out from the library."""

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, title, borrower, checkout_date, due_date, returned=False):
        self.title = title
        self.borrower = borrower
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.returned = returned

    @property
    def title(self):
        """Title of the borrowed book."""
        return self._title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty.")
        self._title = value.strip()

    @property
    def borrower(self):
        """Name of the person who borrowed the book."""
        return self._borrower

    @borrower.setter
    def borrower(self, value):
        if not value or not value.strip():
            raise ValueError("Borrower cannot be empty.")
        self._borrower = value.strip()

    @property
    def checkout_date(self):
        """Date the book was checked out."""
        return self._checkout_date

    @checkout_date.setter
    def checkout_date(self, value):
        self._checkout_date = self._parse_date(value)

    @property
    def due_date(self):
        """Date the book is due back."""
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        self._due_date = self._parse_date(value)

    @property
    def returned(self):
        """Whether the book has already been returned."""
        return self._returned

    @returned.setter
    def returned(self, value):
        self._returned = bool(value)

    @property
    def is_overdue(self):
        """True when the loan is still active past its due date."""
        return not self._returned and date.today() > self._due_date

    @classmethod
    def _parse_date(cls, value):
        """Accept either a date object or a string in DATE_FORMAT."""
        if isinstance(value, date):
            return value
        return datetime.strptime(value, cls.DATE_FORMAT).date()

    def to_row(self):
        """Serialize this loan into a single pipe-delimited text line."""
        return "|".join([
            self.title,
            self.borrower,
            self.checkout_date.strftime(self.DATE_FORMAT),
            self.due_date.strftime(self.DATE_FORMAT),
            "1" if self.returned else "0",
        ])

    @classmethod
    def from_row(cls, row):
        """Rebuild a BookLoan from a line produced by to_row()."""
        title, borrower, checkout_date, due_date, returned = row.strip().split("|")
        return cls(title, borrower, checkout_date, due_date, returned == "1")

    def __str__(self):
        if self.returned:
            status = "Returned"
        elif self.is_overdue:
            status = "OVERDUE"
        else:
            status = "On loan"
        return f"{self.title} -> {self.borrower} (due {self.due_date}, {status})"
