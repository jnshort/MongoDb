import pymongo
from pymongo import MongoClient
from db import db 

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
        """Adds this department to the database.
        :return:    None
        """
        # todo
        pass


    def remove_dept(self):
        """Removes this department from the database.
        :return:    None"""
        # todo
        pass


    def list_dept(self):
        """Lists the departments that are in the database.
        :return:    String"""
        # todo
        pass


    def __str__(self):
        text = f"Name: {self.name} Abbreviation: {self.abbreviation}\n"
        text += f"\tChair: {self.chair} Building: {self.building} Office: {self.office}\n"
        text += f"\tDescription: {self.description}"
        return text



