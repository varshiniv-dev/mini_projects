# create a project of student management system using- oop design, file/ csv/ json storage, add/ update/delete/search student, marks analysis(top,avg,fail list),login system/admin/user
import json
import getpass
import os
import statistics


class Student:
    def __init__(self, student_id, name, marks):
        self.student_id = student_id
        self.name = name
        self.marks = marks

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'marks': self.marks
        }

    @staticmethod
    def from_dict(data):
        return Student(data['student_id'], data['name'], data['marks'])


class StudentManagementSystem:
    def __init__(self, data_file='students.json'):
        self.data_file = data_file
        self.students = self.load_students()

    def load_students(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return [Student.from_dict(student) for student in data]
        return []

    def save_students(self):
        with open(self.data_file, 'w') as f:
            json.dump([student.to_dict() for student in self.students], f)

    def add_student(self, student):
        self.students.append(student)
        self.save_students()

    def update_student(self, student_id, name=None, marks=None):
        for student in self.students:
            if student.student_id == student_id:
                if name:
                    student.name = name
                if marks is not None:
                    student.marks = marks
                self.save_students()
                return True
        return False

    def delete_student(self, student_id):
        self.students = [
            student for student in self.students if student.student_id != student_id]
        self.save_students()

    def search_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def top_students(self, n=3):
        return sorted(self.students, key=lambda s: s.marks, reverse=True)[:n]

    def average_marks(self):
        if not self.students:
            return 0
        return statistics.mean(student.marks for student in self.students)

    def fail_list(self, passing_marks=40):
        return [student for student in self.students if student.marks < passing_marks]


class User:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin


class UserManagementSystem:
    def __init__(self):
        self.users = {
            'admin': User('admin', 'admin123', True),
            'user': User('user', 'user123', False)
        }

    def authenticate(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            return user
        return None


def main():
    ums = UserManagementSystem()
    sms = StudentManagementSystem()

    print("Welcome to the Student Management System")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    user = ums.authenticate(username, password)
    if not user:
        print("Authentication failed!")
        return

    while True:
        print("\nMenu:")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Search Student")
        print("5. Top Students")
        print("6. Average Marks")
        print("7. Fail List")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1' and user.is_admin:
            student_id = input("Student ID: ")
            name = input("Name: ")
            marks = float(input("Marks: "))
            sms.add_student(Student(student_id, name, marks))
            print("Student added successfully.")
        elif choice == '2' and user.is_admin:
            student_id = input("Student ID to update: ")
            name = input("New Name (leave blank to keep unchanged): ")
            marks_input = input("New Marks (leave blank to keep unchanged): ")
            marks = float(marks_input) if marks_input else None
            if sms.update_student(student_id, name if name else None, marks):
                print("Student updated successfully.")
            else:
                print("Student not found.")
        elif choice == '3' and user.is_admin:
            student_id = input("Student ID to delete: ")
            sms.delete_student(student_id)
            print("Student deleted successfully.")
        elif choice == '4':
            student_id = input("Student ID to search: ")
            student = sms.search_student(student_id)
            if student:
                print(
                    f"Found Student - ID: {student.student_id}, Name: {student.name}, Marks: {student.marks}")
            else:
                print("Student not found.")
        elif choice == '5':
            top_students = sms.top_students()
            print("Top Students:")
            for student in top_students:
                print(
                    f"ID: {student.student_id}, Name: {student.name}, Marks: {student.marks}")
        elif choice == '6':
            avg_marks = sms.average_marks()
            print(f"Average Marks: {avg_marks}")
        elif choice == '7':
            fails = sms.fail_list()
            print("Fail List:")
            for student in fails:
                print(
                    f"ID: {student.student_id}, Name: {student.name}, Marks: {student.marks}")
        elif choice == '8':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice or insufficient permissions.")


if __name__ == "__main__":
    main()

    def run_as_module():
        pass
else:
    print("This module is intended to be run as a standalone program.")

    def run_as_module():
        pass
    run_as_module()
