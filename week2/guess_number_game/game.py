"""Game logic for the two guess-the-number modes."""

import random

HIGHER_HINTS = ["Higher! Aim bigger.", "Nope, go higher.", "Higher, don't be shy."]
LOWER_HINTS = ["Lower! That's too big.", "Come down a bit.", "Lower, champ."]
PLAYER_WIN_REMARKS = ["Nailed it!", "Sharp shooter!", "You got it!"]
PLAYER_LOSE_REMARKS = [
    "Better luck next time!",
    "That number was too sneaky for you, huh?",
    "So close, yet so far.",
]
CPU_WIN_REMARKS = ["I knew it!", "Mind-reading level: expert.", "Too easy for me!"]
CPU_LOSE_REMARKS = [
    "You win! I clearly need to recalibrate my circuits.",
    "Impressive. My CPU is blushing.",
    "Well played, human.",
]


class GuessNumberGame:
    """Base configuration shared by both game modes."""

    def __init__(self, min_number=1, max_number=100, max_attempts=6):
        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts
        self._attempts_used = 0

    @property
    def min_number(self):
        """Smallest number that may be picked or guessed."""
        return self._min_number

    @min_number.setter
    def min_number(self, value):
        if not isinstance(value, int):
            raise TypeError("min_number must be an integer.")
        self._min_number = value

    @property
    def max_number(self):
        """Largest number that may be picked or guessed."""
        return self._max_number

    @max_number.setter
    def max_number(self, value):
        if not isinstance(value, int):
            raise TypeError("max_number must be an integer.")
        if hasattr(self, "_min_number") and value <= self._min_number:
            raise ValueError("max_number must be greater than min_number.")
        self._max_number = value

    @property
    def max_attempts(self):
        """Maximum number of guesses allowed per game."""
        return self._max_attempts

    @max_attempts.setter
    def max_attempts(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("max_attempts must be a positive integer.")
        self._max_attempts = value

    @property
    def attempts_used(self):
        """How many guesses have been made so far."""
        return self._attempts_used

    @property
    def attempts_left(self):
        """How many guesses remain before the game ends."""
        return self._max_attempts - self._attempts_used

    def _register_attempt(self):
        """Record that one more guess was made."""
        self._attempts_used += 1

    def reset(self):
        """Clear the attempt counter to start a fresh game."""
        self._attempts_used = 0

    def play(self):
        """Run one full game. Implemented by each mode subclass."""
        raise NotImplementedError


class PlayerGuessesMode(GuessNumberGame):
    """The computer secretly picks a number and the player tries to guess it."""

    def play(self):
        """Pick a secret number and let the player guess it interactively."""
        self.reset()
        secret_number = random.randint(self.min_number, self.max_number)
        print(f"\nI'm thinking of a number between {self.min_number} and "
              f"{self.max_number}. You have {self.max_attempts} tries.")

        while self.attempts_left > 0:
            guess = self._read_guess()
            self._register_attempt()

            if guess == secret_number:
                print(f"Correct! The number was {secret_number}. "
                      f"You used {self.attempts_used} attempt(s). {random.choice(PLAYER_WIN_REMARKS)}")
                return True

            hint = random.choice(HIGHER_HINTS) if guess < secret_number else random.choice(LOWER_HINTS)
            print(f"{hint} Attempts left: {self.attempts_left}")

        print(f"Out of tries! The number was {secret_number}. {random.choice(PLAYER_LOSE_REMARKS)}")
        return False

    def _read_guess(self):
        """Prompt the player until a valid in-range integer is entered."""
        while True:
            raw_value = input(f"Enter a number ({self.min_number}-{self.max_number}): ")
            try:
                value = int(raw_value)
            except ValueError:
                print("Please enter a whole number.")
                continue
            if not self.min_number <= value <= self.max_number:
                print(f"Number must be between {self.min_number} and {self.max_number}.")
                continue
            return value


class ComputerGuessesMode(GuessNumberGame):
    """The player secretly thinks of a number and the computer guesses it
    using a binary search strategy."""

    def play(self):
        """Guess the player's secret number using binary search."""
        self.reset()
        low, high = self.min_number, self.max_number
        print(f"\nThink of a number between {self.min_number} and {self.max_number} "
              f"and don't tell me. I have {self.max_attempts} tries to guess it.")
        print("Reply with 'h' (too high), 'l' (too low) or 'c' (correct).")

        while self.attempts_left > 0 and low <= high:
            guess = (low + high) // 2
            self._register_attempt()
            response = self._read_response(guess)

            if response == "c":
                print(f"I guessed it! Your number was {guess}. "
                      f"It took me {self.attempts_used} attempt(s). {random.choice(CPU_WIN_REMARKS)}")
                return True
            elif response == "h":
                high = guess - 1
            else:
                low = guess + 1

        print(f"I couldn't guess your number in time. {random.choice(CPU_LOSE_REMARKS)}")
        return False

    def _read_response(self, guess):
        """Prompt until the player answers with h, l or c."""
        while True:
            raw_value = input(f"My guess is {guess}. (h/l/c)? ").strip().lower()
            if raw_value in ("h", "l", "c"):
                return raw_value
            print("Please answer with 'h', 'l' or 'c'.")
