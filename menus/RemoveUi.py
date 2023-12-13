import pymongo
from Records import Records
from classes.Student import Student
from classes.Major import Major
from classes.Course import Course
from classes.Enrollment import Enrollment
from classes.Department import Department
from classes.Section import Section

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
    8) Return to main menu"""
    inp = 0
    while inp not in [1, 2, 3, 4, 5, 6, 7,8]:
        print(menu)
        inp = int(input("Choice # --> "))

    match inp:
        case 1:
           remove_department()
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

def remove_department():
    database = Records()

    departmentNotFound = True
    while departmentNotFound:
        department_name = input("Enter department abbreviation --> ")
        query = {"abbreviation":department_name}
        result = database.departments.find_one(query)
        if result is not None:
            departmentNotFound = False
        else:
            print("Could not find the department!")

    # Check that there are no courses associated with the department
    course_count = len(result['courses'])
    if course_count > 0:
        print("Department still has courses associated with it!")

    # Check that there are no majors associated with the department
    major_count = len(result['majors'])
    if major_count > 0:
        print("Department still has majors associated with it!")

    department = Department()
    department.load_from_db(result)

    # Delete department if safe
    if major_count == 0 and course_count == 0:
        database.departments.delete_one(query)
        print("Department removed!")




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

    # todo something about enrollments
    enrollments = len(student['enrollments'])
    if enrollments > 0:
        print("Student is still enrolled in courses!")

    #todo something about majors
    majors = len(student['student_majors'])
    if majors > 0:
        print("Student still has majors declared!")
    if majors == 0 and enrollments == 0:
        if valid_student:
            student_obj = Student()
            student_obj.load_from_db(student)
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
        departmentQuery = {"abbreviation": deptAbrv}

        department = rec.departments.find_one(departmentQuery)
        if department:
            valid_department = True
        else:
            print("Could not find department!")

    valid_course = False
    course = None
    while not valid_course:
        course_number = input("Enter course number --> ")
        course = rec.courses.find_one({"course_number": course_number})
        if course:
            valid_course = True
        else:
            print("Unable to find course, enter a valid course name")

    if len(course['sections']) > 0:
        print("Course still has sections!")
    else:
        if valid_course:
            course_obj = Course()
            course_obj.load_from_db(course)
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
        departmentQuery = {"abbreviation": deptAbrv}

        department = rec.departments.find_one(departmentQuery)
        if department:
            valid_department = True

    valid_major = False
    major = None
    while not valid_major:
        major_name = input("Enter major name --> ")
        major = rec.majors.find_one({"name": major_name})
        if major:
            valid_major = True
        else:
            print("Unable to find major, enter a valid major name")
    if len(major['students']) > 0:
        print("Major still has students declaired!")
    else:
        if valid_major:
            major_obj = Major()
            major_obj.load_from_db(major)
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
    rec = Records()

    valid_department = False
    while not valid_department:
        deptAbrv = input("Enter department abbreviation --> ")
        departmentQuery = {"abbreviation": deptAbrv}

        department = rec.departments.find_one(departmentQuery)
        if department:
            valid_department = True

    valid_course = False
    course = None
    while not valid_course:
        course_number = input("Enter course number --> ")
        course = rec.courses.find_one({'dept_abrv':deptAbrv,"course_number": course_number})
        if course:
            valid_course = True

    valid_section = False
    section = None
    while not valid_section:
        section_number = int(input("Enter section number --> "))
        section_query = {'course_id':course['_id'], 'section_number':section_number}
        section = rec.sections.find_one(section_query)
        if section is not None:
            valid_section = True
        else:
            print("Could not find section")
    if len(section['students']) > 0:
        print("Section still has students!")
    else:
        if valid_section:
            section_obj = Section()
            section_obj.load_from_db(section)
            try:
                section_obj.remove_section()
            except Exception as ex:
                print("\n*******************************")
                print("There are errors with the input")
                if type(ex) == pymongo.errors.WriteError:
                    print("\tAt least one invalid field")
                    print("*******************************")
                else:
                    print(ex)


def undeclare_student():
    rec = Records()

    valid_student = False
    while not valid_student:
        firstName = input("Enter first name --> ")
        lastName = input("Enter last name --> ")
        studentQuery = {"first_name": firstName, "last_name": lastName}

        student = rec.students.find_one(studentQuery)
        if student:
            valid_student = True

    student_obj = Student()
    student_obj.load_from_db(student)

    majors_list = student_obj.get_majors()

    valid_major = False
    major = None
    while not valid_major:
        major_name = input("Enter major name --> ")
        major = rec.majors.find_one({"name": major_name})
        if major:
            valid_major = True
        else:
            print("Unable to find major, enter a valid major name")

    major_removed = False
    for declared_major in majors_list:
        if declared_major["major"] == major["_id"]:
            majors_list.remove(declared_major)
            major_removed = True
    
    students_in_major = major["students"]
    for student_id in students_in_major:
        if student_id == student_obj.get_id():
            students_in_major.remove(student_id)
            student_removed = True

    if major_removed and student_removed:
        try:
            rec.students.update_one(studentQuery, {"$set": {"student_majors": majors_list}})
            rec.majors.update_one({"name": major_name}, {"$set": {"students": students_in_major}})
        except Exception as ex:
            print("\n*******************************")
            print("There are errors with the input")
            if type(ex) == pymongo.errors.WriteError:
                print("\tAt least one invalid field")
                print("*******************************")
            else:
                print(ex)
    else:
        print("Student does not have that major declared!")
