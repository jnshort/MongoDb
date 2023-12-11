section_validator = {
        'validator': {
            '$jsonSchema': {
                'description': 'A course associated with a particular department at a university',
                'required': ['course_id','section_number', 'semester', 'section_year', 'building'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'course_id':{
                        'bsonType': 'objectId',
                        'description': 'Course that the section is part of'
                    },
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
                    },
                    'students': {
                        'bsonType': 'array',
                        'description': 'a list of student objectId',
                        'minItems': 0,
                        'uniqueItems': True,
                        'items': {
                            'bsonType': 'objectId',
                            'description': 'reference to a student'
                        }
                    }
                },
            }
        }
}