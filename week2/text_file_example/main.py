"""Demo entry point for the library ledger text-file example."""

import argparse

from library_ledger import LibraryLedger


def parse_args():
    """Parse the ledger filename from the command line."""
    parser = argparse.ArgumentParser(
        description="Library loan ledger backed by a plain text file."
    )
    parser.add_argument(
        "filename",
        help="Path to the ledger text file (created automatically if missing).",
    )
    return parser.parse_args()


def main():
    """Seed sample loans on first run, then print a loan report."""
    args = parse_args()
    ledger = LibraryLedger(args.filename)

    if not ledger.loans:
        ledger.checkout("Clean Code", "Ana Rodriguez", loan_days=7)
        ledger.checkout("The Pragmatic Programmer", "Luis Mora")
        ledger.return_book("Clean Code", "Ana Rodriguez")

    print(f"Ledger file: {ledger.filename}\n")

    print("All loans:")
    for loan in ledger.loans:
        print(f"  - {loan}")

    print("\nActive loans:")
    for loan in ledger.active_loans():
        print(f"  - {loan}")

    print("\nOverdue loans:")
    overdue = ledger.overdue_loans()
    if overdue:
        for loan in overdue:
            print(f"  - {loan}")
    else:
        print("  None")


if __name__ == "__main__":
    main()
