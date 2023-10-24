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
    _initialized = None

    def __new__(cls, *args):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self, x):
		if not Records._initialized:
			self.db_connect = MongoClient(db)
            self.deparments = []
			Singleton._initialized = True

    def new_dept(self, dept: Department):
        self.departments.append(dept)

    def remove_dept(self, dept: Department):
        self.departmnets.remove(dept)
