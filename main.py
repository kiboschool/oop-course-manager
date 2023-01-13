
import persistence


def main_menu():
    enrollment_manager = persistence.load()
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
          enrollment_manager.add_student()
          persistence.save(enrollment_manager)
        elif choice == "2":
          enrollment_manager.remove_student()
          persistence.save(enrollment_manager)
        elif choice == "3":
          enrollment_manager.lookup_student()
        elif choice == "4":
          enrollment_manager.add_course()
          persistence.save(enrollment_manager)
        elif choice == "5":
          enrollment_manager.enroll_student()
          persistence.save(enrollment_manager)
        elif choice == "6":
          enrollment_manager.show_students_and_enrollment()
        elif choice == "7":
          return
        else:
          print("Invalid choice. Please try again.")


main_menu()

