import course_enrollment

def main_menu():
    students = []
    courses = []
    while True:        
        print("")
        print("")
        print("Please select an option,")
        print("1. Add a student")
        print("2. Remove a student")
        print("3. Look up a student")
        print("4. Add a course")
        print("5. Enroll a student in a course")
        print("6. Show students and enrollment")
        print("7. Quit")
        print()

        choice = input("")
        if choice == "1":
          course_enrollment.add_student(students, courses)
        elif choice == "2":
          course_enrollment.remove_student(students, courses)
        elif choice == "3":
          course_enrollment.lookup_student(students, courses)
        elif choice == "4":
          course_enrollment.add_course(students, courses)
        elif choice == "5":
          course_enrollment.enroll_student(students, courses)
        elif choice == "6":
          course_enrollment.show_students_and_enrollment(students, courses)
        elif choice == "7":
          return
        else:
          print("Invalid choice. Please try again.")


main_menu()

