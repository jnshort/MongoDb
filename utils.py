import datetime
from classes.Department import Department


def get_datetime()->datetime.datetime:
    """Promts user for year month and day, and returns a datetime object
    representing the date
    :return:    datetime"""
    current_date = datetime.datetime.now()
    valid = False
    year = ""
    month = ""
    day = ""
    while not valid:
        year = input("Enter year (YYYY) --> ")
        if year.isnumeric() and (int(year) <= current_date.year):
            valid = True
    valid = False
    while not valid:
        month = input("Enter month (MM) --> ")
        if month.isnumeric() and (int(month) in range(1, 13)):
            valid = True
    valid = False
    while not valid:
        day = input("Enter year (DD) --> ")
        if month.isnumeric() and (int(day) in range (1, 32)):
            valid = True

    return datetime.datetime(int(year), int(month), int(day))

def load_dept(dept: dict) -> Department:
    """Takes a dictionary returned by MongoDb representing a department document
    and creates a Departent object of that document.
    :return:    Department
    """
    name = dept["name"]
    abrv = dept["abbreviation"]
    chair = dept["chair_name"]
    build = dept["building"]
    off = dept["office"]
    desc = dept["description"]
    return Department(name, abrv, chair, build, off, desc)