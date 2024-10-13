from sqlalchemy import select, delete, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import Enrollment, Student, Course, Base
from enrollment_manager import EnrollmentManager, AlreadyExistsError, NotFoundError


class EnrollmentManagerDB(EnrollmentManager):
    # set logging=True to log all SQL queries
    def __init__(self, path="sqlite:///courses.db", logging=False):
        self.engine = create_engine(path, echo=logging)
        Session = sessionmaker(self.engine)
        self.session = Session()

    def initialize_db_schema(self):
        Base.metadata.create_all(self.engine)

    # seed db data using a dict
    def initialize_data(self, data):
        for student in data["students"]:
            self.session.add(Student(name=student["name"]))
        for (course_id, course) in enumerate(data["courses"], start=1):
            self.session.add(Course(name=course["name"], hours=course["hours"]))
            for student_id in course["students"]:
                self.session.add(Enrollment(student_id=student_id, course_id=course_id))
        self.session.commit()

    def get_students(self):
        return self.session.scalars(select(Student)).all()

    def add_student(self, new_student_name):
        self.session.add(Student(name=new_student_name))
        self.session.commit()

    def remove_student(self, student_id_to_remove):
        count = self.session.execute(
            delete(Student).where(Student.id == student_id_to_remove)
        ).rowcount
        self.session.commit()
        if count == 0:
            raise NotFoundError(f"No student with ID {student_id_to_remove}.")

    def lookup_student(self, student_id_to_lookup):
        result = self.session.get(Student, student_id_to_lookup)
        if result == None:
            raise NotFoundError(f"No student with ID {student_id_to_lookup}.")
        return result

    def search_students_by_name(self, name_to_lookup):
        return (
            self.session.query(Student)
            .filter(Student.name.ilike("%" + name_to_lookup + "%"))
            .all()
        )

    def get_courses(self):
        raise NotImplementedError

    def add_course(self, new_course_name, new_course_hours):
        raise NotImplementedError

    def lookup_course(self, course_id_to_lookup):
        raise NotImplementedError

    def enroll_student(self, student_id_to_enroll, course_id_to_enroll):
        raise NotImplementedError
