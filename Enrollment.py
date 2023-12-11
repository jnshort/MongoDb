import pymongo
from pymongo import MongoClient
from db import db
from Records import Records
from Student import Student
from Section import Section
from Course import Course

class Enrollment:
    def __init__(self, student: Student, course: Course, sectionNum: int, type: int, field: str = ""):
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
                "course": self.course.get_id(),
                "section_number": self.sectionNum,
                "application_data": self.applicationDate
            }
        elif self.type == 2:
            enroll = {
                "course": self.course.get_id(),
                "section_number": self.sectionNum,
                "min_satisfactory": self.minSatisfactory
            }
        return enroll


    def add_enrollment(self):
        rec = Records()
        student = rec.students.find_one({"last_name": self.student.lastName ,"first_name": self.student.firstName})
        if student:
            enrollments = student["enrollments"]
        else:
            raise KeyError("Student not found")

        
        section = rec.sections.find_one({"course_id": self.course.get_id(), "section_number": self.sectionNum})
        

        if section:
            enrollments.append(self.dict_repr())
            print(enrollments)
            filter = {"last_name": self.student.lastName ,"first_name": self.student.firstName}
            rec.students.update_one(filter, {"$set": {"enrollments": enrollments}})
            return True
        else: #throw error myself since I have to do constrainsts of embedded docs clientside
            raise KeyError("Section not found")



    def remove_enrollment(self):
        rec = Records()
        
        student = rec.students.find_one({"last_name": self.student.lastName ,"first_name": self.student.firstName})
        enrollments = student["enrollments"]

        enrollment_found = False
        for enroll in enrollments:
            if enroll["course"] == self.course.get_id():
                enrollments.remove(enroll)
                enrollment_found = True
        
        if enrollment_found:
            filter = {"last_name": self.student.lastName ,"first_name": self.student.firstName}
            rec.students.update_one(filter, {"$set": {"enrollments": enrollments}})
            return True
        else:
            return False
        
    