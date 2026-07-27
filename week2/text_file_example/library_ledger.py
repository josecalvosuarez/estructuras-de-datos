"""Text-file backed storage for library book loans."""

from datetime import date, timedelta
from pathlib import Path

from models.book_loan import BookLoan


class LibraryLedger:
    """Reads and writes book loan records to a pipe-delimited text file."""

    def __init__(self, filename):
        self.filename = filename
        self._loans = []
        self.load()

    @property
    def filename(self):
        """Path to the text file backing this ledger."""
        return self._filename

    @filename.setter
    def filename(self, value):
        if not value:
            raise ValueError("A filename is required.")
        self._filename = value

    @property
    def loans(self):
        """A copy of every loan recorded in the ledger."""
        return list(self._loans)

    def load(self):
        """Populate the ledger from the text file, if it exists."""
        path = Path(self.filename)
        self._loans = []
        if not path.exists():
            return
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    self._loans.append(BookLoan.from_row(line))

    def save(self):
        """Persist every loan back to the text file."""
        with open(self.filename, "w", encoding="utf-8") as handle:
            for loan in self._loans:
                handle.write(loan.to_row() + "\n")

    def checkout(self, title, borrower, loan_days=14):
        """Record a new loan and persist it immediately."""
        checkout_date = date.today()
        due_date = checkout_date + timedelta(days=loan_days)
        loan = BookLoan(title, borrower, checkout_date, due_date)
        self._loans.append(loan)
        self.save()
        return loan

    def return_book(self, title, borrower):
        """Mark the active loan for title/borrower as returned."""
        for loan in self._loans:
            if loan.title == title and loan.borrower == borrower and not loan.returned:
                loan.returned = True
                self.save()
                return loan
        raise LookupError(f"No active loan found for '{title}' borrowed by {borrower}.")

    def active_loans(self):
        """Loans that have not yet been returned."""
        return [loan for loan in self._loans if not loan.returned]

    def overdue_loans(self):
        """Active loans whose due date has passed."""
        return [loan for loan in self._loans if loan.is_overdue]
