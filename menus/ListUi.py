from classes.Major import Major
from classes.Student import Student
from Records import Records
from classes.Section import Section
from classes.Course import Course
from utils import load_dept
import pprint

"""
********************************************************************************* 

 Main List Menu

 *********************************************************************************
"""
def list_menu():
    rec = Records()
    menu = """\nWhich collection would you like to list?
    1) Department
    2) Majors
    3) Students
    4) Courses
    5) Enrollments
    6) Return to main menu"""
    inp = 0
    while inp not in ["1", "2", "3", "4", "5", "6"]:
        print(menu)
        inp = input("Choice # --> ")

    if inp == "1":
        print("\n--------------------")
        print("Departments:")
        col = rec.department_list()
        for dept in col:
            print(str(load_dept(dept)))
            print()
        print("--------------------")
    elif inp == "2":
        list_majors_menu()
    elif inp == "3":
        list_students_menu()
    elif inp == "4":
        list_courses_menu()
    elif inp == "5":
        list_enrollments_menu()
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
    while inp not in ["1","2","3","4"]:
        print(menu)
        inp = input('Choice # --> ')
    if inp == "1":
        list_students_in_majors()
    elif inp == "2":
        list_majors_in_departments()
    elif inp == "3":
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
            pp = pprint.PrettyPrinter()
            pp.pprint(printStudent.print_dict())
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
            pp = pprint.PrettyPrinter()
            pp.pprint(printMajor.print_dict())
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
            pp = pprint.PrettyPrinter()
            pp.pprint(printMajor.print_dict())

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
    while inp not in ["1","2"]:
        print(menu)
        inp = input('Choice # --> ')
        if inp == "1":
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
        text = ""
        match enrollment["type"]:
            case "Letter Grade":
                text += f"Minimum Grade: {enrollment['min_satisfactory']}"
            case "Pass Fail":
                text += f"Application Date: {str(enrollment['application_date'])}"
        course = database.courses.find_one({"_id": enrollment['course']})
        print(f"Course: {course['course_name']} \t\tSection #{enrollment['section_number']}")
        print(f"\tGrading Option: {enrollment['type']} \t{text}")
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
    while inp not in ["1", "2", "3", "4"]:
        print(menu)
        inp = input("Choice # --> ")

    if inp == "1":
        list_all_students()
    if inp == "2":
        list_students_in_majors()
    if inp == "3":
        list_students_by_section()

def list_all_students():
    database = Records()
    result = database.students.find({})
    if result is not None:
        for student in result:
            printStudent = Student()
            printStudent.load_from_db(student)
            pp = pprint.PrettyPrinter()
            pp.pprint(printStudent.print_dict())


def list_students_by_section():
    database = Records()
    sectionNotFound = True
    while sectionNotFound:
        course_number = input("Course number --> ")
        while not course_number.isnumeric():
            course_number = input("Course number --> ")
        course = database.courses.find_one({"course_number": int(course_number)})
        section_number = input("Section number --> ")
        while not section_number.isnumeric():
            section_number = input("Section number --> ")
        section = database.sections.find_one({"section_number": int(section_number), "course_id": course["_id"]})
        if section is not None:
            sectionNotFound = False
        else:
            print("Could not find the section!")

    print("\n-----------------------------------------------------")
    print(f"Students enrolled in {course['course_name']}: section #{section_number}")
    for student_id in section["students"]:
        student = database.students.find_one({"_id": student_id})
        if student is not None:
            tempStudent = Student()
            pp = pprint.PrettyPrinter()
            tempStudent.load_from_db(student)
            pp.pprint(tempStudent.print_dict())
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
    while inp not in ["1", "2", "3", "4"]:
        print(menu)
        inp = input("Choice # --> ")

    if inp == "1":
        list_all_courses()
    elif inp == "2":
        list_courses_in_department()
    elif inp == "3":
        list_sections_by_course()
    elif inp == "4":
        pass


def list_all_courses():
    database = Records()
    result = database.courses.find({})
    print("\n-----------------------------------------------------")
    print("Listing all courses: ")
    if result is not None:
        for course in result:
            printCourse = Course()
            printCourse.load_from_db(course)
            pp = pprint.PrettyPrinter()
            pp.pprint(printCourse.print_dict())
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
            test = printCourse.print_dict();
            pp = pprint.PrettyPrinter()
            pp.pprint(test)
            print("\n-----------------------------------------------------")

def list_sections_by_course():
    database = Records()
    courseFound = False

    while not courseFound:
        courseNum = input("Course number --> ")
        while not courseNum.isnumeric():
            courseNum = input("Course number --> ")
        course = database.courses.find_one({"course_number": int(courseNum)})
        if course:
            courseFound = True

    print("\n-----------------------------------------------------")
    print(f"Sections for {course['course_name']}")
    print()
    for section_id in course["sections"]:
        section = database.sections.find_one({"_id": section_id})
        printSection = Section()
        printSection.load_from_db(section)
        pp = pprint.PrettyPrinter()
        pp.pprint(printSection.print_dict())

        print("-----------------------------------------------------")
