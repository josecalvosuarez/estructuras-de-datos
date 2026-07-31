"""Domain model for an hourly employee."""


class Employee:
    """Represents an hourly employee tracked by the payroll system."""

    OVERTIME_THRESHOLD_HOURS = 40
    OVERTIME_MULTIPLIER = 1.5

    def __init__(self, employee_id, name, hourly_rate, hours_worked=0.0):
        self.employee_id = employee_id
        self.name = name
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    @property
    def employee_id(self):
        """Unique identifier for the employee."""
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        if not value:
            raise ValueError("Employee id cannot be empty.")
        self._employee_id = value

    @property
    def name(self):
        """The employee's full name."""
        return self._name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def hourly_rate(self):
        """Pay rate per hour, in currency units."""
        return self._hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value):
        if value < 0:
            raise ValueError("Hourly rate cannot be negative.")
        self._hourly_rate = float(value)

    @property
    def hours_worked(self):
        """Total hours logged for the current pay period."""
        return self._hours_worked

    @hours_worked.setter
    def hours_worked(self, value):
        if value < 0:
            raise ValueError("Hours worked cannot be negative.")
        self._hours_worked = float(value)

    @property
    def gross_pay(self):
        """Gross pay for the period, including 1.5x overtime past 40 hours."""
        regular_hours = min(self._hours_worked, self.OVERTIME_THRESHOLD_HOURS)
        overtime_hours = max(self._hours_worked - self.OVERTIME_THRESHOLD_HOURS, 0)
        overtime_rate = self._hourly_rate * self.OVERTIME_MULTIPLIER
        return regular_hours * self._hourly_rate + overtime_hours * overtime_rate

    def __str__(self):
        return (f"{self.employee_id} - {self.name}: {self.hours_worked}h "
                f"@ ${self.hourly_rate:.2f}/h -> ${self.gross_pay:.2f}")
