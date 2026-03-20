import csv
import base64
import time
from statistics import mean,median



class Role:
    STUDENT = "student"
    PROFESSOR = "professor"
    ADMIN = "admin"
    UNKNOWN = "unknown"

class User:
    def __init__(self, email, password, role = Role.UNKNOWN):
        self.email = email
        self.password = password
        self.role = role
        self.inputFile = "database/login.csv"

    def encryptPassword(password):
        return base64.b64encode(password.encode()).decode()

    def decryptPassword(encoded_password):
        return base64.b64decode(encoded_password.encode()).decode()

    def login(self):
        try:
            with open(self.inputFile, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if self.email == row["email"]:
                        decrypted_password = User.decryptPassword(row["password"])
                        if self.password == decrypted_password:
                            self.role = row["role"]
                            print("Login successful", self.role)
                            return True
                        else:
                            print("Error - Incorrect password")
                            return False
                print("Error - Email not found")
                return False
        except Exception as e:
            print("Error - cannot login, internal error", e)
            return False

    def logout(self):
        if self.role == Role.UNKNOWN:
            print("Error - User is not logged in")
        self.role = Role.UNKNOWN
        print("Logged out successfully")

    def change_password(self, new_password):
        if self.role == Role.UNKNOWN:
            print("Error - User not logged in: Cannot update password")
            return
        try:
            with open(self.inputFile, "r") as file:
                reader = list(csv.DictReader(file))
                fieldnames = reader[0].keys()
            for row in reader:
                if row["email"] == self.email:
                    row["password"] = User.encryptPassword(new_password)
                    break
            with open(self.inputFile, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(reader)
            self.password = new_password
            print("Password updated successfully")
        except Exception as e:
            print("Error - Cannot update password, internal error", e)

# ------------------- Course Class -------------------
class Course:
    def __init__(self, course_id, course_name, credits, description):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.description = description

    def display_course_details(self):
        print("Course details:")
        print(f"Course ID      : {self.course_id}")
        print(f"Course Name    : {self.course_name}")
        print(f"Credits        : {self.credits}")
        print(f"Description    : {self.description}")

    def loadCourse(course_id):
        try:
            with open("database/courses.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["id"] == course_id:
                        return Course(
                            row["id"],
                            row["name"],
                            int(row["credits"]),
                            row["description"]
                        )
            print("Error - Course not found")
            return None
        except Exception as e:
            print("Error - Cannot load course", e)
            return None

# ------------------- Professor Class -------------------
class Professor(User):
    def __init__(self, email, password, role, name, rank, course_ids):
        super().__init__(email, password, role)
        self.name = name
        self.rank = rank
        self.course_ids = course_ids

    def displayMenu(self):
        while True:
            print("\n----- Professor Menu -----")
            print("1. View My Details")
            print("2. Show Course Details")
            print("3. Modify My Details")
            print("4. Course Statistics")
            print("5. Search Student")
            print("6. Sort Students by Name")
            print("7. Sort Students by Marks")
            print("8. Change Password")
            print("9. Logout")
            choice = input("Enter choice: ")
            
            if choice == "1":
                self.professor_details()
            elif choice == "2":
                self.show_course_details_by_professor()
            elif choice == "3":
                new_name = input("Enter new name: ")
                new_rank = input("Enter new rank: ")
                self.modify_details(new_name, new_rank)
            elif choice == "4":
                self.course_statistics()
            elif choice == "5":
                email = input("Enter student email to search: ")
                self.search_student(email)
            elif choice == "6":
                self.sort_students_by_name()
            elif choice == "7":
                course_id = input("Enter course ID to sort students by marks: ")
                self.sort_students_by_marks(course_id)
            elif choice == "8":
                new_pass = input("Enter new password: ")
                self.change_password(new_pass)
            elif choice == "9":
                self.logout()
                break
            else:
                print("Error - Invalid choice")
    
    @staticmethod
    def loadProfessor(email, password):
        import os
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(BASE_DIR, "database", "professors.csv")

            with open(file_path, "r") as file:
                reader = csv.DictReader(file)

                name = ""
                rank = ""
                course_list = []

                for row in reader:
                    if row["email"] == email:
                        name = row["name"]
                        rank = row["rank"]
                        if row["courseId"]:
                            course_list.append(row["courseId"])

                if name == "":
                    print("Error - Professor not found")
                    return None

                return Professor(email, password, Role.PROFESSOR, name, rank, course_list)

        except Exception as e:
            print("Error - Cannot load professor", e)
            return None


    # --- Existing functions ---
    def professor_details(self):
        print("--------------------------------------------------")
        print(f"Email      : {self.email}")
        print(f"Name       : {self.name}")
        print(f"Rank       : {self.rank}")
        print(f"Courses    : {', '.join(self.course_ids)}")
        print("--------------------------------------------------")

    def show_course_details_by_professor(self):
        if not self.course_ids:
            print("Error - No courses assigned")
            return
        for course_id in self.course_ids:
            course = Course.loadCourse(course_id)
            if course:
                course.display_course_details()

    def modify_details(self, new_name, new_rank):
        try:
            with open("database/professors.csv", "r") as file:
                reader = list(csv.DictReader(file))
                fieldnames = reader[0].keys()
            for row in reader:
                if row["email"] == self.email:
                    row["name"] = new_name
                    row["rank"] = new_rank
                    break
            with open("database/professors.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(reader)
            self.name = new_name
            self.rank = new_rank
            print("Professor details updated successfully")
        except Exception as e:
            print("Error - Cannot update professor details", e)


    # --- New Professor Methods ---

    # 1️⃣ Statistics for professor courses
    def course_statistics(self):
        if not self.course_ids:
            print("Error - No courses assigned")
            return
        for course_id in self.course_ids:
            marks = []
            try:
                with open("database/students.csv", "r") as file:
                    for row in csv.DictReader(file):
                        if row["courseId"] == course_id:
                            marks.append(int(row["marks"]))
                if marks:
                    print(f"\nStatistics for course {course_id}:")
                    print(f"Average marks: {mean(marks)}")
                    print(f"Median marks : {median(marks)}")
                else:
                    print(f"No students found for course {course_id}")
            except Exception as e:
                print(f"Error - Cannot compute statistics for {course_id}", e)

    #  Search student
    def search_student(self, email):
        start = time.time()
        found = False
        try:
            with open("database/students.csv", "r") as file:
                for row in csv.DictReader(file):
                    if row["email"] == email and row["courseId"] in self.course_ids:
                        found = True
                        print(f"Found student: {row['firstName']} {row['lastName']} - {row['email']}")
                        break
            if not found:
                print("Student not found in your courses")
        except Exception as e:
            print("Error - cannot search student", e)
        end = time.time()
        print(f"Time taken: {end-start:.6f} seconds")

    # 3️⃣ Sort students by name (only for their courses)
    def sort_students_by_name(self):
        try:
            students = []
            with open("database/students.csv", "r") as file:
                for row in csv.DictReader(file):
                    if row["courseId"] in self.course_ids:
                        students.append(row)
            students.sort(key=lambda x: (x["firstName"], x["lastName"]))
            print("Students sorted by name:")
            for s in students:
                print(f"{s['firstName']} {s['lastName']} - {s['email']} - Course: {s['courseId']}")
        except Exception as e:
            print("Error - cannot sort students", e)

    # 4️⃣ Sort students by marks (only for their courses)
    def sort_students_by_marks(self, course_id):
        if course_id not in self.course_ids:
            print("Error - You do not teach this course")
            return
        try:
            students = []
            with open("database/students.csv", "r") as file:
                for row in csv.DictReader(file):
                    if row["courseId"] == course_id:
                        students.append(row)
            students.sort(key=lambda x: int(x["marks"]), reverse=True)
            print(f"Students sorted by marks for course {course_id}:")
            for s in students:
                print(f"{s['firstName']} {s['lastName']} - {s['marks']}")
        except Exception as e:
            print("Error - cannot sort students by marks", e)

# ------------------- Student Class -------------------
class Student(User):
    def __init__(self, email, password, role, first_name, last_name, grade_report):
        super().__init__(email, password, role)
        self.first_name = first_name
        self.last_name = last_name
        self.grade_report = grade_report

    def loadStudent(email, password):
        try:
            with open("database/students.csv", "r") as file:
                reader = csv.DictReader(file)
                first_name = ""
                last_name = ""
                grade_report = {}
                for row in reader:
                    if row["email"] == email:
                        first_name = row["firstName"]
                        last_name = row["lastName"]
                        grade_report[row["courseId"]] = {
                            "grade": row["grade"],
                            "marks": row["marks"]
                        }
                if first_name == "":
                    return None
                return Student(email, password,Role.STUDENT, first_name, last_name, grade_report)
        except Exception as e:
            print("Error - Cannot load student", e)
            return None

    def check_your_marks(self):
        print("Here are your marks")
        for course_id, data in self.grade_report.items():
            print(f"{course_id} : {data['marks']}")

    def check_your_grade(self):
        print("Here are your grades")
        for course_id, data in self.grade_report.items():
            print(f"{course_id} : {data['grade']}")

    def display_records(self):
        print("Student record:")
        print(f"Name   : {self.first_name} {self.last_name}")
        print(f"Email  : {self.email}")
        print("Course Details:")
        for course_id, data in self.grade_report.items():
            print(f"Course ID : {course_id}")
            print(f"Grade     : {data['grade']}")
            print(f"Marks     : {data['marks']}")

    def update_student_record(self, new_first_name, new_last_name):
        try:
            with open("database/students.csv", "r") as file:
                reader = list(csv.DictReader(file))
                fieldnames = reader[0].keys()
            for row in reader:
                if row["email"] == self.email:
                    row["firstName"] = new_first_name
                    row["lastName"] = new_last_name
            with open("database/students.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(reader)
            self.first_name = new_first_name
            self.last_name = new_last_name
            print("Student details updated successfully")
        except Exception as e:
            print("Error - Cannot update student details", e)

    def calculate_average(self):
        marks = [int(data['marks']) for data in self.grade_report.values()]
        if marks:
            avg = sum(marks)/len(marks)
            print("Average marks:", avg)
        else:
            print("No marks available")

    def calculate_median(self):
        marks = [int(data['marks']) for data in self.grade_report.values()]
        if marks:
            med = median(marks)
            print("Median marks:", med)
        else:
            print("No marks available")

    def displayMenu(self):
        while True:
            print("\n----- Student Menu -----")
            print("1. View My Records")
            print("2. Check My Marks")
            print("3. Check My Grades")
            print("4. Update My Name")
            print("5. Change Password")
            print("6. Logout")
            choice = input("Enter choice: ")
            if choice == "1":
                self.display_records()
            elif choice == "2":
                self.check_your_marks()
            elif choice == "3":
                self.check_your_grade()
            elif choice == "4":
                new_first = input("Enter new first name: ")
                new_last = input("Enter new last name: ")
                self.update_student_record(new_first, new_last)
            elif choice == "5":
                new_pass = input("Enter new password: ")
                self.change_password(new_pass)
            elif choice == "6":
                self.logout()
                break
            else:
                print("Error - Invalid choice")

# ------------------- Admin Class -------------------
class Admin(User):
    def __init__(self, email, password, role):
        super().__init__(email, password, role)

    # ----------------- Professor Functions -----------------
    def add_professor(self):
        email = input("Enter email: ")
        name = input("Enter name: ")
        rank = input("Enter rank: ")
        course_id = input("Enter course id: ")
        login_found = False
        try:
            with open("database/login.csv", "r") as file:
                login_data = list(csv.DictReader(file))
                fieldnames = login_data[0].keys()
            for row in login_data:
                if row["email"] == email:
                    login_found = True
                    break
            if not login_found:
                new_row = {
                    "email": email,
                    "password": User.encryptPassword("PROFESSOR"),
                    "role": Role.PROFESSOR
                }
                login_data.append(new_row)
                with open("database/login.csv", "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(login_data)

            with open("database/professors.csv", "r") as file:
                prof_data = list(csv.DictReader(file))
                fieldnames = prof_data[0].keys()
            new_prof = {
                "email": email,
                "name": name,
                "rank": rank,
                "courseId": course_id
            }
            prof_data.append(new_prof)
            with open("database/professors.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(prof_data)
            print("Professor added successfully")
        except Exception as e:
            print("Error - Cannot add professor", e)

    def delete_professor(self):
        email = input("Enter email of professor to delete: ")
        try:
            with open("database/professors.csv", "r") as file:
                prof_data = list(csv.DictReader(file))
                fieldnames = prof_data[0].keys()
            prof_data = [row for row in prof_data if row["email"] != email]
            with open("database/professors.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(prof_data)

            with open("database/login.csv", "r") as file:
                login_data = list(csv.DictReader(file))
                fieldnames = login_data[0].keys()
            login_data = [row for row in login_data if row["email"] != email]
            with open("database/login.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(login_data)
            print("Professor deleted successfully")
        except Exception as e:
            print("Error - Cannot delete professor", e)

    # ----------------- Student Functions -----------------
    def add_student(self):
        email = input("Enter student email: ")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        course_id = input("Enter course id for student: ")
        grade = input("Enter grade (e.g., A/B/C): ")
        marks = input("Enter marks (0-100): ")
        login_found = False
        try:
            # login.csv
            with open("database/login.csv", "r") as file:
                login_data = list(csv.DictReader(file))
                fieldnames = login_data[0].keys()
            for row in login_data:
                if row["email"] == email:
                    login_found = True
                    break
            if not login_found:
                login_data.append({
                    "email": email,
                    "password": User.encryptPassword("STUDENT"),
                    "role": Role.STUDENT
                })
                with open("database/login.csv", "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(login_data)

            # students.csv
            with open("database/students.csv", "r") as file:
                student_data = list(csv.DictReader(file))
                fieldnames = student_data[0].keys()
            student_data.append({
                "email": email,
                "firstName": first_name,
                "lastName": last_name,
                "courseId": course_id,
                "grade": grade,
                "marks": marks
            })
            with open("database/students.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(student_data)

            print("Student added successfully!")
        except Exception as e:
            print("Error - Cannot add student", e)

    def delete_student(self):
        email = input("Enter email of student to delete: ")
        try:
            # students.csv
            with open("database/students.csv", "r") as file:
                student_data = list(csv.DictReader(file))
                fieldnames = student_data[0].keys()
            student_data = [row for row in student_data if row["email"] != email]
            with open("database/students.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(student_data)

            # login.csv
            with open("database/login.csv", "r") as file:
                login_data = list(csv.DictReader(file))
                fieldnames = login_data[0].keys()
            login_data = [row for row in login_data if row["email"] != email]
            with open("database/login.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(login_data)

            print("Student deleted successfully!")
        except Exception as e:
            print("Error - Cannot delete student", e)

    # ----------------- Course Functions -----------------
    def add_course(self):
        course_id = input("Enter course ID: ")
        course_name = input("Enter course name: ")
        credits = input("Enter credits: ")
        description = input("Enter description: ")
        try:
            with open("database/courses.csv", "r") as file:
                course_data = list(csv.DictReader(file))
                fieldnames = course_data[0].keys()
            course_data.append({
                "id": course_id,
                "name": course_name,
                "credits": credits,
                "description": description
            })
            with open("database/courses.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(course_data)
            print("Course added successfully!")
        except Exception as e:
            print("Error - Cannot add course", e)

    def delete_course(self):
        course_id = input("Enter course ID to delete: ")
        try:
            with open("database/courses.csv", "r") as file:
                course_data = list(csv.DictReader(file))
                fieldnames = course_data[0].keys()
            course_data = [row for row in course_data if row["id"] != course_id]
            with open("database/courses.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(course_data)
            print("Course deleted successfully!")
        except Exception as e:
            print("Error - Cannot delete course", e)

    # ------------------- Admin Menu -------------------
    def displayMenu(self):
        while True:
            print("\n----- Admin Menu -----")
            print("1. Add Professor")
            print("2. Delete Professor")
            print("3. Add Student")
            print("4. Delete Student")
            print("5. Add Course")
            print("6. Delete Course")
            print("7. Modify Student Grade")
            print("8. Change Password")
            print("9. Logout")
            choice = input("Enter choice: ")
            if choice == "1":
                self.add_professor()
            elif choice == "2":
                self.delete_professor()
            elif choice == "3":
                self.add_student()
            elif choice == "4":
                self.delete_student()
            elif choice == "5":
                self.add_course()
            elif choice == "6":
                self.delete_course()
            elif choice == "7":
                s_email = input("Enter student email: ")
                course_id = input("Enter course ID: ")
                new_grade = input("Enter new grade: ")
                new_marks = int(input("Enter new marks: "))
                self.modify_student_grade(s_email, course_id, new_grade, new_marks)
            elif choice == "8":
                new_pass = input("Enter new password: ")
                self.change_password(new_pass)
            elif choice == "9":
                self.logout()
                break
            else:
                print("Error - Invalid choice")

    def modify_student_grade(self, student_email, course_id, new_grade, new_marks):
        try:
            updated = False
            with open("database/students.csv", "r") as file:
                students = list(csv.DictReader(file))
                fieldnames = students[0].keys()

            for row in students:
                if row["email"] == student_email and row["courseId"] == course_id:
                    row["grade"] = new_grade
                    row["marks"] = str(new_marks)
                    updated = True
                    break

            if not updated:
                print("Error - Student not found")
                return

            with open("database/students.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(students)

            print(f"Student {student_email}'s grade updated successfully for course {course_id}")

        except Exception as e:
            print("Error - Cannot update student grade", e)

    

# ------------------- Main System -------------------
def main():
    while True:
        print("\n=== Welcome to CheckMyGrade ===")
        email = input("Enter email: ")
        password = input("Enter password: ")
        user = User(email, password)
        if not user.login():
            continue
        if user.role == Role.STUDENT:
            student = Student.loadStudent(email, password)
            if student:
                student.displayMenu()
        elif user.role == Role.PROFESSOR:
            professor = Professor.loadProfessor(email, password)
            if professor:
                professor.displayMenu()
        elif user.role == Role.ADMIN:
            admin = Admin(email, password, Role.ADMIN)
            admin.displayMenu()

if __name__ == "__main__":
    main()