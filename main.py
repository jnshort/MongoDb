import pymongo
from pymongo import MongoClient
from Department import Department
from Records import Records


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
        print("Adding Department:")
        name = input("Enter department name --> ")
        abrv = input("Enter abbreviation --> ")
        chair = input("Enter chair --> ")
        building = input("Enter building -->")
        office = input("Enter office (must be an integer)--> ")
        while not office.isnumeric():
            office = input("must be an integer --> ")
        desc = input("Enter description --> ")

        dept = Department(name, abrv, chair, building, office, desc)    
        if dept.constrains():
            dept.add_dept()
            print("Department added")
        else:
            print("Failed to add department")


def remove_menu():
    """Prints a menu for removing from a collectin.
    Prompts the user for necessary information and removes
    from collection of the user's choice.
    :return:    None
    """
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
        for dept in departments:
            if dept.name == name:
                found = True
                to_del = dept
        if found:
            to_del.remove_dept()
            print("Department removed")
        else:
            print("Failed to find department")

            


def list_menu():
    menu ="""Which collection would you like to list?
    1) Department
    2) Return to main menu"""
    inp = 0
    while inp not in [1,2]:
        print(menu)
        inp = int(input("Choice # --> "))
    
    if inp == 1:
        print("Departments:")
        for dept in departments:
            print(str(dept))
            

  


def main_menu():
    menu ="""Manage Database
    1) Add 
    2) Delete
    3) List
    4) Load"""
    
    inp = 0
    while inp not in [1,2, 3]:
        print(menu)
        inp = int(input("Choice # --> "))

    if inp == 1:
        add_menu()

    elif inp == 2:
        remove_menu()

    elif inp == 3:
        list_menu()

    elif inp == 4:
        load_dp()

    elif inp == 5:
        return True

    return False
    

def load_db():
    """Takes existing documents in the database and adds them to 
    the records singleton based on what collection they belong to 
    for tracking and constraint checking.
    """
    # todo 
    # I don't think we need this for this assignment, but probably will for term project
    # and the goal of this was to make this scalable
    pass


def main():
    done = False
    while !done:
        done = main_menu()


    

