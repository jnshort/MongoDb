from Records import Records
from classes.Student import Student

from classes.Course import Course

# force a commit
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
                "type": "Pass Fail",
                "course": self.course.get_id(),
                "section_number": self.sectionNum,
                "application_date": self.applicationDate
            }
        elif self.type == 2:
            enroll = {
                "type": "Letter Grade",
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
            student_ids = section["students"]
            student_ids.append(student["_id"])
            enrollments.append(self.dict_repr())
            filter1 = {"last_name": self.student.lastName ,"first_name": self.student.firstName}
            filter2 = {"course_id": self.course.get_id(), "section_number": self.sectionNum}
            rec.students.update_one(filter1, {"$set": {"enrollments": enrollments}})
            rec.sections.update_one(filter2, {'$set': {"students": student_ids}})

            return True
        else: #throw error myself since I have to do constrainsts of embedded docs clientside
            return False



    def remove_enrollment(self):
        rec = Records()
        
        student = rec.students.find_one({"last_name": self.student.lastName ,"first_name": self.student.firstName})
        enrollments = student["enrollments"]

        section = rec.sections.find_one({"course_id": self.course.get_id(), "section_number": self.sectionNum})
        student_ids = section["students"]
        
        enrollment_found = False
        for enroll in enrollments:
            if enroll["course"] == self.course.get_id():
                enrollments.remove(enroll)
                enrollment_found = True
        
        for student_id in student_ids:
            if student_id == student["_id"]:
                student_ids.remove(student_id)

        if enrollment_found:
            filter1 = {"last_name": self.student.lastName ,"first_name": self.student.firstName}
            filter2 = {"course_id": self.course.get_id(), "section_number": self.sectionNum}
            rec.students.update_one(filter1, {"$set": {"enrollments": enrollments}})
            rec.sections.update_one(filter2, {'$set': {"students": student_ids}})
            return True
        else:
            raise KeyError("Enrollment does not exist")
