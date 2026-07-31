"""Interactive entry point for the guess-the-number game."""

from game import ComputerGuessesMode, PlayerGuessesMode

MIN_NUMBER = 1
MAX_NUMBER = 100
DEFAULT_MAX_ATTEMPTS = 6

MENU = f"""
==============================
   GUESS THE NUMBER ({MIN_NUMBER}-{MAX_NUMBER})
==============================
1) You think of a number, the computer guesses it
2) The computer thinks of a number, you guess it
3) Quit
==============================
"""


def choose_option():
    """Prompt until the player picks a valid menu option."""
    while True:
        choice = input("Choose an option (1-3): ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print("Please enter 1, 2 or 3.")


def ask_max_attempts():
    """Ask how many attempts to allow, keeping the default on empty/invalid input."""
    raw_value = input(f"Max attempts (press Enter for {DEFAULT_MAX_ATTEMPTS}): ").strip()
    if not raw_value:
        return DEFAULT_MAX_ATTEMPTS
    if raw_value.isdigit() and int(raw_value) > 0:
        return int(raw_value)
    print(f"That's not a valid number of attempts, using the default ({DEFAULT_MAX_ATTEMPTS}).")
    return DEFAULT_MAX_ATTEMPTS


def play_again():
    """Ask the player whether to start another round."""
    return input("\nPlay again? (y/n): ").strip().lower().startswith("y")


def main():
    """Show the menu and run rounds until the player chooses to quit."""
    print(MENU)
    while True:
        choice = choose_option()

        if choice == "3":
            print("Thanks for playing. See you next time!")
            break

        max_attempts = ask_max_attempts()
        if choice == "1":
            game = ComputerGuessesMode(min_number=MIN_NUMBER, max_number=MAX_NUMBER, max_attempts=max_attempts)
        else:
            game = PlayerGuessesMode(min_number=MIN_NUMBER, max_number=MAX_NUMBER, max_attempts=max_attempts)

        game.play()

        if not play_again():
            print("Thanks for playing. See you next time!")
            break


if __name__ == "__main__":
    main()
