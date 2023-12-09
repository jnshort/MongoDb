import pymongo
from pymongo import MongoClient
from db import db
from Records import Records

class Course:

    def __init__(self, course_number: int, course_name: str, description: str, units: int):
        self.course_number: int = course_number
        self.course_name: str = course_name
        self.description: str = description
        self.units: int = units
        self.db = MongoClient(db)
        self.active: bool = False

    def checkFields(self) -> bool:
        return (
            len(self.course_number) <= 700 and
            len(self.units) <= 5)

    def dict_repr(self) -> dict:
        """Returns a dictionary representation of the class.
        :return:    dict
        """
        course = {
            "course_number": self.course_number,
            "course_name": self.course_name,
            "description": self.description,
            "units": self.units,
        }
        return course

    def add_course(self):
        """Adds this course to the database and the
        records list of courses.
        :return:    None
        """

        rec = Records()
        rec.courses.insert_one(self.dict_repr())
        self.active = True

    def remove_course(self):
        """Removes this course from the database.
        Main has already verified that this course is in the database.
        :return:    None
        """
        rec = Records()
        self.active = False

        #to_del = rec.db_connect.singlecollection.departments.find()
        rec.courses.delete_one({"course_name":self.course_name})