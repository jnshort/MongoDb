from Major import Major
from Student import Student
from Records import Records
from Course import Course

"""
********************************************************************************* 

 List Majors Section
 
 *********************************************************************************
"""
def list_majors_menu():
    menu = """\nWhat kind of Major list?
        1) Students in Major
        2) Majors in Departments
        3) Majors a Student has declared'
        4) Return to main menu
        """
    inp = 0
    while inp not in [1,2,3]:
        print(menu)
        inp = int(input('Choice # --> '))
        if inp == 1:
            list_students_in_majors()
        elif inp == 2:
            list_majors_in_departments()
        elif inp == 3:
            list_majors_by_student()

def list_students_in_majors():
    database = Records()
    majorName = input("Major name -->")

    # description and department don't matter for this case
    description = ""
    department = ""

    print("\n-----------------------------------------------------")
    print("Students majoring in ", majorName, ": ")
    testMajor = Major(majorName, description, department)
    for student in testMajor.dict_repr()['students']:
        query = {'_id':student}
        result = database.students.find_one(query)
        if result is not None:
            printStudent = Student()
            printStudent.load_from_db(result)
            print(printStudent)
    print("-----------------------------------------------------")

def list_majors_in_departments():
    database = Records()
    departmentNotFound = True
    while departmentNotFound:
        departmentAbbreviation = input("Department Abbreviation --> ")
        departmentQuery = {'abbreviation':departmentAbbreviation}
        result = database.departments.find_one(departmentQuery)

        if result is not None:
            departmentNotFound = False
        else:
            print("Could not find the department!")
    print("\n-----------------------------------------------------")
    print("Majors offered by ", result['name'], "department: ")
    for major in result['majors']:
        majorQuery = {'_id':major}
        majorResult = database.majors.find_one(majorQuery)
        if majorResult is not None:
            printMajor = Major()
            printMajor.load_from_db(majorResult)
            print(printMajor)
    print("-----------------------------------------------------")

def list_majors_by_student():
    database = Records()

    studentNotFound = True
    while studentNotFound:
        firstName = input("First name --> ")
        lastName = input("Last name --> ")

        studentQuery = {"first_name":firstName, "last_name":lastName}
        result = database.students.find_one(studentQuery)
        if result is not None:
            studentNotFound = False
        else:
            print("Could not find the student!")

    print("\n-----------------------------------------------------")
    print("Majors declared by ", firstName, " ", lastName)
    for major in result['student_majors']:
        majorName = database.majors.find_one({"_id":major['major']})
        if majorName is not None:
            printMajor = Major()
            printMajor.load_from_db(majorName)
            print(printMajor)

    print("-----------------------------------------------------")

"""
********************************************************************************* 

 List Enrollments
 
 *********************************************************************************
"""
def list_enrollments_menu():
    menu = """\nWhat kind of Enrollment list?
        1) Enrollments by Student
        2) Return to main menu
        """
    inp = 0
    while inp not in [1]:
        print(menu)
        inp = int(input('Choice # --> '))
        if inp == 1:
            list_enrollments_by_student()




def list_enrollments_by_student():
    database = Records()
    studentNotFound = True

    while studentNotFound:
        firstName = input("First name --> ")
        lastName = input("Last name --> ")

        studentQuery = {"first_name":firstName, "last_name":lastName}
        student = database.students.find_one(studentQuery)
        if student is not None:
            studentNotFound = False
        else:
            print("Could not find the student!")

    print("\n-----------------------------------------------------")
    print(f"Listing {firstName} {lastName}'s enrollments")

    for enrollment in student["enrollments"]:
        course = database.courses.find_one({"_id": enrollment["course"]})
        print(f"Course: {course['course_name']} Section #{enrollment['section_number']}")
    print("-----------------------------------------------------")


"""
********************************************************************************* 

 List Students Section

 *********************************************************************************
"""
def list_students_menu():
    menu = """\nWhich student collection would you like to list?
        1) All Students
        2) All Students in Major
        3) All Students in Section
        4) Return to main menu"""

    inp = 0
    while inp not in [1, 2, 3, 4]:
        print(menu)
        inp = int(input("Choice # --> "))

    if inp == 1:
        list_all_students()
    if inp == 2:
        list_students_in_majors()
    if inp == 3:
        list_students_by_section()

def list_all_students():
    database = Records()
    result = database.students.find({})
    if result is not None:
        for student in result:
            printStudent = Student()
            printStudent.load_from_db(student)
            print(printStudent)


def list_students_by_section():
    database = Records()
    sectionNotFound = True
    while sectionNotFound:
        course_number = input("Course number --> ")
        course = database.courses.find_one({"course_number":course_number})
        section_number = input("Section number --> ")
        section = database.sections.find_one({"_id":section_number, "course_id": course["_id"]})
        if section is not None:
            sectionNotFound = False
        else:
            print("Could not find the section!")

    print("\n-----------------------------------------------------")
    print(f"Students enrolled in {course['course_name']}: section #{section_number}")
    for student_id in section["students"]:
        student = database.students.find_one({"_id": student_id})
        text = f"{student['first_name']} {student['last_name']}\n"
        print(text)
    print("-----------------------------------------------------")

"""
********************************************************************************* 

 List Course Section

 *********************************************************************************
"""
def list_courses_menu():
    menu = """\nWhich student collection would you like to list?
        1) All Courses
        2) All Courses in Department
        3) All Sections in a Course
        4) Return to Main Menu
        """

    inp = 0
    while inp not in [1, 2, 3, 4]:
        print(menu)
        inp = int(input("Choice # --> "))

    if inp == 1:
        list_all_courses()
    if inp == 2:
        list_courses_in_department()
    if inp == 3:
        list_sections_by_course()

def list_all_courses():
    database = Records()
    result = database.courses.find({})
    print("\n-----------------------------------------------------")
    print("Listing all courses: ")
    if result is not None:
        for course in result:
            printCourse = Course()
            printCourse.load_from_db(course)
            print(printCourse)
            print("-----------------------------------------------------")

def list_courses_in_department():
    database = Records()
    departmentNotFound = True

    while departmentNotFound:
        abbreviation = input("Department Abbreviation --> ")
        query = {'abbreviation': abbreviation}
        department = database.departments.find_one(query)
        if department is not None:
            departmentNotFound = False
        else:
            print("Could not find department!")

    print("\n-----------------------------------------------------")
    print("Listing all courses in: ", department['name'])
    for course in department['courses']:
        courseQuery = {'_id':course}
        courseFound = database.courses.find_one(courseQuery)
        if courseFound is not None:
            printCourse = Course()
            printCourse.load_from_db(courseFound)
            print(printCourse)
            print("\n-----------------------------------------------------")

def list_sections_by_course():
    database = Records()
    courseNotFound = True
    while courseNotFound:
        course_number = input("Course Number")
        course = database.courses.find_one({"course_number": course_number})
        if course:
            courseNotFoud = False
        else:
            print("Could not find the course!")
    print("\n-----------------------------------------------------")
    print(f"Sections for {course['course_name']}")
    for section_id in course["sections"]:
        section = database.sections.find_one({"_id": section_id})
        print(f"Section {section['section_number']} {section['semester']} {section['section_year']}")
        print(f"{section['building']} room {section['room']}")
        print(f"Meets on {section['schedule']} at {section['start_time']}")
        print(f"Instructor: {section['instructor']}")
