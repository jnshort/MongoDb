import pymongo
from pymongo import MongoClient
from db import db
import certifi


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
        return cls._instance


    def __init__(self):
        if not Records._initialized:
            self.db_connect = MongoClient(db, tlsCAFile=certifi.where())
            self.departments = self.db_connect.singlecollection.departments
            self.students = self.db_connect.singlecollection.students
            self.majors = self.db_connect.singlecollection.majors
            Records._initialized = True


    def department_list(self):
        return self.departments.find()

    
    def students_list(self):
        return self.students.find()
    

    def majors_list(self):
        return self.majors.find()