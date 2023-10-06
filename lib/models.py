from sqlalchemy.orm import declarative_base,relationship,sessionmaker
from sqlalchemy import String,Integer,Column,ForeignKey,Table,create_engine
import click


Base = declarative_base()
engine = create_engine("sqlite:///grades.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Association Table
student_course = Table(
    'student_courses', #Table name
    Base.metadata,
    Column
    ('student_id',
     Integer,
     ForeignKey('students.id')),
    Column
    ("course_id",
     Integer,
     ForeignKey("courses.id")),
    extend_existing=True,
)

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer(),primary_key=True)
    first_name = Column(String())
    last_name = Column(String())


    courses = relationship("Course",secondary= student_course, back_populates = 'students')
    
    #Defines the one-to-many relationship between Grade and Student
    grades = relationship("Grade",back_populates='student')

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer(),primary_key=True)
    name = Column(String())
    department= Column(String())

    students = relationship("Student",secondary=student_course,back_populates='courses')

    grades = relationship("Grade",back_populates='course')

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer(), primary_key=True)
    grade = Column(Integer())
    student_id = Column(Integer(), ForeignKey("students.id"))

    course_id = Column(Integer(),ForeignKey('courses.id'))

    student = relationship("Student",back_populates="grades")
    course = relationship("Course",back_populates="grades")

# CLI commands
@click.group()
def cli():
    pass

@cli.command()
def list_options():
    click.echo("Available Options:")
    click.echo("1. Add Student")
    click.echo("2. Add Course")
    click.echo("3. Record Grade")
    click.echo("4. Delete Grade")
    click.echo("5. List Options")
    click.echo("6. Exit")

@cli.command()
@click.option('--first-name', prompt='First Name')
@click.option('--last-name', prompt='Last Name')
def add_student(first_name, last_name):
    session = Session()
    student = Student(first_name=first_name, last_name=last_name)
    session.add(student)
    session.commit()
    session.close()
    click.echo(f"Added student: {first_name} {last_name}")

@cli.command()
@click.option('--name', prompt='Course Name')
@click.option('--department',prompt="Enter department")
def add_course(name,department):
    session = Session()
    course = Course(name=name,department=department)
    session.add(course)
    session.commit()
    session.close()
    click.echo(f"Added course: {name} Added department: {department}")

@cli.command()
@click.option('--student-id', type=int, prompt='Student ID')
@click.option('--course-id', type=int, prompt='Course ID')
@click.option('--grade', type=float, prompt='Grade')
def record_grade(student_id, course_id, grade):
    session = Session()
    # Retrieve the student and course objects based on their IDs
    student = session.query(Student).get(student_id)
    course = session.query(Course).get(course_id)
    
    # Check if the student and course exist
    if not student:
        click.echo(f"Error: Student with ID {student_id} does not exist.")
        session.close()
        return
    
    if not course:
        click.echo(f"Error: Course with ID {course_id} does not exist.")
        session.close()
        return
    
    # Create a grade record and associate it with the student and course
    grade_record = Grade(grade=grade, student=student, course=course)
    session.add(grade_record)
    session.commit()
    session.close()
    click.echo(f"Recorded grade: Student ID {student_id}, Course ID {course_id}, Grade {grade}")

@cli.command()
@click.option('--student-id', type=int, prompt='Student ID')
@click.option('--course-id', type=int, prompt='Course ID')
def delete_grade(student_id, course_id):
    session = Session()
    
    # Retrieve the grade record to delete
    grade_record = session.query(Grade).filter_by(student_id=student_id, course_id=course_id).first()
    
    # Check if the grade record exists
    if not grade_record:
        click.echo(f"Error: No grade record found for Student ID {student_id} and Course ID {course_id}.")
        session.close()
        return
    
    # Delete the grade record
    session.delete(grade_record)
    session.commit()
    session.close()
    click.echo(f"Deleted grade record: Student ID {student_id}, Course ID {course_id}")

if __name__ == '__main__':
    cli()






# studentA = Student(first_name='Ruweyda',last_name='Adan')
# studentB = Student(first_name='Amish',last_name='Abdi')
# studentC = Student(first_name='Irfan',last_name='Osman')

# course1 = Course(course_name='Computer Science',department='Science And Technology')
# course2 = Course(course_name='Public Health',department='Veterinary Medicine')
# course3 = Course(course_name='Finance ',department='Business')

# gradeA = Grade(grade='A',student_id='1',course_id='1')
# gradeB = Grade(grade='B',student_id='2',course_id='2')
# gradeC = Grade(grade='F',student_id='3',course_id='3')

# session.bulk_save_objects([studentA,studentB,studentC,course1,course2,course3,gradeA,gradeB,gradeC])

# session.commit()