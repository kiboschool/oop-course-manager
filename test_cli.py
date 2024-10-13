from cli import CLI
from unittest.mock import patch, mock_open, call, ANY
import unittest
import json

FAKE_DATA = {
    "students": [
        {"id": "1", "name": "Ope", "courses": []},
        {"id": "2", "name": "Keno", "courses": []},
        {"id": "3", "name": "Mohammed", "courses": []},
        {"id": "4", "name": "Olaperi", "courses": []},
        {"id": "5", "name": "Chukwuemeka", "courses": []},
        {"id": "6", "name": "Oyinloluwa", "courses": []},
        {"id": "7", "name": "Funminiyi", "courses": []},
        {"id": "8", "name": "Michael", "courses": []},
        {"id": "9", "name": "Jacob", "courses": []},
        {"id": "10", "name": "Nekesa", "courses": []},
    ],
    "courses": [
        {"id": "1", "hours": 150, "name": "English", "students": ["1", "2", "3"]},
        {"id": "2", "hours": 150, "name": "Math", "students": ["1"]},
        {"id": "3", "hours": 150, "name": "French", "students": ["1"]},
        {"id": "4", "hours": 150, "name": "Science", "students": ["1"]},
    ],
}


class TestCLI(unittest.TestCase):
    mock_file_content = json.dumps(FAKE_DATA)

    @patch("builtins.open", new_callable=mock_open, read_data=mock_file_content)
    @patch("os.path.exists", value=True)
    def setUp(self, file_mock, _osmock):
        self.file_mock = file_mock
        self.cli = CLI("sqlite://")
        self.cli.manager.initialize_db_schema()
        self.cli.manager.initialize_data(FAKE_DATA)

    @patch("builtins.print")
    def test_show_options(self, mock_print):
        self.cli.show_options()
        mock_print.assert_has_calls(
            [
                call("Please select an option."),
                call("1. Add a student"),
                call("2. Remove a student"),
                call("3. Look up a student"),
                call("4. Add a course"),
                call("5. Enroll a student in a course"),
                call("6. Show students and enrollment"),
                call("7. Quit"),
            ]
        )

    @patch("builtins.input", side_effect=["Test Student"])
    @patch("builtins.print")
    def test_handle_add_student(self, mock_print, mock_input):
        self.cli.handle_choice("1")
        mock_input.assert_called_with("Enter the student's name: ")
        mock_print.assert_called_with("Student added successfully.")

    @patch("builtins.input", side_effect=["1"])
    @patch("builtins.print")
    def test_handle_remove_student(self, mock_print, mock_input):
        self.cli.handle_choice("2")
        mock_input.assert_called_with("Enter the student's ID: ")
        mock_print.assert_called_with("Student removed successfully.")

    @patch("builtins.input", side_effect=["1"])
    @patch("builtins.print")
    def test_handle_lookup_student(self, mock_print, mock_input):
        self.cli.handle_choice("3")
        mock_input.assert_called_with("Enter the student's ID: ")
        mock_print.assert_has_calls(
            [
                call("Student id:", "1"),
                call("Student name:", "Ope"),
                call("Student courses:", ANY),
            ]
        )

    @patch("builtins.input", side_effect=["Test Course", "10"])
    @patch("builtins.print")
    def test_handle_add_course(self, mock_print, mock_input):
        self.cli.handle_choice("4")
        mock_input.assert_has_calls(
            [call("Please enter a course name: "), call("Please enter course hours: ")]
        )
        mock_print.assert_called_with("Course added successfully.")

    @patch("builtins.input", side_effect=["3", "3"])
    @patch("builtins.print")
    def test_handle_enroll_student(self, mock_print, mock_input):
        self.cli.handle_choice("5")
        mock_input.assert_has_calls(
            [call("Please enter a student id: "), call("Please enter a course id: ")]
        )
        mock_print.assert_called_with("Successfully enrolled student in course.")

    @patch("builtins.print")
    def test_handle_show_students(self, mock_print):
        self.cli.handle_choice("6")
        mock_print.assert_has_calls(
            [
                call("Student id", "1"),
                call("Student name", "Ope"),
                call("Student id", "2"),
                call("Student name", "Keno"),
                call("Student id", "3"),
                call("Student name", "Mohammed"),
                call("Student id", "4"),
                call("Student name", "Olaperi"),
                call("Student id", "5"),
                call("Student name", "Chukwuemeka"),
                call("Student id", "6"),
                call("Student name", "Oyinloluwa"),
                call("Student id", "7"),
                call("Student name", "Funminiyi"),
                call("Student id", "8"),
                call("Student name", "Michael"),
                call("Student id", "9"),
                call("Student name", "Jacob"),
                call("Student id", "10"),
                call("Student name", "Nekesa"),
            ],
            any_order=True,
        )

    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "Stanley",
            "Python",
            "15",
            "10",
            "5",
            "10",
            "4",
            "11",
            "1",
        ],
    )
    @patch("builtins.print")
    def test_handle_full_flow(self, mock_print, mock_input):
        # remove 6 students
        self.cli.handle_choice("2")
        self.cli.handle_choice("2")
        self.cli.handle_choice("2")
        self.cli.handle_choice("2")
        self.cli.handle_choice("2")
        self.cli.handle_choice("2")
        # add a student
        self.cli.handle_choice("1")
        # add a class
        self.cli.handle_choice("4")
        # enroll students in classes
        self.cli.handle_choice("5")
        self.cli.handle_choice("5")
        self.cli.handle_choice("5")
        # print the output
        mock_print.reset_mock()
        self.cli.handle_choice("6")
        mock_print.assert_has_calls(
            [
                call("Student id", "7"),
                call("Student name", "Funminiyi"),
                call("Student courses:"),
                call("Student id", "8"),
                call("Student name", "Michael"),
                call("Student courses:"),
                call("Student id", "9"),
                call("Student name", "Jacob"),
                call("Student courses:"),
                call("Student id", "10"),
                call("Student name", "Nekesa"),
                call("Student courses:"),
                call("\t", ANY),
                call("\t", ANY),
                call("Student id", "11"),
                call("Student name", "Stanley"),
                call("Student courses:"),
                call("\t", ANY),
            ],
        )


if __name__ == "__main__":
    unittest.main()
