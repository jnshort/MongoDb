from Records import Records



# hello world
class Student:
    
    def __init__(self, lastName: str = "", firstName: str = "", email: str = ""):
        self.lastName: str = lastName
        self.firstName: str = firstName
        self.email: str = email
        self.active: bool = False

    def load_from_db(self, database_file):
        self.lastName = database_file['last_name']
        self.firstName = database_file['first_name']
        self.email = database_file['email']
        self.student_majors = database_file['student_majors']
        self.enrollments = database_file['enrollments']
        self.studentId = database_file['_id']


    def dict_repr(self) -> dict:
        """Returns a dictionary representation of the class.
        :return:    dict
        """
        student = {
            "last_name": self.lastName,
            "first_name": self.firstName,
            "email": self.email,
            "student_majors": self.get_majors(),
            "enrollments": self.get_enrollments()
        }
        return student

    def print_dict(self) -> dict:
        student = {
            "last_name": self.lastName,
            "first_name": self.firstName,
            "email": self.email,
        }
        return student

    def add_student(self):
        """Adds this department to the database and the
        records list of departments.
        :return:    None
        """

        rec = Records()
        rec.students.insert_one(self.dict_repr())

    def get_majors(self) -> list:
        """Returns a list of majors the student has declared
        :return:    list
        """
        rec = Records()

        student = rec.students.find_one({"first_name": self.firstName, "last_name": self.lastName})

        if not student:
            return []
        else:
            majors = student["student_majors"]
            return majors
        

    def get_enrollments(self):
        """Returns a list of enrollments the student is enrolled in
        :return:    list
        """
        rec = Records()

        student = rec.students.find_one({"first_name": self.firstName, "last_name": self.lastName})

        if not student:
            return []
        else:
            enrolls = student["enrollments"]
            return enrolls

    def remove_student(self):
        """"Removes this department from the database.
        Main has already verified that this dept is in the database.
        :return:    None
        """
        rec = Records()
        self.active = False

        # to_del = rec.db_connect.singlecollection.departments.find()
        rec.students.delete_one({"first_name": self.firstName, 'last_name':self.lastName})

    def __str__(self):
        """Returns a string representation of the department.
        :return:    String
        """
        text = f"First Name: {self.firstName}, Last Name: {self.lastName}\n"
        text += f"\temail: {self.email}, ID: {self.studentId}"
        return text


    def get_id(self):
        """Returns the id stored in the database of this student
        :return:    objectId
        """
        rec = Records()
        return rec.students.find_one({"first_name":self.firstName, "last_name": self.lastName})["_id"]
