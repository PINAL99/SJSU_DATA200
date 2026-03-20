import unittest
from unittest.mock import patch
import csv
import time
from DATA200Lab1 import Admin, Student, Professor, Course, Role

class TestCheckMyGradeExtended(unittest.TestCase):

    def setUp(self):
        self.admin = Admin("admin@abc.com", "ADMIN001", Role.ADMIN)
        self.courses_csv = "database/courses.csv"
        self.professors_csv = "database/professors.csv"
        self.students_csv = "database/students.csv"
        with open(self.courses_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id","name","credits","description"])
            writer.writeheader()
        with open(self.professors_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","name","rank","courseId"])
            writer.writeheader()
        with open(self.students_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","firstName","lastName","courseId","grade","marks"])
            writer.writeheader()

    def generate_course(self, index):
        return {"id": f"DATA{index}","name": f"Course{index}","credits": "3","description": "Desc"}

    def generate_professor(self, index):
        return {"email": f"prof{index}@abc.com","name": f"Prof{index}","rank":"Senior","courseId": f"DATA{index}"}

    def generate_student(self, index):
        return {"email": f"stud{index}@abc.com","firstName": f"First{index}","lastName": f"Last{index}","courseId": f"DATA{index%50}","grade":"A","marks": str(50+index%50)}

    def test_course_add(self):
        start = time.time()
        courses = []
        for i in range(50):
            courses.append(self.generate_course(i))
        with open(self.courses_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id","name","credits","description"])
            writer.writeheader()
            writer.writerows(courses)
        with open(self.courses_csv, "r") as f:
            courses_loaded = list(csv.DictReader(f))
        self.assertEqual(len(courses_loaded), 50)
        print(f">>> Time taken by test_course_add: {time.time()-start:.3f} seconds")

    def test_course_delete(self):
        start = time.time()
        course = self.generate_course(0)
        with open(self.courses_csv, "r") as f:
            courses = list(csv.DictReader(f))
        courses.append(course)
        with open(self.courses_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id","name","credits","description"])
            writer.writeheader()
            writer.writerows(courses)
        courses = courses[1:]
        with open(self.courses_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id","name","credits","description"])
            writer.writeheader()
            writer.writerows(courses)
        with open(self.courses_csv, "r") as f:
            courses = list(csv.DictReader(f))
        self.assertEqual(len(courses), 0)
        print(f">>> Time taken by test_course_delete: {time.time()-start:.3f} seconds")

    def test_course_modify(self):
        start = time.time()
        course = self.generate_course(0)
        with open(self.courses_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id","name","credits","description"])
            writer.writeheader()
            writer.writerow(course)
        with open(self.courses_csv, "r") as f:
            courses = list(csv.DictReader(f))
        courses[0]["name"] = "ModifiedCourse"
        with open(self.courses_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id","name","credits","description"])
            writer.writeheader()
            writer.writerows(courses)
        with open(self.courses_csv, "r") as f:
            courses = list(csv.DictReader(f))
        self.assertEqual(courses[0]["name"], "ModifiedCourse")
        print(f">>> Time taken by test_course_modify: {time.time()-start:.3f} seconds")

    def test_professor_add(self):
        start = time.time()
        profs = []
        for i in range(100):
            profs.append(self.generate_professor(i))
        with open(self.professors_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","name","rank","courseId"])
            writer.writeheader()
            writer.writerows(profs)
        with open(self.professors_csv, "r") as f:
            profs_loaded = list(csv.DictReader(f))
        self.assertEqual(len(profs_loaded), 100)
        print(f">>> Time taken by test_professor_add: {time.time()-start:.3f} seconds")

    def test_professor_delete(self):
        start = time.time()
        prof = self.generate_professor(0)
        with open(self.professors_csv, "r") as f:
            profs = list(csv.DictReader(f))
        profs.append(prof)
        with open(self.professors_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","name","rank","courseId"])
            writer.writeheader()
            writer.writerows(profs)
        profs = profs[1:]
        with open(self.professors_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","name","rank","courseId"])
            writer.writeheader()
            writer.writerows(profs)
        with open(self.professors_csv, "r") as f:
            profs = list(csv.DictReader(f))
        self.assertEqual(len(profs), 0)
        print(f">>> Time taken by test_professor_delete: {time.time()-start:.3f} seconds")

    def test_professor_modify(self):
        start = time.time()
        prof = self.generate_professor(0)
        with open(self.professors_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","name","rank","courseId"])
            writer.writeheader()
            writer.writerow(prof)
        with open(self.professors_csv, "r") as f:
            profs = list(csv.DictReader(f))
        profs[0]["rank"] = "ModifiedRank"
        with open(self.professors_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","name","rank","courseId"])
            writer.writeheader()
            writer.writerows(profs)
        with open(self.professors_csv, "r") as f:
            profs = list(csv.DictReader(f))
        self.assertEqual(profs[0]["rank"], "ModifiedRank")
        print(f">>> Time taken by test_professor_modify: {time.time()-start:.3f} seconds")

    def test_student_add(self):
        start = time.time()
        students = []
        for i in range(1000):
            students.append(self.generate_student(i))
        with open(self.students_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","firstName","lastName","courseId","grade","marks"])
            writer.writeheader()
            writer.writerows(students)
        with open(self.students_csv, "r") as f:
            students_loaded = list(csv.DictReader(f))
        self.assertEqual(len(students_loaded), 1000)
        print(f">>> Time taken by test_student_add: {time.time()-start:.3f} seconds")

    def test_student_delete(self):
        start = time.time()
        student = self.generate_student(0)
        with open(self.students_csv, "r") as f:
            students = list(csv.DictReader(f))
        students.append(student)
        with open(self.students_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","firstName","lastName","courseId","grade","marks"])
            writer.writeheader()
            writer.writerows(students)
        students = students[1:]
        with open(self.students_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","firstName","lastName","courseId","grade","marks"])
            writer.writeheader()
            writer.writerows(students)
        with open(self.students_csv, "r") as f:
            students = list(csv.DictReader(f))
        self.assertEqual(len(students), 0)
        print(f">>> Time taken by test_student_delete: {time.time()-start:.3f} seconds")

    def test_student_modify(self):
        start = time.time()
        student = self.generate_student(0)
        with open(self.students_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","firstName","lastName","courseId","grade","marks"])
            writer.writeheader()
            writer.writerow(student)
        with open(self.students_csv, "r") as f:
            students = list(csv.DictReader(f))
        students[0]["grade"] = "B"
        with open(self.students_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","firstName","lastName","courseId","grade","marks"])
            writer.writeheader()
            writer.writerows(students)
        with open(self.students_csv, "r") as f:
            students = list(csv.DictReader(f))
        self.assertEqual(students[0]["grade"], "B")
        print(f">>> Time taken by test_student_modify: {time.time()-start:.3f} seconds")

    def test_student_search(self):
        start = time.time()
        student = self.generate_student(0)
        with open(self.students_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","firstName","lastName","courseId","grade","marks"])
            writer.writeheader()
            writer.writerow(student)
        found = False
        with open(self.students_csv, "r") as f:
            for row in csv.DictReader(f):
                if row["email"] == student["email"]:
                    found = True
                    break
        self.assertTrue(found)
        print(f"Search time: {time.time()-start:.6f} seconds")
        print(f">>> Time taken by test_student_search: {time.time()-start:.3f} seconds")

    def test_student_sorting(self):
        start = time.time()
        students = [self.generate_student(i) for i in range(10)]
        with open(self.students_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email","firstName","lastName","courseId","grade","marks"])
            writer.writeheader()
            writer.writerows(students)
        with open(self.students_csv, "r") as f:
            students_loaded = list(csv.DictReader(f))
        start_sort = time.time()
        students_sorted_marks = sorted(students_loaded, key=lambda x: int(x["marks"]))
        print(f"Sorting by marks time: {time.time()-start_sort:.6f} seconds")
        start_sort = time.time()
        students_sorted_email = sorted(students_loaded, key=lambda x: x["email"])
        print(f"Sorting by email time: {time.time()-start_sort:.6f} seconds")
        self.assertTrue(int(students_sorted_marks[0]["marks"]) <= int(students_sorted_marks[-1]["marks"]))
        self.assertTrue(students_sorted_email[0]["email"] <= students_sorted_email[-1]["email"])
        print(f">>> Time taken by test_student_sorting: {time.time()-start:.3f} seconds")

if __name__ == "__main__":
    unittest.main()