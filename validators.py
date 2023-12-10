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
                    'courses': {
                        'bsonType': 'array',
                        'description': 'list of  courses offered by department',
                        'minItems': 0,
                        'uniqueItems': True,
                        'items': {
                            'bsonType': 'objectId',
                            'description': 'reference to a course',
                        },
                    },
                    'majors': {
                        'bsonType': 'array',
                        'description': 'list of majors offered by department',
                        'minItems': 0,
                        'uniqueItems': True,
                        'items': {
                            'bsonType': 'objectId',
                            'description': 'reference to a major',
                        },
                    },

                    
                }
            }
        }
    }

student_validator = {
        'validator': {
            '$jsonSchema': {
                'description': 'A person who is registered with the university and may enroll in courses',
                'required': ['last_name', 'first_name', 'email'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'last_name': {
                        'bsonType': 'string',
                        'description': 'last name of student',
                        'minLength': 0,
                        'maxLength': 50
                    },
                    'first_name': {
                        'bsonType': 'string',
                        'description': 'last name of student',
                        'minLength':0,
                        'maxLength': 50
                    },
                    'email': {
                        'bsonType': 'string',
                        'description': 'email address of a given student',
                        'maxLength': 80
                    },
                    'student_majors' : {
                        'bsonType':'array',
                        'description':'List of majors declared by student',
                        'minItems': 0,
                        'uniqueItems': True,
                        'items': {
                            'bsonType':'object',
                            'description': 'a major declared by the student',
                            'required':['declaration_date','major'],
                            'additionalProperties':False,
                            'properties': {
                                'declaration_date': {
                                    'bsonType':'string',
                                    'description':'date that a student delcared the given major',
                                },
                                'major': {
                                    'bsonType':'objectId',
                                    'description':'a reference to a major'
                                },
                            }
                        }
                    },
                    'enrollments': {
                            'bsonType': 'array',
                            'description': 'list of student enrollemnts',
                            'items':{
                                'oneOf':[
                                    {
                                        'bsonType': 'object',
                                        'properties': {
                                            'application_date':{
                                                'bsonType':'string'
                                            },
                                            'course': {
                                                'bsonType': 'objectId',
                                            },
                                            'section_number': {
                                                'bsonType': 'int'
                                            }
                                        }
                                    },
                                    {
                                        'bsonType': 'object',
                                        'properties': {
                                            'letter_grade': {
                                                'bsonType':'string'
                                            },
                                            'course': {
                                                'bsonType': 'objectId',
                                            },
                                            'section_number': {
                                                'bsonType': 'int'
                                            }
                                        }
                                    }
                                ]
                            }
                    },
                }
            }
        }
    }

