import json
import os

class StudentManagementSystem:
    def __init__(self, data_file='students.json'):
        self.data_file = data_file
        self.students = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.students = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.students = []
        else:
            self.students = []

    def save_data(self):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.students, f, indent=4)
            return True, "Data saved successfully."
        except IOError as e:
            return False, f"Error saving data: {e}"

    def student_exists(self, student_id):
        for s in self.students:
            if s[0] == student_id:
                return True
        return False

    def add_student(self, student_id, name, age, course, marks):
        if self.student_exists(student_id):
            return False, "Error: Student ID already exists."

        # Validate numbers
        if not age.isdigit():
            return False, "Invalid age. Please enter a number."
        
        # Simple float check for marks
        if not marks.replace('.', '', 1).isdigit():
            return False, "Invalid marks. Please enter a number."

        row = [student_id, name, age, course, marks]
        self.students.append(row)
        return True, "Student added successfully!"

    def get_all_students(self):
        return self.students

    def search_student(self, search_name):
        return [s for s in self.students if search_name.lower() in s[1].lower()]

    def update_student(self, update_id, field, value):
        for student in self.students:
            if student[0] == update_id:
                if field.lower() == 'name':
                    student[1] = value
                elif field.lower() == 'age':
                    if not value.isdigit():
                        return False, "Invalid age."
                    student[2] = value
                elif field.lower() == 'course':
                    student[3] = value
                elif field.lower() == 'marks':
                    if not value.replace('.', '', 1).isdigit():
                        return False, "Invalid marks."
                    student[4] = value
                else:
                    return False, "Invalid detail type."
                
                return True, "Student details updated successfully!"
        
        return False, "Invalid Student ID."

    def delete_student(self, delete_id):
        for i, student in enumerate(self.students):
            if student[0] == delete_id:
                del self.students[i]
                return True, "Student deleted successfully!"
        return False, "Invalid Student ID."


# CLI Handler to maintain original functionality
def run_cli():
    sms = StudentManagementSystem()
    
    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Save & Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\n--- Add Student ---")
            sid = input("Enter Student ID: ")
            name = input("Enter Student Name: ")
            age = input("Enter Student Age: ")
            course = input("Enter Student Course: ")
            marks = input("Enter Student Marks: ")
            success, msg = sms.add_student(sid, name, age, course, marks)
            print(msg)

        elif choice == '2':
            print("\n--- View Students ---")
            students = sms.get_all_students()
            if not students:
                print("No students found.")
            else:
                print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Course':<15} {'Marks':<10}")
                print("-" * 60)
                for s in students:
                    print(f"{s[0]:<10} {s[1]:<20} {s[2]:<5} {s[3]:<15} {s[4]:<10}")

        elif choice == '3':
            print("\n--- Search Student ---")
            name = input("Enter the name of the student to search: ")
            found = sms.search_student(name)
            if not found:
                print("Student not found.")
            else:
                print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Course':<15} {'Marks':<10}")
                print("-" * 60)
                for s in found:
                    print(f"{s[0]:<10} {s[1]:<20} {s[2]:<5} {s[3]:<15} {s[4]:<10}")

        elif choice == '4':
            print("\n--- Update Student ---")
            uid = input("Enter Student ID to update: ")
            if not sms.student_exists(uid):
                print("Invalid Student ID.")
                continue
            
            # Show update options
            print("Updating details. Which detail do you want to update? (Name, Age, Course, Marks)")
            field = input("Enter your choice: ")
            val = input(f"Enter new {field}: ")
            success, msg = sms.update_student(uid, field, val)
            print(msg)

        elif choice == '5':
            print("\n--- Delete Student ---")
            did = input("Enter Student ID to delete: ")
            if sms.student_exists(did):
                if input(f"Are you sure you want to delete ID {did}? (y/n): ").lower() == 'y':
                    success, msg = sms.delete_student(did)
                    print(msg)
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid Student ID.")

        elif choice == '6':
            success, msg = sms.save_data()
            print(msg)
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    run_cli()
