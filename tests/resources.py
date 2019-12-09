from flask_restful.reqparse import RequestParser
from flask_restful_swagger_3 import Resource, swagger
from tests.models import UserModel


class ParseResource(Resource):
    @swagger.doc({
        'tags': ['user'],
        'description': 'Tests query parameter parser',
        'parameters': [
            {
                'name': 'str',
                'description': 'String value',
                'in': 'query',
                'schema': {
                    'type': 'string'
                }
            },
            {
                'name': 'date',
                'description': 'Date value',
                'in': 'query',
                'schema': {
                    'type': 'string',
                    'format': 'date'
                }
            },
            {
                'name': 'datetime',
                'description': 'Date-time value',
                'in': 'query',
                'schema': {
                    'type': 'string',
                    'format': 'date-time'
                }
            },
            {
                'name': 'bool',
                'description': 'Boolean value',
                'in': 'query',
                'schema': {
                    'type': 'boolean'
                }
            },
            {
                'name': 'int',
                'description': 'Integer value',
                'in': 'query',
                'schema': {
                    'type': 'integer'
                }
            },
            {
                'name': 'float',
                'description': 'Float value',
                'in': 'query',
                'schema': {
                    'type': 'number',
                    'format': 'float'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Parsed values'
            }
        }
    })
    def get(self, _parser):
        """
        Returns parsed query parameters.
        :param _parser: Query parameter parser
        """
        args = _parser.parse_args()

        return {
            'str': args.str,
            'date': args.date.isoformat(),
            'datetime': args.datetime.isoformat(),
            'bool': args.bool,
            'int': args.int,
            'float': args.float
        }, 200


class UserResource(Resource):
    @swagger.doc({
        'tags': ['user'],
        'description': 'Returns a user',
        'parameters': [
            {
                'name': 'user_id',
                'description': 'User identifier',
                'in': 'path',
                'schema': {
                    'type': 'integer'
                }
            },
            {
                'name': 'name',
                'description': 'User name',
                'in': 'query',
                'schema': {
                    'type': 'string'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Get users',
                'content': {
                    'application/json': {
                        'schema': UserModel,
                        'examples': {
                            'application/json': {
                                'id': 1,
                                'name': 'somebody'
                            }
                        }
                    }
                }
            }
        }
    })
    def get(self, user_id, _parser):
        """
        Returns a specific user.
        :param user_id: The user identifier
        :param _parser: Query parameter parser
        """
        args = _parser.parse_args()

        name = args.get('name', 'somebody')
        return UserModel(**{'id': user_id, 'name': name}), 200


class EntityAddResource(Resource):
    post_parser = RequestParser()
    post_parser.add_argument('id', type=int, help='id help')
    post_parser.add_argument('name', type=str)
    post_parser.add_argument('value', type=float, default=1.1)
    post_parser.add_argument('private', type=bool, required=True)
    post_parser.add_argument('type', type=str, choices=['common', 'major', 'minor'])

    class PasswordType(str):
        swagger_type = 'password'
    post_parser.add_argument('password_arg', type=PasswordType, required=False)

    @swagger.doc({
        'tags': ['user'],
        'description': 'List of entities',
        'reqparser': {'name': 'EntityAddParser',
                      'parser': post_parser},
        'responses': {
            '200': {
                'description': 'User',
                'content': {
                    'application/json': {
                        'examples': {
                            'application/json': {
                                'id': 1,
                            }
                        }
                    }
                }
            }
        }
    })
    def post(self):
        """
        Returns a specific user.
        """
        args = self.post_parser.parse_args()

        name = args.get('name', 'somebody')
        return UserModel(**{'id': id, 'name': name}), 200
