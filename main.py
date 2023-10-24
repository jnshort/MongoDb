import pymongo
from pymongo import MongoClient
from Department import Department
#from db import db 


<<<<<<< HEAD
print("Hello World!")
print("Hello Branch!")
=======

>>>>>>> 68e36a406770038330873d4bf13f79f4d877ad75



def add_menu():
    """Prints a menu for adding to a collection.
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

    # todo
    pass


def list_menu():

    # todo
    pass

def main_menu():

    # todo
    pass


def main():

    # todo
    pass
