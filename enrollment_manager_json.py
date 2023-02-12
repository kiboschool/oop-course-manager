import os
import json
from enrollment_manager import EnrollmentManager, NotFoundError, AlreadyExistsError


class EnrollmentManagerJSON(EnrollmentManager):
    def __init__(self, filename):
        self._students = []
        self._courses = []
        self.filename = filename
        self.initialize_data(None)

    def _next_student_id(self):
        if len(self._students) == 0:
            return 1
        else:
            return int(self._students[-1]["id"]) + 1

    def _next_course_id(self):
        if len(self._courses) == 0:
            return 1
        else:
            return int(self._courses[-1]["id"]) + 1

    # initializes based on file, not the passed-in data
    def initialize_data(self, data):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                persisted = json.load(f)
                self._students = persisted["students"]
                self._courses = persisted["courses"]
        return self

    def save(self):
        to_persist = {"students": self._students, "courses": self._courses}
        if os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump(to_persist, f)

    def get_students(self):
        return self._students

    def get_courses(self):
        return self._courses

    def add_student(self, new_student_name):
        new_student_id = self._next_student_id()
        self._students.append(
            {"id": new_student_id, "name": new_student_name, "courses": []}
        )
        self.save()

    def remove_student(self, student_id_to_remove):
        for student in self.get_students():
            if str(student["id"]) == str(student_id_to_remove):
                self._students.remove(student)
                self.save()
                return
        # if can't find the student
        raise NotFoundError(f"No student with ID {student_id_to_remove}.")

    def lookup_student(self, student_id_to_lookup):
        for student in self.get_students():
            if str(student["id"]) == str(student_id_to_lookup):
                return student
        # if can't find the student
        raise NotFoundError(f"No student with ID {student_id_to_lookup}.")

    def lookup_course(self, course_id_to_lookup):
        for course in self.get_courses():
            if str(course["id"]) == str(course_id_to_lookup):
                return course
        # if can't find the course
        raise NotFoundError(f"No course with ID {course_id_to_lookup}.")

    def add_course(self, new_course_name, new_course_hours):
        new_course_id = self._next_course_id()
        new_course = {
            "id": new_course_id,
            "name": new_course_name,
            "hours": new_course_hours,
            "students": [],
        }
        self._courses.append(new_course)
        self.save()

    def enroll_student(self, student_id_to_enroll, course_id_to_enroll):
        student = self.lookup_student(student_id_to_enroll)
        course = self.lookup_course(course_id_to_enroll)

        if str(student["id"]) in course["students"]:
            raise AlreadyExistsError("Student is already enrolled in this course")

        student["courses"].append(course)
        course["students"].append(student["id"])
        self.save()
