from enrollment_manager_db import EnrollmentManagerDB

# from enrollment_manager_json import EnrollmentManagerJSON
from enrollment_manager import AlreadyExistsError, NotFoundError

# DEFAULT_FILE = "courses.json"
DEFAULT_FILE = "sqlite:///courses.db"


class CLI:
    def __init__(self, path=DEFAULT_FILE):
        self.manager = EnrollmentManagerDB(path)

    def run(self):
        while True:
            self.show_options()
            choice = input("")
            self.handle_choice(choice)
            input("Press Enter to continue.")

    def show_options(self):
        print()
        print()
        print("Please select an option.")
        print("1. Add a student")
        print("2. Remove a student")
        print("3. Look up a student")
        print("4. Add a course")
        print("5. Enroll a student in a course")
        print("6. Show students and enrollment")
        print("7. Quit")
        print("8. Search for student by name")
        print()

    def handle_choice(self, choice):
        try:
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.remove_student()
            elif choice == "3":
                self.lookup_student()
            elif choice == "4":
                self.add_course()
            elif choice == "5":
                self.enroll_student()
            elif choice == "6":
                self.show_students_and_enrollment()
            elif choice == "7":
                exit()
            elif choice == "8":
                self.search_student()
            else:
                print("Invalid choice. Please try again.")
        except NotFoundError as not_found:
            print(not_found)
        except AlreadyExistsError as already_exists:
            print(already_exists)

    def add_student(self):
        new_student_name = input("Enter the student's name: ")
        self.manager.add_student(new_student_name)
        print("Student added successfully.")

    def remove_student(self):
        student_id_to_remove = input("Enter the student's ID: ")
        self.manager.remove_student(student_id_to_remove)
        print("Student removed successfully.")

    def lookup_student(self):
        student_id_to_lookup = input("Enter the student's ID: ")
        student = self.manager.lookup_student(student_id_to_lookup)
        print("Student id:", str(student["id"]))
        print("Student name:", student["name"])
        print("Student courses:", student["courses"])

    def search_student(self):
        student_name_to_search = input("Enter a name to search: ")
        students = self.manager.search_students_by_name(student_name_to_search)
        if len(students) > 0:
            for student in students:
                print("Student id:", str(student["id"]), "name:", student["name"])
        else:
            print("No students found")

    def add_course(self):
        new_course_name = input("Please enter a course name: ")
        new_course_hours = input("Please enter course hours: ")

        self.manager.add_course(new_course_name, new_course_hours)
        print("Course added successfully.")

    def enroll_student(self):
        student_id_to_enroll = input("Please enter a student id: ")
        course_id_to_enroll = input("Please enter a course id: ")
        self.manager.enroll_student(student_id_to_enroll, course_id_to_enroll)
        print("Successfully enrolled student in course.")

    def show_students_and_enrollment(self):
        for student in self.manager.get_students():
            print("Student id", str(student["id"]))
            print("Student name", student["name"])
            print("Student courses:")
            for course in student["courses"]:
                print("\t", course)
