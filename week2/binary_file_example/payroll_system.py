"""Binary-file (pickle) backed storage for employee payroll records."""

import pickle
from pathlib import Path

from models.employee import Employee


class PayrollSystem:
    """Persists Employee records to a binary file using pickle."""

    def __init__(self, filename):
        self.filename = filename
        self._employees = {}
        self.load()

    @property
    def filename(self):
        """Path to the binary file backing this payroll system."""
        return self._filename

    @filename.setter
    def filename(self, value):
        if not value:
            raise ValueError("A filename is required.")
        self._filename = value

    @property
    def employees(self):
        """All employees currently loaded in memory."""
        return list(self._employees.values())

    def load(self):
        """Load employee records from the binary file, if it exists."""
        path = Path(self.filename)
        if not path.exists():
            self._employees = {}
            return
        with path.open("rb") as handle:
            self._employees = pickle.load(handle)

    def save(self):
        """Persist all employee records to the binary file."""
        with open(self.filename, "wb") as handle:
            pickle.dump(self._employees, handle)

    def add_employee(self, employee):
        """Register a new employee and persist immediately."""
        if not isinstance(employee, Employee):
            raise TypeError("employee must be an Employee instance.")
        self._employees[employee.employee_id] = employee
        self.save()

    def log_hours(self, employee_id, hours):
        """Add worked hours to an existing employee and persist."""
        employee = self._employees[employee_id]
        employee.hours_worked += hours
        self.save()

    def total_payroll(self):
        """Sum of gross pay across every employee."""
        return sum(employee.gross_pay for employee in self._employees.values())
