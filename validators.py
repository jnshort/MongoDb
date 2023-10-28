department_validator = {
        'validator': {
            '$jsonSchema': {
                'description': 'A department associated with a particular set of majors at a university',
                'required': ['name', 'abbreviation', 'chair_name', 'building', 'office', 'description'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'name': {
                        'bsonType': 'string',
                        'description': 'name of the department',
                        'minLength': 10,
                        'maxLength': 50
                    },
                    'abbreviation': {
                        'bsonType': 'string',
                        'description': 'abbreviated representation of the department',
                        'maxLength': 6
                    },
                    'chair_name': {
                        'bsonType': 'string',
                        'description': 'name of the chair of the department',
                        'maxLength': 80
                    },
                    'building': {
                        'enum': ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC'],
                        'description': 'building containing the department office'
                    },
                    'office': {
                        'bsonType': 'int',
                        'description': 'room number of department office'
                    },
                    'description': {
                        'bsonType': 'string',
                        'minLength': 10,
                        'maxLength': 80
                  },
                }
            }
        }
    }