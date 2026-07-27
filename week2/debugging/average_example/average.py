def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num  # Bug: crashes with TypeError if a non-numeric value sneaks into the list
    average = total / len(numbers)
    return avrage  # Bug: misspelled variable -> NameError


def find_highest(numbers):
    highest = numbers[0]
    for num in numbers:
        if num < highest:  # Bug: comparison is backwards, this actually finds the lowest value
            highest = num
    return highest


def find_lowest(numbers):
    lowest = numbers[0]
    for num in numbers:
        if num < lowest:
            lowest = num
    return lowest


def calculate_median(numbers):
    # Bug: forgets to sort before picking the middle value(s)
    middle = len(numbers) // 2
    if len(numbers) % 2 == 0:
        return (numbers[middle - 1] + numbers[middle]) / 2
    return numbers[middle]


if __name__ == "__main__":
    grades = [82, 91, "78", 65, 90, 88]  # Bug: one grade was entered as a string by mistake

    print("The average is:", calculate_average(grades))
    print("The highest grade is:", find_highest(grades))
    print("The lowest grade is:", find_lowest(grades))
    print("The median grade is:", calculate_median(grades))
