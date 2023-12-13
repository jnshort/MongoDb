import pymongo
from pymongo import MongoClient
from db import db 
from Records import Records
from classes.Course import Course
from classes.Major import Major

# hello world
class Department:
    def __init__(self, name: str = "", abrv: str = "", chair: str = "", building: str = "", office: int = 0, desc: str = "", courses=[], majors=[]):
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

    def load_from_db(self, db_file):
        self.name: str = db_file['name']
        self.abbreviation: str = db_file['abbreviation']
        self.chair: str = db_file['chair_name']
        self.building: str = db_file['building']
        self.office: int = db_file['office']
        self.desc: str = db_file['description']
        self.courses = db_file['courses']
        self.majors = db_file['majors']

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

        # remove courses in department
        for course in self.courses:
            query = {'_id':course}
            result = rec.courses.find_one(query)
            if result is not None:
                temp_course = Course()
                temp_course.load_from_db(result)
                temp_course.remove_course()

        # remove majors in department
        for major in self.majors:
            query = {'_id':major}
            result = rec.majors.find_one(query)
            if result is not None:
                temp_major = Major()
                temp_major.load_from_db(result)
                temp_major.remove_major()

        # remove self
        rec.departments.delete_one({'abbreviation': self.abbreviation})



    def __str__(self):
        """Returns a string representation of the department.
        :return:    String
        """
        text = f"Name: {self.name}, Abbreviation: {self.abbreviation}\n"
        text += f"\tChair: {self.chair}, Building: {self.building}, Office: {self.office}\n"
        text += f"\tDescription: {self.desc}"
        return text

    def get_id(self):
        rec = Records()
        return rec.departments.find_one({"name":self.name})["_id"]

