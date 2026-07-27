class Student:
    def __init__(self, name, grades=[]):  # Bug: mutable default argument is shared across every Student created without grades
        self.name = name
        self.grades = grades

    def add_grade(self, grade):
        self.grades.append(grade)
