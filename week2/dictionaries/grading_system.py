# grading_system.py

def add_student(grades, name, scores):
    grades[name] = scores
    print(f"Added {name} with scores {scores}")

def calculate_average(scores):
    return sum(scores) / len(scores)

def print_report(grades):
    print("Student Report:")
    for name, scores in grades.items():
        avg = calculate_average(scores)
        print(f"{name}: Scores={scores}, Average={avg:.2f}")

# Example usage
if __name__ == "__main__":
    students_grades = {}

    add_student(students_grades, "Anna", [85, 90, 78])
    add_student(students_grades, "Liam", [92, 88, 95])
    add_student(students_grades, "Mika", [70, 75, 80])

    print_report(students_grades)
