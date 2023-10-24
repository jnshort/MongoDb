import pymongo
from pymongo import MongoClient
from db import db
from Department import Department


class Records:
    """A singleton class used to keep record of what we have
    added to the database, in addition to storing the connection
    to the database to be accessed from anywhere in the program.
    """
    _instance = None
    _initialized = False

    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls.instance
            

    def __init__(self):
		if not Records._initialized:
			self.db_connect = MongoClient(db)
           	self.departments = [] # im not sure why the indentation on this line is messed up, it shows correctly on my ide but not in github
			Singleton._initialized = True


    def new_dept_rec(self, dept: Department):
        self.departments.append(dept)


    def remove_dept_rec(self, dept: Department):
        self.departments.remove(dept)