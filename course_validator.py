course_validator = {
        'validator': {
            '$jsonSchema': {
                'description': 'A course associated with a particular department at a university',
                'required': ['course_number, course_name, description, units'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'course_number': {
                        'bsonType': 'int',
                        'description': 'number of a course',
                        'maxLength': 700,
                        'minLength': 100
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
                        'maxLength': 5,
                        'minLength': 1
                    },
                    'sections': {
                        'bsonType': 'array',
                        'description': 'list of course sections',
                        'items': {
                            'oneOf': [
                                {
                                    'bsonType': 'object',
                                    'properties': {
                                        'section_number': {
                                            'bsonType': 'int',
                                            'description': 'number of a section'
                                        },
                                        'semester': {
                                            'bsonType': 'string',
                                            'description': 'semester when section is offered',
                                            'enum': ['Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter']
                                        },
                                        'section_year': {
                                            'bsonType': 'int',
                                            'description': 'year section is offered'
                                        },
                                        'building': {
                                            'bsonType': 'string',
                                            'description': 'building of a course section'
                                        },
                                        'room': {
                                            'bsonType': 'int',
                                            'description': 'room of a course section',
                                            'maxLength': 1000,
                                            'minLength': 0
                                        },
                                        'schedule': {
                                            'bsonType': 'string',
                                            'description': 'days section is offered',
                                            'enum': ['MW', 'TuTh', 'MWF', 'F', 'S']
                                        },
                                        'start_time': {
                                            'bsonType': 'string',
                                            'description': 'time the section starts',
                                        },
                                        'instructor': {
                                            'bsonType': 'string',
                                            'description': 'person who teaches the section'
                                        }
                                      }
                                    }
                            ]
                        }
                    }
                  },
                }
            }
        }
