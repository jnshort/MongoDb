import pymongo
from pymongo import MongoClient
from db import db
from Records import Records
import datetime

class StudentMajor:

    def __init__(self, declarationDate: datetime.datetime, major: str):
        self.declarationDate: str = declarationDate
        self.major: str = major

    def dict_repr(self) -> dict:
        """Returns a dictionary representation of the class.
        :return:    dict
        """
        studentmajor = {
            "declaration_date": self.declarationDate,
            "major": self.major,
        }
        return studentmajor

    def add_student_major(self):
        """Adds this department to the database and the
        records list of departments.
        :return:    None
        """
        """
        rec = Records()
        rec.students.insert_one(self.dict_repr())
        self.active = True
        """

        #todo add method to add student major to given student

    def __str__(self):
        """Returns a string representation of the department.
        :return:    String
        """
        text = f"Major: {self.major}, Declaration Date: {str(self.declarationDate)}\n"
        return text



