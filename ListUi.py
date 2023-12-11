from Major import Major
from Records import Records

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
            # todo
            list_students_in_majors()
            pass
        elif inp == 2:
            #todo
            list_majors_in_departments()
            pass
        elif inp == 3:
            #todo
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
            print(result['first_name'], " ", result['last_name'])
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
