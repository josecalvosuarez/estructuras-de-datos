from models.student import Student


def get_sample_students():
    alice = Student("Alice")
    alice.add_grade(90)
    alice.add_grade(85)

    bob = Student("Bob")
    bob.add_grade(70)

    carol = Student("Carol")
    carol.add_grade(100)

    return [alice, bob, carol]
