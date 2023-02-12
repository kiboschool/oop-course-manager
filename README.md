# Course Enrollment Manager OOP

## Introduction

In Programming 1, there was a project to create a Student Enrollment system. This system kept a list of students and courses, and the courses each student was enrolled in. In this project, you'll work with an object-oriented version of the Enrollment Manager. You'll practice with lots of the concepts you've seen: inheritance, data and files, databases and ORMs, and custom errors.

This project has more files and lines of code than prior projects. Larger projects are more authentic to the real world, but it also requires more time to explore the code, trace the behavior, and understand how things tie together.

## Starter code

Let's quickly walk through the starter code files and their descriptions:

- `cli.py` has a class for the interactive program. It relies on an implementation of an EnrollmentManager class to manage the data.
- `courses.json` and `courses.db` are JSON and sqlite database files with sample data for students, courses, and enrollments.
- `enrollment_manager_db.py` is an implementation of the enrollment manager that stores data in a database. It uses the SQLAlchemy ORM.
- `enrollment_manager_json.py` is an implementation of the enrollment manager that stores data in a JSON file.
- `enrollment_manager.py` is a _base_ class. It doesn't actually implement any of the methods, but the JSON-backed and Database-backed subclasses both implement its methods.
- `main.py` creates an instance of the `CLI` class and runs it. It's how you start the interactive program.
- `models.py` has the SQLAlchemy database models for the database-backed implementation in  `enrollment_manager_db.py`
- The `test_*.py` files have tests for the CLI and the two implementations of the EnrollmentManager.

## Your Task

In Part 1, you'll fix some representation bugs in the Enrollment Manager application by switching from a JSON-backed to a database-backed implementation. You'll have to implement some of the missing functionality in the EnrollmentManagerDB class first.

In Part 2, you'll add some functionality to the application, and adjust some test cases.

### Getting Started

`requirements.txt` lists the packages required for the project. Install them using `pip`.

```sh
pip install -r requirements.txt
```

If you are using a virtual environment, be sure to create and initialize it before you install the requirements.

- Run `python main.py` to run the interactive CLI program.
- Run `python -m unittest` (or `pytest`, if it's installed) to run the tests.

## Part 1: Bugs in the JSON implementation

### Replicating the bug

Your Senior Engineer colleague noticed some bugs in the existing JSON implementation of the enrollment manager. If you remove a student, it doesn't remove their id from the courses they are enrolled in. Also, if you add another student, the implementation might re-use the id of the student that was removed. Then the new student might show up as enrolled in courses that they weren't supposed to be.

Before you get started changing the code, try to _replicate_ the bug.

1. Run the interactive program with `python main.py`.
2. Enroll student 10 in course 2.
3. Then, remove student 10.
4. Finally, add another student, and then show all the students and enrollments.

You should see that the new student 10 has the enrollments of the old student 10.

### Fixing the bug

Your colleague analyzed the source of the bug and considered different fixes. You could try to loop through all the courses and check all their enrollments when removing a student, but that seems slow and error-prone. You could change the representation in JSON so that `enrollments` were kept in another array, apart from students and courses. Then, there'd have to be some (again, slow and error-prone) logic to figure out which students are enrolled in which courses.

Instead of trying to fix the JSON-backed version, your colleague decided to use a proper database instead. If there was an association table "enrollments" between courses and students, these kinds of bugs wouldn't happen.

They started writing the ORM-backed version, but then got pulled away onto another task, and asked you to finish the work. Here's what they said:

> I'm switching the CLI to use a sqlite-backed version of the EnrollmentManager, called EnrollmentManagerDB. I've written the models in `models.py` and started the new class in `EnrollmentManagerDB.py`, but it's not quite finished. I added the methods to work with students, but not with courses.
> I need you to finish the class, then swap the CLI to use the new database version instead of the old JSON version of the manager.
> The test coverage is pretty good, so if you pass the db and cli tests, you should be good to go.

1. Fill in the missing methods of `EnrollmentManagerDB`, so that it passes the tests in `test_enrollment_manager_db.py`
  - `get_courses` should select all the courses
  - `add_course` should create a new course
  - `lookup_course` should find a single course by id. If there's no course with that id, it should raise a `NotFoundError` with the message `"No course with ID {id}."`.
  - `enroll_student` should enroll a student in a course.
    - first, it should find the student and course using the `lookup_student` and `lookup_course` methods
    - then, it should create a new `Enrollment` with the `course` and `student` and add it to the session
    - next, it should call `session.commit()` to ensure the new enrollment is persisted
    - if there is already an enrollment for that student and course, SQLite will raise an `IntegrityError` because of the unique constraint violation. `enroll_student` should catch this error and raise an `AlreadyExistsError` instead, with the message `"Student is already enrolled in this course"`.
2. Change `cli.py` to use `EnrollmentManagerDB` instead of `EnrollmentManagerJSON`

Run all the tests. All the tests should pass at this point.

### Part 2: Adding functionality

You did a great job fixing the CLI to use the database, and you've still got some time. You look in the issue backlog, and notice that there's another request for an improvement to the EnrollmentManager.

It's quite awkward to look students up by id, and several customers have requested the ability to search for students by name. The CLI should have a new option to find a student by name. Now that we have a database-backed version of the EnrollmentManager, it should be possible to use an `ILIKE` query to do a case-insensitive match on text.

Add this feature to the EnrollmentManagerDB and CLI classes.

1. In `test_enrollment_manager_db.py`, unskip the test for `search_students_by_name`. If you run the tests, they should now have one failing test.
2. Implement the `search_students_by_name` function in `EnrollmentManagerDB`. (See [this Stackoverflow answer](https://stackoverflow.com/a/54672057/3574917) for a hint on how to use ilike). The tests should pass again.
3. Add an option to the CLI to search by name. You'll need to edit `show_options` and `handle_choice`, and add a new function that performs the search.
4. Run the application `python main.py` and test out your changes to the CLI.

### BONUS: Fix the CLI tests

Since you added an option, it's likely that some of the CLI tests are failing now -- especially if you added the option to the middle of the list.

Update the tests so that they are checking the new behavior.
- Update the test for `show_options` so that it is testing for the right options
- Update any of the numbers passed to `handle_options` in the other tests that no longer match your implementation in CLI
- Add new tests to the CLI to check the behavior of the new option to search by name
  - Add tests to handle the case where there are search results, and where there are none

The CLI tests won't count towards the autograder

## Rubric

Points | Criteria | Description
--------- | ------- | ---------
80 | Autograder | The autograder will run the unit tests in `test_enrollment_manager_db.py`. If those all pass, you'll get full autograder points.
20 | Code organization | Code is styled well, organized effectively, uses good variable names, comments are clear and appropriate.
+10 | Bonus | Fixed the tests for the CLI, and added a test of the new CLI option to search for a student by name