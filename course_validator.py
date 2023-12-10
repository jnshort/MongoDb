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
                        'description': 'list of course sections',
                        'items': {
                            'oneOf': [
                                {
                                    'bsonType': 'object',
                                    'properties': {
                                        '_id': {},
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
                                            'maximum': 1000,
                                            'minimum': 0
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
