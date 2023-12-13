from Records import Records


class Section:
    students = []
    id = ""
    def __init__(self, courseId: str = "", section_number: int = 0, semester: str = "", section_year: str = "", building: str = "", room: int = "", schedule: str = "", start_time: str = "", instructor: str = ""):
        self.courseId = courseId
        self.section_number: int = section_number
        self.semester: str = semester
        self.section_year: str = section_year
        self.building: str = building
        self.room: int = room
        self.schedule: str = schedule
        self.start_time: str = start_time
        self.instructor: str = instructor

    def checkFields(self) -> bool:
        return (
            len(self.room) <= 1000)

    def load_from_db(self, db_file):
        self.id = db_file['_id']
        self.courseId = db_file['course_id']
        self.section_number = db_file['section_number']
        self.semester = db_file['semester']
        self.section_year = db_file['section_year']
        self.building = db_file['building']
        self.room = db_file['room']
        self.schedule = db_file['schedule']
        self.start_time = db_file['start_time']
        self.instructor = db_file['instructor']
        self.students = db_file['students']
    def dict_repr(self) -> dict:
        """Returns a dictionary representation of the class.
        :return:    dict
        """
        section = {
            "course_id":self.courseId,
            "section_number": self.section_number,
            "semester": self.semester,
            "section_year": self.section_year,
            "building": self.building,
            "room": self.room,
            "schedule": self.schedule,
            "start_time": self.start_time,
            "instructor": self.instructor,
            "students": self.get_student_list()
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

        # remove itself from sections list in course
        course_query = {'_id':self.courseId}
        course_update_query = update_department_query = {'$pull': {'sections': self.id}}
        rec.courses.update_one(course_query,course_update_query)

        # delete section
        rec.sections.delete_one({"_id":self.id})


    def get_student_list(self):
        """Returns the list of students in this section from the database.
        If the section is not yet in the database, it will instead return an empty list
        :return:    List of student objectIds
        """
        rec = Records()

        students = []
        query = {'course_id':self.courseId, 'section_number':self.section_number, 'semester':self.semester}
        section = rec.sections.find_one(query)
        students = []
        if section is not None:
            for student in section['students']:
                students.append(student)
        return students
