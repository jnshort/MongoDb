import pymongo
from pymongo import MongoClient
from db import db 
from Records import Records

class Department:

    def __init__(self, name: str, abrv: str, chair: str, building: str, office: int, desc: str):
        self.name: str = name
        self.abbreviation: str = abrv
        self.chair: str = chair
        self.building: str = building
        self.office: int = office
        self.desc: str = desc
        self.db_connection = db
        self.active: bool = False



    def constraints(self) -> bool:
        """Checks uniqueness constraints of the Department class 
        and that the departent does not already exist in the database.
        Returns True if it passes.
        :return:    Boolean
        """
        # todo
        pass


    def dict_repr(self) -> dict:
        """Returns a dictionary representation of the class.
        :return:    dict
        """
        dept = {
            "name": self.name,
            "abbreviation": self.abbreviation,
            "chair": self.chair,
            "building": self.building,
            "office": self.office,
            "description": self.description
        }
        return dept


    def add_dept(self):
        """Adds this department to the database and the 
        records list of departments.
        :return:    None
        """
        
        if self.constraints():
            rec = Records()
            rec.new_dept(self)
            self.active = True

            # todo
            pass
        


    def remove_dept(self):
        """Removes this department from the database.
        Main has already verified that this dept is in the database.
        :return:    None
        """
        rec = Records()
        rec.remove_dept(self)
        self.active = False

        # todo
        pass




    def __str__(self):
        """Returns a string representation of the department.
        :return:    String
        """
        text = f"Name: {self.name} Abbreviation: {self.abbreviation}\n"
        text += f"\tChair: {self.chair} Building: {self.building} Office: {self.office}\n"
        text += f"\tDescription: {self.description}"
        return text



