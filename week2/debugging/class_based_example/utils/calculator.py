class AverageCalculator:
    def calculate(self, numbers):
        # Bug: forgets to check for empty list -> ZeroDivisionError
        total = 0
        for n in numbers:
            total += n
        return total / len(numbrs)  # Bug: misspelled variable -> NameError

    def calculate_weighted(self, numbers, weights):
        # Bug: assumes numbers and weights always have the same length -> IndexError
        total = 0
        for i in range(len(numbers)):
            total += numbers[i] * weights[i]
        return total / sum(weights)
