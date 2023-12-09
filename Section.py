import pymongo
from pymongo import MongoClient
from db import db
from Records import Records

class Section:

    def __init__(self, section_number: int, semester: str, section_year: str, building: str, room: int, schedule: str, start_time: str, instructor: str):
        self.section_number: int = section_number
        self.semester: str = semester
        self.section_year: str = section_year
        self.building: str = building
        self.room: int = room
        self.schedule: str = schedule
        self.start_time: str = start_time
        self.instructor: str = instructor
        self.db = MongoClient(db)
        self.active: bool = False

    def checkFields(self) -> bool:
        return (
            len(self.room) <= 1000)

    def dict_repr(self) -> dict:
        """Returns a dictionary representation of the class.
        :return:    dict
        """
        section = {
            "section_number": self.section_number,
            "semester": self.semester,
            "section_year": self.section_year,
            "building": self.building,
            "room": self.room,
            "schedule": self.schedule,
            "start_time": self.start_time,
            "instructor": self.instructor
        }
        return section

    def add_section(self):
        """Adds this section to the database and the
        records list of sections.
        :return:    None
        """

        rec = Records()
        rec.sections.insert_one(self.dict_repr())
        self.active = True

    def remove_section(self):
        """Removes this section from the database.
        Main has already verified that this section is in the database.
        :return:    None
        """
        rec = Records()
        self.active = False
        
        rec.sections.delete_one({"section_number":self.section_number})
