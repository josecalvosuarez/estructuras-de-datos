"""Demo entry point for the guess-the-number game."""

import argparse

from game import ComputerGuessesMode, PlayerGuessesMode


def parse_args():
    """Parse the game mode and attempt limit from the command line."""
    parser = argparse.ArgumentParser(description="Guess the number game (1-100).")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["player", "cpu"],
        help="'player' to guess the computer's number, "
             "'cpu' to have the computer guess yours.",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=6,
        help="Number of tries allowed (default: 6).",
    )
    return parser.parse_args()


def choose_mode():
    """Interactively ask the player which mode to play when none was given."""
    while True:
        choice = input("Choose a mode - (1) You guess  (2) Computer guesses: ").strip()
        if choice == "1":
            return "player"
        if choice == "2":
            return "cpu"
        print("Please enter 1 or 2.")


def main():
    """Build the selected game mode and play a single round."""
    args = parse_args()
    mode = args.mode or choose_mode()

    if mode == "player":
        game = PlayerGuessesMode(min_number=1, max_number=100, max_attempts=args.max_attempts)
    else:
        game = ComputerGuessesMode(min_number=1, max_number=100, max_attempts=args.max_attempts)

    game.play()


if __name__ == "__main__":
    main()
