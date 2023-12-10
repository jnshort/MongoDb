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

section_constraints = [
    [("course_id", pymongo.ASCENDING),("section_number",pymongo.ASCENDING),("semester",pymongo.ASCENDING),("section_year",pymongo.ASCENDING)],
    [("semester", pymongo.ASCENDING),("section_year",pymongo.ASCENDING),("building",pymongo.ASCENDING),("room",pymongo.ASCENDING),("schedule",pymongo.ASCENDING),("start_time",pymongo.ASCENDING)],
    [("semester",pymongo.ASCENDING),("section_year",pymongo.ASCENDING),("schedule",pymongo.ASCENDING),("start_time",pymongo.ASCENDING),("instructor",pymongo.ASCENDING)],
]