from Records import Records

class Major:
    id = ""
    def __init__(self, name: str = "", description: str = "", department: str = ""):
        self.name = name
        self.description = description
        self.department = department
        self.department_name = "Not Found!"


    def load_from_db(self, database_file):
        """Takes document from database and fills in attributes of Major object
        to match
        :return:    None
        """
        database = Records()
        departmentQuery = {'_id':database_file['department']}
        department = database.departments.find_one(departmentQuery)
        if department is not None:
            self.department_name = department['name']
        else:
            self.department_name = "Not Found!"
        database.departments.find_one()
        self.name = database_file['name']
        self.description = database_file['description']
        self.students = database_file['students']
        self.department = database_file['department']
        self.id = database_file['_id']

    def dict_repr(self) -> dict:
        """Returns a dictionary representation of this Major with all attributes
        :return:    dict
        """
        major = {
            "name": self.name,
            "description": self.description,
            "department": self.department,
            "students": self.get_students_list()
        }
        return major

    def print_dict(self) -> dict:
        """Returns an abbreviated dictionary representation of this Major 
        for display purposes.
        :return:    dict
        """

        major = {
            "name": self.name,
            "description": self.description,
        }
        return major
    

    def get_students_list(self) -> list:
        """Returns a list of students who are declared to this major
        :return:    list
        """

        rec = Records()
        """
        result = []
        students = rec.students.find({})

        for student in students:
            found = False
            for student_major in student["student_majors"]:
                if student_major.major == self.get_id():
                    found = True
            if found:
                result.append(student["_id"])
        return result
        """
        result = rec.majors.find_one({"name":self.name})
        students = []
        if result is not None:
            for student in result['students']:
                students.append(student)
        return students
    
    def add_major(self):
        """Adds a Major to the database with attributes matching those of this object
        :return:    None
        """
        rec = Records()
        rec.majors.insert_one(self.dict_repr())


    def remove_major(self):
        """Removes a Major from the database with attributes matching those
        of this object
        :return:    None"""
        rec = Records()
        """
        if not self.students: # can only delete majors with no students
            rec.majors.delete_one({"name": self.name})
            return True
        else:
            return False
        """

        # update departments
        department_query = {'_id':self.department}
        update_department_query = {'$pull': {'majors': self.id}}
        rec.departments.update_one(department_query,update_department_query)

        # delete self
        rec.majors.delete_one({'_id':self.id})


    def get_id(self):
        """Returns the id stored in the database of this Major
        :return:    objectId
        """
        rec = Records()
        return rec.majors.find_one({"name":self.name})["_id"]

    def __str__(self):
        """Returns a string representation of this Major for listing
        :return:    String
        """
        text = f"Name: {self.name} Department: {self.department_name} "
        text += f"Description: {self.description}"
        return text
