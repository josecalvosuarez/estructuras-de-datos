"""Demo entry point for the payroll binary-file example."""

import argparse

from models.employee import Employee
from payroll_system import PayrollSystem


def parse_args():
    """Parse the payroll filename from the command line."""
    parser = argparse.ArgumentParser(
        description="Payroll system backed by a binary (pickle) file."
    )
    parser.add_argument(
        "filename",
        help="Path to the binary payroll file (created automatically if missing).",
    )
    return parser.parse_args()


def main():
    """Seed sample employees on first run, then print a payroll report."""
    args = parse_args()
    payroll = PayrollSystem(args.filename)

    if not payroll.employees:
        payroll.add_employee(Employee("E001", "Maria Gomez", hourly_rate=18.5))
        payroll.add_employee(Employee("E002", "Carlos Vindas", hourly_rate=22.0))
        payroll.log_hours("E001", 45)
        payroll.log_hours("E002", 38)

    print(f"Payroll file: {payroll.filename}\n")

    print("Employees:")
    for employee in payroll.employees:
        print(f"  - {employee}")

    print(f"\nTotal payroll: ${payroll.total_payroll():.2f}")


if __name__ == "__main__":
    main()
