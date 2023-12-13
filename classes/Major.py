from Records import Records

class Major:

    def __init__(self, name: str = "", description: str = "", department: str = ""):
        self.name = name
        self.description = description
        self.department = department
        self.department_name = "Not Found!"


    def load_from_db(self, database_file):
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

    def dict_repr(self) -> dict:
        major = {
            "name": self.name,
            "description": self.description,
            "department": self.department,
            "students": self.get_students_list()
        }
        return major

    def get_students_list(self):

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
        rec = Records()
        rec.majors.insert_one(self.dict_repr())


    def remove_major(self):
        rec = Records()
        """
        if not self.students: # can only delete majors with no students
            rec.majors.delete_one({"name": self.name})
            return True
        else:
            return False
        """
        if self.get_students_list() == []:
            rec.majors.delete_one({"name": self.name})
            print(self.department)
            dept = rec.departments.find_one({"_id": self.department})
            for id in dept["majors"]:
                if id == self.get_id():
                    dept["majors"].remove(id)
            rec.departments.update_one({"name": dept["name"]}, {"$set": {"majors": dept["majors"]}})
            return True
        print("Cannot delete a major with students declared")

    def get_id(self):
        rec = Records()
        return rec.majors.find_one({"name":self.name})["_id"]

    def __str__(self):
        text = f"Name: {self.name} Department: {self.department_name} "
        text += f"Description: {self.description}"
        return text
