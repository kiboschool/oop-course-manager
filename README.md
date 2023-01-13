# Course Enrollment OOP

In Programming 1, one of the projects was to create a Student Enrollment system. This system kept a list of students and which courses they were enrolled in, a much better way for the school to keep this information than to use paper records.

You'll now be creating a new Student Enrollment system, one that builds on of your knowledge of classes and objects. It will now be written with "OOP" - Object-Oriented Programming.

## Your Task

We have provided two working files, `main.py` and `course_enrollment.py`. You can try running these files and see what the program does. Just like the Programming 1 project, the program keeps a list of students and courses and lets people use a menu to mark students as being enrolled in a course.

There are many steps in this list, but don't worry, each step should be fairly simple!

* First, create a new file, `enrollment_manager.py`
* In this file, create a class called EnrollmentManager
* Write an `init` method for the class. In this method, create two member variables for the class, `students` and `courses`, and set them to be empty lists.
* Now, take each of the functions from `course_enrollment.py` and do this:
   * Make a method with the same name inside of the EnrollmentManager class.
   * Copy the code for that function over into the method, but have it use the `students` and `courses` member variables you created earlier.
   * 💡Hint: remember that the method you just made will need to have different parameters than the function did.
   * Delete the function from `course_enrollment.py`
* (It's ok that the program won't work for a bit while you are making these changes.)
* You can now get a working program going - at the top of `main.py` you can import the enrollment_manager file, and create an object that is an instance of the EnrollmentManager class.
* Modify the code in `main.py` so that it calls the methods on the object.
* Finally, you'll add persistence (loading and saving):
  * Add a way for an `EnrollmentManager` to save data to a file on disk.
  * Add a way for `EnrollmentManager` to load data from a saved file.
  * Edit `main.py` so that the program automatically saves and loads data.


## Requirements

* The program should be able to add students, add courses, and enroll students into a course, just like it did before.
* The program should be able to save its data to disk, and read the same data back the next time the program runs.
* The program must have an EnrollmentManager class. (You don't need any other classes, though).
* Please do not change any of the function or method names.


## Rubric

Points | Criteria | Description
--------- | ------- | ---------
30 | Program runs without errors | No errors found when running the program and entering different and unexpected user input
10 | Showing students | Looking up students and showing enrollments works correctly.
10 | Managing students | Adding and removing students works correctly
10 | Managing courses | Adding a course works correctly
10 | Managing enrollments | Enrolling a student to a course works correctly, and the program will not let you enroll a student again if they are already enrolled in the course
15 | Persistence | Data is saved to a file, and when the program starts again, saved data is loaded successfully
15 | Code organization | Code is styled well, organized effectively, uses good variable names, comments are clear and appropriate




