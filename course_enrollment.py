
def add_student(students, courses):
    new_student_id = input("Enter the student's ID: ")
    new_student_name = input("Enter the student's name: ")
    for student in students:
        if student['id'] == new_student_id:
            print('There is already a student with this ID.')
            return
    
    course_ids = []
    students.append({'id': new_student_id, 'name': new_student_name, 'course_ids': course_ids})
    print('Student added successfully.')
    
    
def remove_student(students, courses):
    student_id_to_remove = input("Enter the student's ID: ")
    for student in students:
        if student['id'] == student_id_to_remove:
            students.remove(student)
            print('Student removed succesfully.')
            return
    print('Could not find a student with this ID.')
    
def lookup_student(students, courses):
    student_id_to_lookup = input("Enter the student's ID: ")
    for student in students:
        if student['id'] == student_id_to_lookup:
            print('Student id:', student['id'])
            print('Student name:', student['name'])
            print('Student courses:', student['course_ids'])
            return
            
    print('Could not find a student with this ID.')
    
def add_course(students, courses):
    new_course_id = input("Please enter a course ID: ")
    new_course_name = input("Please enter a course name: ")
    new_course_hours = input("Please enter course hours: ")
    for course in courses:
        if course['id'] == new_course_id:
            print('There is already a course with this ID.')
            return
    
    course_student_ids = []
    new_course = {'id': new_course_id, 'name': new_course_name, 'hours': new_course_hours, 'student_ids': course_student_ids}
    courses.append(new_course)
    print('Course added successfully.')
    
def enroll_student(students, courses):
    student_id_to_enroll = input("Please enter a student id: ")
    course_id_to_enroll = input("Please enter a course id: ")
    course_exists = False
    for course in courses:
        if course['id'] == course_id_to_enroll:
            course_exists = True
            
    if not course_exists:
        print('Course not found')
        return
    
    for student in students:
        if student['id'] == student_id_to_enroll:
            # this is an easy way to see if an item exists in a list,
            # for example `if 'a' in ['a', 'b', 'c']: return True`
            if course_id_to_enroll in student['course_ids']:
                print('Student is already enrolled in this course')
                return
            else:
                student['course_ids'].append(course_id_to_enroll)
                print('Successfully enrolled student in course')
                return
    
    print("Could not find student with this ID.")
    
def show_students_and_enrollment(students, courses):
    for student in students:
        print('Student id', student['id'])
        print('Student name', student['name'])
        print('Student courses:')
        for course_id in student['course_ids']:
            print('\t' + course_id)
    
    
