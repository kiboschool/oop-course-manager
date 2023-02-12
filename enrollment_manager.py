# custom errors to raise in certain situations
class AlreadyExistsError(Exception):
    pass


class NotFoundError(Exception):
    pass


# The interface for the enrollment manager
# This class doesn't implement any of the methods; they are all implemented in the subclasses
class EnrollmentManager:
    def __init__(self):
        raise NotImplementedError

    def initialize_db_schema(self):
        pass

    def initialize_data(self, data):
        raise NotImplementedError

    def get_students(self):
        raise NotImplementedError

    def get_courses(self):
        raise NotImplementedError

    def add_student(self, new_student_name):
        raise NotImplementedError

    def remove_student(self, student_id_to_remove):
        raise NotImplementedError

    def lookup_student(self, student_id_to_lookup):
        raise NotImplementedError

    def lookup_course(self, course_id_to_lookup):
        raise NotImplementedError

    def add_course(self, new_course_name, new_course_hours):
        raise NotImplementedError

    def enroll_student(self, student_id_to_enroll, course_id_to_enroll):
        raise NotImplementedError
