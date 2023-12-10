import pymongo
from pymongo import MongoClient
from Department import Department
from Student import Student
from Records import Records
from Major import Major
from StudentMajor import StudentMajor
from validators import department_validator
from validators import student_validator
from constraints import department_constraints, student_constraints, major_constraints
from major_validator import major_validator
from course_validator import course_validator

database_name = "singlecollection"
database = Records()

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
    4) Student
    5) Student to Major
    6) Return to main menu"""
    inp = 0
    while inp not in [1,2,3,4,5,6]:
        print(menu)
        inp = int(input("Choice # --> "))
    
    if inp == 1:
        add_department()
    elif inp == 2:
        add_major_to_department()
    elif inpt == 3:
        add_course_to_department()
    elif inp == 4:
        add_student()
    elif inp == 5:
        add_student_to_major()

def add_department():
    getting_input = True
    while getting_input:
        print("\nAdding Department:")
        name = input("Enter department name --> ")
        abrv = input("Enter abbreviation --> ")
        chair = input("Enter chair --> ")
        building = input("Enter building -->")
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
        result = database.departments.find_one({"abbreviation":department})
        if(result is not None):
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
        try:
            newMajor.add_major()
            majorAdded = True
        except Exception as ex:
            majorAdded = False
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

def add_course_to_department():
    pass


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
        majorName = input("Enter major -->")
        majorQuery = {"name":majorName}
        major = database.majors.find_one(majorQuery)

        if major is not None:
            majorFound = True
        else:
            print("Could not find major!")

    declarationDate = input("Declaration Date --> ")
    studentMajor = StudentMajor(declarationDate, major['_id'])

    try:
        #add studentMajor to student_majors inside given student
        updateStudent = {'$push': {'student_majors':studentMajor.dict_repr()}}
        database.students.update_one(studentQuery, updateStudent )

        #add student to students inside given major
        updateMajor = {'$push':{'students':student['_id']}}
        database.majors.update_one(majorQuery, updateMajor)
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


def remove_menu():
    """Prints a menu for removing from a collectin.
    Prompts the user for necessary information and removes
    from collection of the user's choice.
    :return:    None
    """
    rec = Records()
    menu = """\nWhat would you like to remove?
    1) Department
    2) Return to main menu"""
    inp = 0
    while inp not in [1,2]:
        print(menu)
        inp = int(input("Choice # --> "))
    
    
    if inp == 1:
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

            


def list_menu():
    rec = Records()
    menu ="""\nWhich collection would you like to list?
    1) Department
    2) Majors
    3) Return to main menu"""
    inp = 0
    while inp not in [1,2,3]:
        print(menu)
        inp = int(input("Choice # --> "))
    
    if inp == 1:
        print("\n--------------------")
        print("Departments:")
        col = rec.department_list()
        for dept in col:
            print(str(load_dept(dept)))
            print()
        print("--------------------")
    if inp == 2:
        list_majors_menu()
            
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
            #list_students_in_majors()
            pass
        elif inp == 2:
            #todo
            #list_majors_in_departments()
            pass
        elif inp == 3:
            #todo
            list_majors_by_student()

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

def list_students_menu():
    #todo
    pass

def main_menu():
    menu ="""\nManage Database
    1) Add 
    2) Delete
    3) List
    4) Exit"""
    
    inp = 0
    while inp not in [1,2, 3, 4]:
        print(menu)
        inp = input("Choice # --> ")
        if inp.isdigit():
            inp = int(inp)

    if inp == 1:
        add_menu()

    elif inp == 2:
        remove_menu()

    elif inp == 3:
        list_menu()

    elif inp == 4:
        return True

    return False
    

def load_dept(dept: dict) -> Department:
    """Takes a dictionary returned by MongoDb representing a department document
    and creates a Departent object of that document.
    """
    name = dept["name"]
    abrv = dept["abbreviation"]
    chair = dept["chair_name"]
    build = dept["building"]
    off = dept["office"]
    desc = dept["description"]
    return Department(name, abrv, chair, build, off, desc)

1
def startNewDatabase():
    # connect to database
    database = Records()
    database = database.db_connect[database_name]

    #iterate and delete collections
    for collection in database.list_collection_names():
        database.drop_collection(collection)

    # create collections with validator schemas
    database.create_collection("departments", **department_validator)
    database.create_collection("students", **student_validator)
    database.create_collection("majors", **major_validator)
    database.create_collection("courses", **course_validator)

    # apply uniqueness constraints
    for constraint in department_constraints:
        database["departments"].create_index(constraint, unique = True)
    for constraint in student_constraints:
        database["students"].create_index(constraint, unique = True)
    for constraint in major_constraints:
        database["majors"].create_index(constraint, unique=True)
    

def main():
    """Menu to use existing database, or start over """
    validChoice = False
    choiceOptions = [1,2]
    print("=========================================================================================================\n")
    print("""\n
                                         _.--\"\"--._
                                        /  _    _  \\
                                     _  ( (_\  /_) )  _
                                    { \._\   /\   /_./ }
                                    /_\"=-.}______{.-\=\"_\\
                                     _  _.=(\"\"\"\")=._  _
                                    (_\'\"_.-\"`~~`\"-._\"\'_)
                                    {_\"            \"_}
        """)
    print("""
     ___________                    __________                   __               __   
    \\__    ___/__________  _____   \\______   \\_______  ____    |__| ____   _____/  |_ 
      |    |_/ __ \\_  __ \\/     \\   |     ___/\\_  __ \\/  _ \\   |  |/ __ \\_/ ___\\   __\\
      |    |\\  ___/|  | \\/  Y Y  \\  |    |     |  | \\(  <_> )  |  \\  ___/\\  \\___|  |  
      |____| \\___  >__|  |__|_|  /  |____|     |__|   \\____/\\__|  |\\___  >\\___  >__|  
                 \\/            \\/                          \\______|    \\/     \\/      
""")
    print("=================================== CECS 323 - Term Project ======================================\n")
    while not validChoice:
        print("""Would you like to use existing database?
            1.) Use existing database
            2.) Start from scratch\n""")
        
        inp =  input("Choice # --> ")
        if inp.isdigit():
            inp = int(inp)
            validChoice = True
            match inp:
                case 1:
                    pass
                case 2:
                    startNewDatabase() # start over
                case _:
                    validChoice = False
                    print("Invalid input entered, please enter from the following options ", choiceOptions)
        else:
            print("Invalid input entered, please enter from the following options ", choiceOptions)

    # main loop
    done = False
    while not done:
        done = main_menu()
    print("Goodbye")


    
if __name__ == '__main__':
    main()
