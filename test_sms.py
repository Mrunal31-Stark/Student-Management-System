import unittest
from unittest.mock import patch
import os
import json
from main import StudentManagementSystem

class TestSMS(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test_students.json'
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.sms = StudentManagementSystem(data_file=self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_add_student(self, mock_print, mock_input):
        # ID, Name, Age, Course, Marks
        mock_input.side_effect = ['101', 'Alice', '20', 'CS', '95']
        self.sms.add_student()
        self.assertEqual(len(self.sms.students), 1)
        self.assertEqual(self.sms.students[0], ['101', 'Alice', '20', 'CS', '95'])

    @patch('builtins.input')
    @patch('builtins.print')
    def test_save_load(self, mock_print, mock_input):
        # Add a student
        mock_input.side_effect = ['102', 'Bob', '22', 'Math', '88']
        self.sms.add_student()
        
        # Save
        self.sms.save_data()
        
        # Load in a new instance
        new_sms = StudentManagementSystem(data_file=self.test_db)
        self.assertEqual(len(new_sms.students), 1)
        self.assertEqual(new_sms.students[0], ['102', 'Bob', '22', 'Math', '88'])

    @patch('builtins.input')
    @patch('builtins.print')
    def test_update_student(self, mock_print, mock_input):
        # Setup student
        self.sms.students.append(['103', 'Charlie', '21', 'Physics', '70'])
        
        # Update name: ID -> '103', Field -> 'Name', New Name -> 'Chuck'
        mock_input.side_effect = ['103', 'Name', 'Chuck']
        self.sms.update_student()
        
        self.assertEqual(self.sms.students[0][1], 'Chuck')

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_student(self, mock_print, mock_input):
        # Setup student
        self.sms.students.append(['104', 'David', '23', 'History', '60'])
        
        # Delete: ID -> '104', Confirm -> 'y'
        mock_input.side_effect = ['104', 'y']
        self.sms.delete_student()
        
        self.assertEqual(len(self.sms.students), 0)

if __name__ == '__main__':
    unittest.main()
