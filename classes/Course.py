import pymongo
from pymongo import MongoClient
from db import db
from Records import Records
from classes.Section import Section

class Course:
    sections = []
    id = ""
    def __init__(self, dept_abrv: str = "", course_number: int = 0, course_name: str = "", description: str = "", units: int = 0):
        self.dept_abrv: str = dept_abrv
        self.course_number: int = course_number
        self.course_name: str = course_name
        self.description: str = description
        self.units: int = units

    def checkFields(self) -> bool:
        return (
            len(self.course_number) <= 700 and
            len(self.units) <= 5)

    def load_from_db(self, database_file):
        self.id = database_file['_id']
        self.dept_abrv = database_file['dept_abrv']
        self.course_number = database_file['course_number']
        self.course_name = database_file['course_name']
        self.description = database_file['description']
        self.units = database_file['units']
        self.sections = database_file['sections']

    def dict_repr(self) -> dict:
        """Returns a dictionary representation of the class.
        :return:    dict
        """
        course = {
            "dept_abrv": self.dept_abrv,
            "course_number": self.course_number,
            "course_name": self.course_name,
            "description": self.description,
            "units": self.units,
            "sections":self.get_sections_list()
        }
        return course

    def print_dict(self) -> dict:
        """Returns a dictionary representation of the class.
                :return:    dict
                """
        course = {
            "dept_abrv": self.dept_abrv,
            "course_number": self.course_number,
            "course_name": self.course_name,
            "description": self.description,
            "units": self.units,
        }
        return course
    def get_sections_list(self):
        result = []
        for section in self.sections:
            result.append(section.dict_repr())
        return result
        
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
        database = Records()

        # reach up to Department to remove itself from course list
        department_query = {'abbreviation':self.dept_abrv}
        result = database.departments.find_one(department_query)
        if result is not None:
            update_department_query = {'$pull': {'courses': self.id}}
            database.departments.update_one(department_query,update_department_query)

        for section in self.sections:
            section_query = {'_id':section}
            result = database.sections.find_one(section_query)
            if result is not None:
                temp_section = Section()
                temp_section.load_from_db(result)
                temp_section.remove_section()

        database.courses.delete_one({"_id":self.id})



    def get_id(self):
        rec = Records()
        return rec.courses.find_one({"course_name":self.course_name})["_id"]

    def __str__(self):
        text = f"\nCourse: {self.course_name} \nNumber: {self.course_number} \nDepartment: {self.dept_abrv}"
        text += f"\nDescription: {self.description}"
        text += f"\nUnits: {self.units}"
        return text