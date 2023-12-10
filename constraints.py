import pymongo

department_constraints = [
        [("name", pymongo.ASCENDING)],
        [("abbreviation", pymongo.ASCENDING)],
        [("chair_name", pymongo.ASCENDING)],
        [("building", pymongo.ASCENDING),("office", pymongo.ASCENDING)]
    ]

student_constraints = [
    [("email", pymongo.ASCENDING)],
    [("last_name", pymongo.ASCENDING),("first_name", pymongo.ASCENDING)]
]

major_constraints = [
    [("name", pymongo.ASCENDING)]
]

course_constraints =[
    [("dept_abrv", pymongo.ASCENDING), ("course_number", pymongo.ASCENDING)],
    [("dept_abrv", pymongo.ASCENDING), ("course_name", pymongo.ASCENDING)]
]