import pymongo
from pymongo import MongoClient
from Department import Department
from Records import Records
from validators import department_validator
from constraints import department_constraints

database_name = "singlecollection"

def add_menu():
    """Prints a menu for adding to a collection.
    Prompts user for necessary information and adds to
    the collection the user chose.
    :return:    None
    """

    menu = """What would you like to add?
    1) Department
    2) Return to main menu"""
    inp = 0
    while inp not in [1,2]:
        print(menu)
        inp = int(input("Choice # --> "))
    
    if inp == 1:
        getting_input = True
        while getting_input:
            print("Adding Department:")
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
                print("There are errors with the input")
                print(ex)



def remove_menu():
    """Prints a menu for removing from a collectin.
    Prompts the user for necessary information and removes
    from collection of the user's choice.
    :return:    None
    """
    rec = Records()
    menu = """What would you like to remove?
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
        for dept in rec.departments:
            if dept.name == name:
                found = True
                to_del = dept
        if found:
            to_del.remove_dept()
            print("Department removed")
        else:
            print("Failed to find department")

            


def list_menu():
    rec = Records()
    menu ="""Which collection would you like to list?
    1) Department
    2) Return to main menu"""
    inp = 0
    while inp not in [1,2]:
        print(menu)
        inp = int(input("Choice # --> "))
    
    if inp == 1:
        print("Departments:")
        for dept in rec.departments:
            print(str(dept))
            

  


def main_menu():
    menu ="""Manage Database
    1) Add 
    2) Delete
    3) List
    4) Exit"""
    
    inp = 0
    while inp not in [1,2, 3, 4]:
        print(menu)
        inp = int(input("Choice # --> "))

    if inp == 1:
        add_menu()

    elif inp == 2:
        remove_menu()

    elif inp == 3:
        list_menu()

    elif inp == 4:
        return True

    return False
    

def load_db():
    """Takes existing documents in the database and adds them to 
    the records singleton based on what collection they belong to 
    for tracking and constraint checking.
    """
    load_dept()


def load_dept():
    """Takes existing departments in the departments collection and
    loads them into our records as Department objects
    """
    rec = Records()
    col = rec.db_connect.singlecollection.departments.find()
    for dept in col:
        name = dept["name"]
        abrv = dept["abbreviation"]
        chair = dept["chair_name"]
        build = dept["building"]
        off = dept["office"]
        desc = dept["description"]

        store = Department(name, abrv, chair, build, off, desc)
        rec.new_dept_rec(store)
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

    # apply uniqueness constraints
    for constraint in department_constraints:
        database["departments"].create_index(constraint, unique = True)
    


def main():

    """Menu to load existing database, or start over """
    validChoice = False
    choiceOptions = [1,2]
    while not validChoice:
        print("""Would you like to load existing database?
            1.) Load existing database
            2.) Start from scratch\n""")
        
        inp =  input("Choice # --> ")
        if inp.isdigit():
            inp = int(inp)
            validChoice = True
            match inp:
                case 1:
                    load_db() # load the database
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
