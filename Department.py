import pymongo
from pymongo import MongoClient
from db import db 
from Records import Records

# hello world
class Department:
    def __init__(self, name: str, abrv: str, chair: str, building: str, office: int, desc: str, courses=[], majors=[]):
        self.name: str = name
        self.abbreviation: str = abrv
        self.chair: str = chair
        self.building: str = building
        self.office: int = office
        self.desc: str = desc
        self.courses = courses
        self.majors = majors


    def dict_repr(self) -> dict:
        """Returns a dictionary representation of the class.
        :return:    dict
        """
        dept = {
            "name": self.name,
            "abbreviation": self.abbreviation,
            "chair_name": self.chair,
            "building": self.building,
            "office": self.office,
            "description": self.desc,
            "courses": self.courses,
            "majors": self.majors
        }
        return dept


    def add_dept(self):
        """Adds this department to the database and the 
        records list of departments.
        :return:    None
        """
        
        rec = Records()
        rec.departments.insert_one(self.dict_repr())

            


    def remove_dept(self):
        """Removes this department from the database.
        Main has already verified that this dept is in the database.
        :return:    None
        """
        rec = Records()
        rec.departments.delete_one({"name":self.name})


    def __str__(self):
        """Returns a string representation of the department.
        :return:    String
        """
        text = f"Name: {self.name}, Abbreviation: {self.abbreviation}\n"
        text += f"\tChair: {self.chair}, Building: {self.building}, Office: {self.office}\n"
        text += f"\tDescription: {self.desc}"
        return text



