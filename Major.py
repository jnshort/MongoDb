import pymongo
from pymongo import MongoClient
from db import db
from Records import Records
from Department import Department
from Student import Student

class Major:

    def __init__(self, name: str, description: str, department: str):
        self.name = name
        self.description = description
        self.department = department


    def dict_repr(self) -> dict:
        major = {
            "name": self.name,
            "description": self.description,
            "department": self.department,
            "students": self.get_students_list()
        }
        return major

    def get_students_list(self):
        rec = Records()
        result = []
        students = rec.students.find({})

        for student in students:
            found = False
            for student_major in student["student_majors"]:
                if student_major.major == self.get_id():
                    found = True
            if found:
                result.append(student["_id"])
        return result
    
    def add_major(self):
        rec = Records()
        rec.majors.insert_one(self.dict_repr())


    def remove_dept(self):
        rec = Records()

        if not self.students: # can only delete majors with no students
            rec.majors.delete_one({"name": self.name})
            return True
        else:
            return False

    def get_id(self):
        pass