validator = {
        'validator': {
            '$jsonSchema': {
                'description': 'A major associated with a particular department at a university',
                'required': ['name', 'description', 'department'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'name': {
                        'bsonType': 'string',
                        'description': 'name of major',
                        'minLength': 3,
                        'maxLength': 50
                    },
                    'description': {
                        'bsonType': 'string',
                        'description': 'description of major'
                    },
                    'department': {
                        'bsonType': 'ObjectId',
                        'description': 'reference to a department'
                    },
                    'students': {
                        'bsonType': 'array',
                        'description': 'list of student references'
                        'minItems': 0,
                        'items': {
                            'bsonType': 'ObjectId',
                            'description': 'reference to a student'
                        }
                    }
                }
            }
        }
    }


