# external libraries
import pymongo

# classes
from classes.Department import Department
from Records import Records
from classes.Major import Major
from classes.Course import Course
from classes.Student import Student
from classes.Enrollment import Enrollment
from classes.Section import Section
from classes.StudentMajor import StudentMajor

# other
from utils import get_datetime


def add_menu():
    """Prints a menu for adding to a collection.
    Prompts user for necessary information and adds to
    the collection the user chose.
    :return:    None
    """

    menu = """\nWhat would you like to add?
    1) Department
    2) Major to Department
    3) Course to Department
    4) Section to Course
    5) Student
    6) Student to Major
    7) Student to Course
    8) Return to main menu"""
    inp = 0
    while inp not in [1, 2, 3, 4, 5, 6, 7, 8]:
        print(menu)
        inp = int(input("Choice # --> "))

    if inp == 1:
        add_department()
    elif inp == 2:
        add_major_to_department()
    elif inp == 3:
        add_course_to_department()
    elif inp == 4:
        add_section_to_course()
    elif inp == 5:
        add_student()
    elif inp == 6:
        add_student_to_major()
    elif inp == 7:
        add_enrollment_by_student()


def add_department():
    getting_input = True
    while getting_input:
        print("\nAdding Department:")
        name = input("Enter department name --> ")
        abrv = input("Enter abbreviation --> ")
        chair = input("Enter chair --> ")
        building = input("Enter building --> ")
        office = input("Enter office (must be an integer)--> ")
        while not office.isnumeric():
            office = input("must be an integer --> ")
        office = int(office)
        desc = input("Enter description --> ")

        dept = Department(name, abrv, chair, building, office, desc)

        try:
            dept.add_dept()
            getting_input = False
        except Exception as ex:
            getting_input = True
            print("\n*******************************")
            print("There are errors with the input")
            if type(ex) == pymongo.errors.WriteError:
                print("\tAt least one invalid field")
                print("*******************************")
            elif type(ex) == pymongo.errors.DuplicateKeyError:
                print("\tDepartment would violate at least one uniqueness constraint")
                print("*******************************")
            else:
                print(ex)


def add_major_to_department():
    database = Records()
    department_id = 0

    # get department id using department abbreviation. Make sure department exists
    found = False
    while not found:
        department = input("Department Abbreviation --> ")
        departmentQuery = {"abbreviation": department}
        result = database.departments.find_one(departmentQuery)
        if (result is not None):
            department_id = result['_id']
            found = True
        else:
            print("Could not find department!")

    # add new major to the department
    majorAdded = False
    while not majorAdded:
        name = input("Major Name --> ")
        description = input("Description --> ")
        newMajor = Major(name, description, department_id)

        # Try adding new major. Catch any errors MongoDB may throw
        # need to add major to deparments
        try:
            newMajor.add_major()

            # get mongoDB major we just added
            majorAdded = database.majors.find_one({"name": name})

            # update the departments collection using the mongoDB major ID
            updateDepartments = {'$push': {'majors': majorAdded['_id']}}
            database.departments.update_one(departmentQuery, updateDepartments)

            majorAdded = True
        except Exception as ex:
            majorAdded = False
            print("\n*******************************")
            print("There are errors with the input")
            if type(ex) == pymongo.errors.WriteError:
                print("\tAt least one invalid field")
                print("*******************************")
            elif type(ex) == pymongo.errors.DuplicateKeyError:
                print("\tMajor would violate at least one uniqueness constraint")
                print("*******************************")
            else:
                print(ex)


def add_course_to_department():
    database = Records()

    courseNotAdded = True
    while courseNotAdded:

        # make sure that the department exists
        departmentNotExist = True
        while departmentNotExist:
            departmentAbbreviation = input("Department Abbreviation --> ")
            departmentQuery = {"abbreviation": departmentAbbreviation}
            result = database.departments.find_one(departmentQuery)
            if (result is not None):
                departmentNotExist = False
            else:
                print("Could not find department!")

        # checking if this course already exists in the department
        courseInDepartment = True
        while courseInDepartment:
            courseName = input("Course name --> ")
            courseNumber = int(input("Course number --> "))

            # course is not in department unless one of the course references has the
            # same name
            courseInDepartment = False
            for courseId in result['courses']:
                exisitingCourse = database.courses.find_one({'_id': courseId})
                if exisitingCourse is not None:
                    if exisitingCourse['course_name'] == courseName:
                        courseInDepartment = True
            if courseInDepartment:
                print("The department already offers this course!")

        description = input("Description --> ")
        units = int(input("Units --> "))

        course = Course(departmentAbbreviation, courseNumber, courseName, description, units)
        try:
            # add course to course collection
            course.add_course()

            # add course reference to departments
            # get course ID of the course we just added
            courseAdded = database.courses.find_one({"course_name": courseName})

            # update the departments collection
            updateDepartments = {'$push': {'courses': courseAdded['_id']}}
            database.departments.update_one(departmentQuery, updateDepartments)
            courseNotAdded = False

        except Exception as ex:
            courseNotAdded = True
            print("\n*******************************")
            print("There are errors with the input")
            if type(ex) == pymongo.errors.WriteError:
                print("\tAt least one invalid field")
                print(ex)
                print("*******************************")
            elif type(ex) == pymongo.errors.DuplicateKeyError:
                print("\tCourse would violate at least one uniqueness constraint")
                print("*******************************")
            else:
                print(ex)


def add_enrollment_by_student():
    rec = Records()

    # get student to add
    student = None
    valid_input = False
    while not valid_input:
        firstName = input("Enter first name --> ")
        lastName = input("Enter last name --> ")
        studentQuery = {"first_name": firstName, "last_name": lastName}

        student = rec.students.find_one(studentQuery)
        if student:
            valid_input = True
    student_obj = Student(student["last_name"], student["first_name"], student["email"])

    student_enrollments = student["enrollments"]
    # choose section to add to (and check student doesn't already have enrollment)
    valid_section = False
    course = None
    sectionNum = ""
    grade_type = None
    while not valid_section:
        courseNumber = input("Enter course number --> ")
        sectionNum = input("Enter section number --> ")
        grade_type = input("Enter 1 for Pass/Fail, or 2 for Letter Grade --> ")
        try:
            course = rec.courses.find_one({"course_number": int(courseNumber)})
        except:
            print("Course number must be an interger between 100 and 700")
            pass
        if course:
            valid_section = True
        else:
            print("Invalid section please try again")
        if grade_type not in ["1", "2"]:
            valid_section = False
            print("Invalid grade type")
        else:
            grade_type = int(grade_type)
    field = ""
    match grade_type:
        case 1:
            print("Enter application date: ")
            field = get_datetime()

        case 2:
            field = ""
            field += input("Enter minimum satisfactory grade --> ")
            while field.upper() not in ["A", "B", "C", "D", "F"]:
                print("Invalid grade, valid choices are: A, B, C, D, F")
                field = input("Enter minium satisfactory grade --> ")
    course_obj = Course(course["dept_abrv"], course["course_number"], course["course_name"], course["description"],
                        course["units"])
    enrollment_obj = Enrollment(student_obj, course_obj, int(sectionNum), grade_type, field)
    try:
        enrollment_obj.add_enrollment()
    except Exception as ex:
        print("\n*******************************")
        print("There are errors with the input")
        if type(ex) == pymongo.errors.WriteError:
            print("\tAt least one invalid field")
            print("*******************************")
        elif type(ex) == ValueError:
            print("\tStudent is already enrolled in that course")
            print("*******************************")
        else:
            print(ex)
def add_section_to_course():
    database = Records()
    sectionNotAdded = True
    while sectionNotAdded:

        # make sure that the section exists
        courseNotExist = True
        while courseNotExist:
            departmentAbbreviation = input("Department Abbreviation --> ")
            courseNumber = int(input("Course Number --> "))
            courseQuery = {"course_number": courseNumber,"dept_abrv": departmentAbbreviation}
            result = database.courses.find_one(courseQuery)
            if (result is not None):
                courseNotExist = False
            else:
                print("Could not find course!")


        # removed check, relying on uniqueness constraints
        # if section passes uniqueness constraints, it's a unique
        # section and it cannot already be in a course
        sectionNumber = int(input("Section number --> "))
        semester = input("Semester --> ")
        sectionYear = int(input("Section Year --> "))
        building = input("Building --> ")
        room = int(input("Room --> "))
        schedule = input("Schedule --> ")
        startTime = input("Start Time --> ")
        instructor = input("Instructor --> ")

        section = Section(result['_id'],sectionNumber, semester, sectionYear, building, room, schedule, startTime, instructor)
        try:
            # add section to section collection
            section.add_section()

            # get section ID of the section we just added
            sectionAdded = database.sections.find_one({"section_number":sectionNumber})

            # update the course collection
            updateCourse = {'$push': {'sections': sectionAdded['_id']}}
            database.courses.update_one(courseQuery, updateCourse)
            sectionNotAdded = False

        except Exception as ex:
            sectionNotAdded = True
            print("\n*******************************")
            print("There are errors with the input")
            if type(ex) == pymongo.errors.WriteError:
                print(ex)
                print("*******************************")
            elif type(ex) == pymongo.errors.DuplicateKeyError:
                print("\tSection would violate at least one uniqueness constraint")
                print("*******************************")
            else:
                print(ex)



def add_student():
    studentNotAdded = True
    while studentNotAdded:
        firstName = input("Enter first name --> ")
        lastName = input("Enter last name --> ")
        email = input("Enter email --> ")
        student = Student(lastName, firstName, email)
        try:
            student.add_student()
            studentNotAdded = False
        except Exception as ex:
            print("\n*******************************")
            print("There are errors with the input")
            if type(ex) == pymongo.errors.WriteError:
                print("\tAt least one invalid field")
                print("*******************************")
            elif type(ex) == pymongo.errors.DuplicateKeyError:
                print("\tStudent would violate at least one uniqueness constraint")
                print("*******************************")
            else:
                print(ex)


def add_student_to_major():
    database = Records()
    studentFound = False

    # find student that is going to add major
    while not studentFound:
        firstName = input("Student first name --> ")
        lastName = input("Student last name --> ")

        studentQuery = {"first_name": firstName, "last_name":lastName}

        student = database.students.find_one(studentQuery)
        if student is not None:
            studentFound = True
        else:
            print("Student could not be found!")

    #find major student wants to add
    majorFound = False
    while not majorFound:
        majorName = input("Enter major --> ")
        majorQuery = {"name":majorName}
        major = database.majors.find_one(majorQuery)

        if major is not None:
            majorFound = True
        else:
            print("Could not find major!")

    declarationDate = get_datetime()
    studentMajor = StudentMajor(declarationDate, major['_id'])

    try:
        # add student to students inside given major
        updateMajor = {'$push': {'students': student['_id']}}
        database.majors.update_one(majorQuery, updateMajor)

        #add studentMajor to student_majors inside given student
        updateStudent = {'$push': {'student_majors':studentMajor.dict_repr()}}
        database.students.update_one(studentQuery, updateStudent )
    except Exception as ex:
        print("\n*******************************")
        print("There are errors with the input")
        if type(ex) == pymongo.errors.WriteError:
            print("\tAt least one invalid field\n\tHas the student already declared this major?")
            print("*******************************")
        elif type(ex) == pymongo.errors.DuplicateKeyError:
            print("\tStudent would violate at least one uniqueness constraint")
            print("*******************************")
        else:
            print(ex)

