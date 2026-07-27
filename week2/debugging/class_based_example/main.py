from models.dataset import get_sample_students
from utils.calculator import AverageCalculator
from utils.report import ReportGenerator

if __name__ == "__main__":
    students = get_sample_students()
    calculator = AverageCalculator()
    report = ReportGenerator()

    for student in students:
        average = calculator.calculate(student.grades)
        print(report.format_line(student.name, average))

    print(report.format_summary(students, calculator))
