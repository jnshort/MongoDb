import pymongo
from Records import Records
from classes.Student import Student
from classes.Major import Major
from classes.Course import Course
from classes.Enrollment import Enrollment

from utils import load_dept
def remove_menu():
    """Prints a menu for removing from a collectin.
    Prompts the user for necessary information and removes
    from collection of the user's choice.
    :return:    None
    """
    rec = Records()
    menu = """\nWhat would you like to remove?
    1) Department
    2) Major
    3) Student
    4) Course
    5) Section
    6) Enrollment
    7) Undeclare Student from Major
    5) Return to main menu"""
    inp = 0
    while inp not in [1, 2, 3, 4, 5, 6, 7]:
        print(menu)
        inp = int(input("Choice # --> "))

    match inp:
        case 1:
            name = input("Enter department name --> ")
            found = False
            to_del = None
            col = rec.department_list()
            for dept in col:
                if dept['name'] == name:
                    found = True
                    to_del = load_dept(dept)
            if found:
                to_del.remove_dept()
                print("Department removed")
            else:
                print("Failed to find department")
        case 2:
            remove_major()
        case 3:
            remove_student()
        case 4:
            remove_course()
        case 5:
            remove_section()
        case 6:
            remove_enrollment_by_student()
        case 7:
            undeclare_student()


def remove_enrollment_by_student():
    rec = Records()

    student = None
    valid_student = False
    while not valid_student:
        firstName = input("Enter first name --> ")
        lastName = input("Enter last name --> ")
        studentQuery = {"first_name": firstName, "last_name": lastName}

        student = rec.students.find_one(studentQuery)
        if student:
            valid_student = True

    valid_course = False
    course = None
    while not valid_course:
        course_number = input("Enter course number --> ")
        try:
            course = rec.courses.find_one({"course_number": int(course_number)})
        except:
            print("Course nummber must be an interger between 100 and 700")
            pass
        if course:
            valid_course = True
        else:
            print("Unable to find course, enter a valid course number")

    if not student["enrollments"]:
        print("Student does not have any enrollments to remove")
        return False

    enrollment_found = False
    enroll_to_rem = None
    type = 0
    for enroll in student["enrollments"]:
        if enroll["course"] == course["_id"]:
            enroll_to_rem = enroll
            enrollment_found = True
            match enroll["type"]:
                case "Pass Fail":
                    type += 1
                case "Letter Grade":
                    type += 2

    if enrollment_found and (type in [1, 2]):
        student_obj = Student(student["last_name"], student["first_name"], student["email"])
        course_obj = Course(course["dept_abrv"], course["course_number"], course["course_name"], course["description"],
                            course["units"])
        enroll_obj = Enrollment(student_obj, course_obj, enroll_to_rem["section_number"], type)
        try:
            enroll_obj.remove_enrollment()
        except Exception as ex:
            print("\n*******************************")
            print("There are errors with the input")
            if type(ex) == pymongo.errors.WriteError:
                print("\tAt least one invalid field")
                print("*******************************")
            else:
                print(ex)
    else:
        print("\n*******************************")
        print("There are errors with the input")
        print("\tUnable to find enrollment")
        print("*******************************")


def remove_student():
    database = Records()
    valid_student = False

    firstName = input("Enter first name --> ")
    lastName = input("Enter last name --> ")
    studentQuery = {"first_name": firstName, "last_name": lastName}

    student = database.students.find_one(studentQuery)
    if student:
        valid_student = True

    if valid_student:
        student_obj = Student(student["first_name"], student["last_name"], student["email"])
        try:
            student_obj.remove_student()
        except Exception as ex:
            print("\n*******************************")
            print("There are errors with the input")
            if type(ex) == pymongo.errors.WriteError:
                print("\tAt least one invalid field")
                print("*******************************")
            else:
                print(ex)


def remove_course():
    rec = Records()

    valid_department = False
    while not valid_department:
        deptAbrv = input("Enter department abbreviation --> ")
        departmentQuery = {"department_abbreviation": deptAbrv}

        department = rec.departments.find_one(departmentQuery)
        if department:
            valid_student = True

    valid_course = False
    course = None
    while not valid_course:
        course_name = input("Enter course name --> ")
        course = rec.courses.find_one({"course_name": course_name})
        if course:
            valid_course = True
        else:
            print("Unable to find course, enter a valid course name")

    if valid_course:
        course_obj = Course(course["dept_abrv"], course["course_number"], course["course_name"], course["description"],
                            course["units"])
        try:
            course_obj.remove_course()
        except Exception as ex:
            print("\n*******************************")
            print("There are errors with the input")
            if type(ex) == pymongo.errors.WriteError:
                print("\tAt least one invalid field")
                print("*******************************")
            else:
                print(ex)


def remove_major():
    rec = Records()

    valid_department = False
    while not valid_department:
        deptAbrv = input("Enter department abbreviation --> ")
        departmentQuery = {"department_abbreviation": deptAbrv}

        department = rec.departments.find_one(departmentQuery)
        if department:
            valid_major = True

    valid_major = False
    major = None
    while not valid_major:
        major_name = input("Enter major name --> ")
        major = rec.majors.find_one({"major_name": major_name})
        if major:
            valid_major = True
        else:
            print("Unable to find major, enter a valid major name")

    if valid_major:
        major_obj = Major(major["major_name"], major["description"], major["department"], major["description"])
        try:
            major_obj.remove_major()
        except Exception as ex:
            print("\n*******************************")
            print("There are errors with the input")
            if type(ex) == pymongo.errors.WriteError:
                print("\tAt least one invalid field")
                print("*******************************")
            else:
                print(ex)


def remove_section():
    pass


def undeclare_student():
    pass
