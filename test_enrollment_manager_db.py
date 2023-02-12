from enrollment_manager import NotFoundError, AlreadyExistsError
from gradescope_utils.autograder_utils.decorators import weight
from enrollment_manager_db import EnrollmentManagerDB
import unittest

FAKE_DATA = {
    "students": [
        {"id": "1", "name": "Ope"},
        {"id": "2", "name": "Keno"},
        {"id": "3", "name": "Mohammed"},
        {"id": "4", "name": "Olaperi"},
        {"id": "5", "name": "Chukwuemeka"},
        {"id": "6", "name": "Oyinloluwa"},
        {"id": "7", "name": "Funminiyi"},
        {"id": "8", "name": "Michael"},
        {"id": "9", "name": "Jacob"},
        {"id": "10", "name": "Nekesa"},
    ],
    "courses": [
        {"id": "1", "hours": 150, "name": "English", "students": ["1", "2", "3"]},
        {"id": "2", "hours": 150, "name": "Math", "students": ["1"]},
        {"id": "3", "hours": 150, "name": "French", "students": ["1"]},
        {"id": "4", "hours": 150, "name": "Science", "students": ["1"]},
    ],
}


class TestEnrollmentManagerDB(unittest.TestCase):
    def setUp(self):
        self.manager = EnrollmentManagerDB("sqlite://")
        self.manager.initialize_db_schema()
        self.manager.initialize_data(FAKE_DATA)

    def test_get_students(self):
        students = self.manager.get_students()
        assert students[0]["name"] == "Ope"
        assert students[0]["id"] == 1
        assert len(students) == len(FAKE_DATA["students"])

    def test_add_student(self):
        before = self.manager.get_students()
        assert len(before) == len(FAKE_DATA["students"])
        self.manager.add_student("Stanley")
        after = self.manager.get_students()
        assert len(after) == len(FAKE_DATA["students"]) + 1
        assert after[-1]["name"] == "Stanley"

    def test_remove_student(self):
        before = self.manager.get_students()
        assert len(before) == len(FAKE_DATA["students"])
        assert before[2]["name"] == "Mohammed"
        assert before[2]["id"] == 3
        self.manager.remove_student(3)
        after = self.manager.get_students()
        assert len(after) == len(FAKE_DATA["students"]) - 1
        assert "Mohammed" not in [student["name"] for student in after]

    def test_remove_missing(self):
        with self.assertRaises(NotFoundError) as e:
            self.manager.remove_student(100)
        assert "No student with ID 100." in e.exception.args

    def test_lookup_student(self):
        ope = self.manager.lookup_student(1)
        assert ope["name"] == "Ope"
        assert ope["id"] == 1
        assert len(ope["courses"]) == 4

    def test_lookup_missing_student(self):
        with self.assertRaises(NotFoundError) as e:
            self.manager.lookup_student(100)
        assert "No student with ID 100." in e.exception.args

    @weight(10)
    def test_search_students_by_name(self):
        results = self.manager.search_students_by_name("m")
        assert len(results) == 4
        assert "Mohammed" in [student["name"] for student in results]
        assert "Michael" in [student["name"] for student in results]
        assert "Funminiyi" in [student["name"] for student in results]
        assert "Chukwuemeka" in [student["name"] for student in results]
        empty = self.manager.search_students_by_name("zzzz")
        assert len(empty) == 0

    @weight(10)
    def test_get_courses(self):
        courses = self.manager.get_courses()
        assert courses[0]["name"] == "English"
        assert courses[0]["id"] == 1
        assert len(courses) == len(FAKE_DATA["courses"])

    @weight(10)
    def test_add_course(self):
        before = self.manager.get_courses()
        assert len(before) == len(FAKE_DATA["courses"])
        self.manager.add_course("Geography", 75)
        after = self.manager.get_courses()
        assert len(after) == len(FAKE_DATA["courses"]) + 1
        assert after[-1]["name"] == "Geography"
        assert after[-1]["hours"] == 75

    @weight(10)
    def test_lookup_course(self):
        english = self.manager.lookup_course(1)
        assert english["name"] == "English"
        assert english["id"] == 1
        assert len(english["students"]) == 3

    @weight(10)
    def test_lookup_missing_course(self):
        with self.assertRaises(NotFoundError) as e:
            self.manager.lookup_course(100)
        assert "No course with ID 100." in e.exception.args

    @weight(10)
    def test_enroll_student(self):
        # The student is not enrolled in the course before
        course_before = self.manager.lookup_course(4)
        student_before = self.manager.lookup_student(4)
        assert len(course_before["students"]) == 1
        assert len(student_before["courses"]) == 0

        self.manager.enroll_student(4, 4)

        # The student is enrolled in the course after
        course_after = self.manager.lookup_course(4)
        student_after = self.manager.lookup_student(4)
        assert len(course_after["students"]) == 2
        assert student_after["id"] in [
            enrollment.student_id for enrollment in course_after.students
        ]
        assert len(student_after["courses"]) == 1
        assert course_after["id"] in [
            enrollment.course_id for enrollment in student_after.courses
        ]

    @weight(10)
    def test_enroll_missing(self):
        with self.assertRaises(NotFoundError) as e:
            self.manager.enroll_student(4, 15)
        assert "No course with ID 15." in e.exception.args
        with self.assertRaises(NotFoundError) as e:
            self.manager.enroll_student(15, 4)
        assert "No student with ID 15." in e.exception.args

    @weight(10)
    def test_enroll_existing(self):
        with self.assertRaises(AlreadyExistsError) as e:
            self.manager.enroll_student(1, 1)
        assert "Student is already enrolled in this course" in e.exception.args


if __name__ == "__main__":
    unittest.main(warnings="ignore")
