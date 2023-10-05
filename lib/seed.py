from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Student,Grade,Course
import random

fake = Faker()

if __name__ == "__main__":
    engine = create_engine("sqlite:///grades.db")
    Session = sessionmaker(bind=engine)
    session = Session()

     # Clear existing data
    session.query(Student).delete()
    session.query(Grade).delete()
    session.query(Course).delete()

    course_departments = ["Agriculture","Arts and Social Sciences",
                   "Built Environment and Design","Business and Management Sciences",
                   "Education","Engineering","Law","Health Sciences",
                   "Science and Technology","Veterinary Medicine"]
    course_names = ["Finance","Civil Engineering","Mechanical Engineering",
                    "Statistics","Quantity Surveying","Applied Mathematics",
                    "Economics","Nursing","Supply Chain Management",
                    "Law","Information Technology","Data Analytics",
                    "Cyber Security"]
    
    courses = []
    for i in range(10):
         course = Course(
            department = random.choice(course_departments),
            name = random.choice(course_names)
        )
         session.add(course)
         session.commit()

         courses.append(course)
   
           
    students = []
    for i in range(25):
        student = Student(
            first_name = fake.first_name(),
            last_name = fake.last_name()
        )
        session.add(student)
        session.commit()

        students.append(student)

    grades= []
    for course in courses:
        for i in range(random.randint(1,5)):
              student = random.choice(students)
              if course not in student.courses:
                  student.courses.append(course)
                  session.add(student)
                  session.commit()
              grade = Grade(
                 grade = random.randint(0,100),
                 student_id = student.id,
                 course_id =course.id
              )
              grade.student = student
              grade.course = course
              grades.append(grade)
    session.bulk_save_objects(grades)
    session.commit()

    
    
