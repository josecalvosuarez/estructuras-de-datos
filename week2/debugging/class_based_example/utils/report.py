class ReportGenerator:
    def format_line(self, name, average):
        return f"{name}: {average}"

    def format_summary(self, students, calculator):
        # Bug: collects each student's grade list instead of flattening them into
        # one list of numbers, so calculator.calculate ends up adding ints to lists
        all_grades = [student.grades for student in students]
        class_average = calculator.calculate(all_grades)
        return f"Class average: {class_average}"
