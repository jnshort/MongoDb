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
        self.db = MongoClient(db)
        self.active: bool = False


    def checkFields(self) -> bool:
        return (
            len(self.name) <= 50 and 
            len(self.abbreviation) <= 6 and 
            len(self.chair) <= 80 and
            len(self.building) <= 10 and
            len(self.desc) <= 80)

    def constraints(self) -> bool:
        """Checks uniqueness constraints of the Department class 
        and that the departent does not already exist in the database.
        Returns True if it passes.
        :return:    Boolean
        """
        # todo
        
        
        uniqueName = {
            "name":self.name,
        }

        uniqueAbbr = {
            "abbreviation":self.abbreviation
        }

        # No professor can chair > one department.
        unique1 = {
            "chair":self.chair,
        }

        # No two departments can occupy the same room.
        unique2 = {
            "building":self.building,
            "office":self.office
        }

        # No two departments can have the same description.
        unique3 = {
            "description":self.desc
        }

        rec = Records()
        uniqueCount =  rec.departments.count_documents(uniqueName)
        uniqueCount +=  rec.departments.count_documents(uniqueAbbr)
        uniqueCount +=  rec.departments.count_documents(unique1)
        uniqueCount +=  rec.departments.count_documents(unique2)
        uniqueCount +=  rec.departments.count_documents(unique3)
        
        
        return uniqueCount == 0


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
            "description": self.desc
        }
        return dept


    def add_dept(self):
        """Adds this department to the database and the 
        records list of departments.
        :return:    None
        """
        
        rec = Records()
        rec.departments.insert_one(self.dict_repr())
        self.active = True

            


    def remove_dept(self):
        """Removes this department from the database.
        Main has already verified that this dept is in the database.
        :return:    None
        """
        rec = Records()
        self.active = False

        #to_del = rec.db_connect.singlecollection.departments.find()
        rec.departments.delete_one({"name":self.name})




    def __str__(self):
        """Returns a string representation of the department.
        :return:    String
        """
        text = f"Name: {self.name} Abbreviation: {self.abbreviation}\n"
        text += f"\tChair: {self.chair} Building: {self.building} Office: {self.office}\n"
        text += f"\tDescription: {self.desc}"
        return text



