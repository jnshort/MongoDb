
from classes.Records import Records
from validators.validators import department_validator, student_validator
from validators.major_validator import major_validator
from validators.course_validator import course_validator
from validators.section_validator import section_validator
from constraints import department_constraints, student_constraints, major_constraints, course_constraints, section_constraints
from menus import ListUi, AddUi, RemoveUi


database_name = "singlecollection"
database = Records()

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
        AddUi.add_menu()

    elif inp == 2:
        RemoveUi.remove_menu()

    elif inp == 3:
        ListUi.list_menu()

    elif inp == 4:
        return True

    return False

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
    database.create_collection("sections", **section_validator)

    # apply uniqueness constraints
    for constraint in department_constraints:
        database["departments"].create_index(constraint, unique = True)
    for constraint in student_constraints:
        database["students"].create_index(constraint, unique = True)
    for constraint in major_constraints:
        database["majors"].create_index(constraint, unique=True)
    for constraint in course_constraints:
        database["courses"].create_index(constraint, unique=True)
    for constraint in section_constraints:
        database["sections"].create_index(constraint, unique=True)

    

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
