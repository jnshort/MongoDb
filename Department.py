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


    def dict_repr(self):
        dict = {
            "name": self.name,
            "abbreviation": self.abbreviation,
            "chair": self.chair,
            "building": self.building,
            "office": self.office,
            "description": self.description
        }
        return dict


    def add_dept(self):
        # todo
        pass


    def remove_dept(self):
        # todo
        pass


    def list_dept(self):
        # todo
        pass


    def __str__(self):
        text = f"Name: {self.name} Abbreviation: {self.abbreviation}\n"
        text += f"Chair: {self.chair} Building: {self.building} Office: {self.office}\n"
        text += f"Description: {self.description}"
        return text



