course_validator = {
        'validator': {
            '$jsonSchema': {
                'description': 'A course associated with a particular department at a university',
                'required': ['course_number', 'course_name', 'description', 'units'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'dept_abrv': {
                        'bsonType': 'string',
                        'description': 'abbreviation of department course is part of',
                    },
                    'course_number': {
                        'bsonType': 'int',
                        'description': 'number of a course',
                        'maximum': 700,
                        'minimum': 100
                    },
                    'course_name': {
                        'bsonType': 'string',
                        'description': 'name of a course',
                    },
                    'description': {
                        'bsonType': 'string',
                        'description': 'description of a course',
                    },
                    'units': {
                        'bsonType': 'int',
                        'description': 'number of units of a course',
                        'maximum': 5,
                        'minimum': 1
                    },
                    'sections': {
                        'bsonType': 'array',
                        'description': 'list of course sections references',
                        'minItems': 0,
                        'uniqueItems': True,
                        'items': {
                            'bsonType': 'objectId',
                            'description': 'reference to a section'
                            }
                        }
                    }
                }
            }
        }       
