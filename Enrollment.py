import pymongo
from pymongo import MongoClient
from db import db
from Records import Records
from Student import Student
from Section import Section
from Course import Course

class Enrollment:
    def __init__(self, student: Student, course: Course, sectionNum: Section, type: int, field: str):
        # type 1 = PassFail, type 2 = LetterGrade
        self.student = student
        self.sectionNum = sectionNum
        self.course = course
        if type == 1: # PassFail
            self.type = 1
            self.applicationDate = field
        elif type == 2: # LetterGrade
            self.type = 2
            self.minSatisfactory = field
        
    def dict_repr(self):
        if self.type == 1:
            enroll = {
                "course": self.course,
                "section_number": self.sectionNum,
                "application_data": self.applicationDate
            }
            return enroll
        elif self.type == 2:
            enroll = {
                "course": self.course,
                "section_number": self.sectionNum,
                "min_satisfactory": self.minSatisfactory
            }

    def add_enrollment(self):
        pass

    def remove_enrollment(self):
        pass