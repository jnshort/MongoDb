import pymongo

department_constraints = [
        [("name", pymongo.ASCENDING)],
        [("abbreviation", pymongo.ASCENDING)],
        [("chair_name", pymongo.ASCENDING)],
        [("building", pymongo.ASCENDING),("office", pymongo.ASCENDING)]
    ]