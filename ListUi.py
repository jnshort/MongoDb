from Major import Major
from Student import Student
from Records import Records

"""
********************************************************************************* 

 List Majors Section
 
 *********************************************************************************
"""
def list_majors_menu():
    menu = """\nWhat kind of Major list?
        1) Students in Major
        2) Majors in Departments
        3) Majors a Student has declared
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
            print(majorResult['name'])
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
        print(majorName['name'])

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
    while inp not in [1, 2, 3,4]:
        print(menu)
        inp = int(input("Choice # --> "))

    if inp == 1:
        list_all_students()
    if inp == 2:
        list_students_in_majors()
    if inp == 3:
        #todo list all students in section
        pass

def list_all_students():
    database = Records()
    result = database.students.find({})
    if result is not None:
        for student in result:
            printStudent = Student()
            printStudent.load_from_db(student)
            print(printStudent)


"""
********************************************************************************* 

 List Course Section

 *********************************************************************************
"""
def list_courses_menu():
    menu = """\nWhich student collection would you like to list?
        1) All Courses
        2) All Courses in Department
        3) Return to Main Menu
        """

    inp = 0
    while inp not in [1, 2, 3]:
        print(menu)
        inp = int(input("Choice # --> "))

    if inp == 1:
        list_all_courses()
    if inp == 2:
        list_courses_in_department()

def list_all_courses():
    database = Records()
    result = database.courses.find({})
    if result is not None:
        for course in result:
            print(course['course_name'], " ", course['course_number'], "Units: ", course['units'])
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

    for course in department['courses']:
        courseQuery = {'_id':course}
        courseFound = database.courses.find_one(courseQuery)
        if courseFound is not None:
            print(courseFound['course_name'], " ", courseFound['course_number'], "Units: ", courseFound['units'])