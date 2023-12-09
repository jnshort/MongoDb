import pymongo
from pymongo import MongoClient
from db import db
from Records import Records
from StudentMajor import StudentMajor


# hello world
class Student:
    self.studentMajors =[]
    def __init__(self, lastName: str, firstName: str, email: str):
        self.lastName: str = lastName
        self.firstName: str = firstName
        self.email: str = email
        self.db = MongoClient(db)
        self.active: bool = False



    def dict_repr(self) -> dict:
        """Returns a dictionary representation of the class.
        :return:    dict
        """
        student = {
            "last_name": self.lastName,
            "first_name": self.firstName,
            "email": self.email,
        }
        return student

    def add_student(self):
        """Adds this department to the database and the
        records list of departments.
        :return:    None
        """

        rec = Records()
        rec.students.insert_one(self.dict_repr())
        self.active = True

    """
    def remove_dept(self):
        """""""Removes this department from the database.
        Main has already verified that this dept is in the database.
        :return:    None
        """"""
        rec = Records()
        self.active = False

        # to_del = rec.db_connect.singlecollection.departments.find()
        rec.departments.delete_one({"name": self.name})
"""
    def __str__(self):
        """Returns a string representation of the department.
        :return:    String
        """
        text = f"First Name: {self.firstName}, Last Name: {self.lastName}\n"
        text += f"\temail: {self.email}"
        return text



