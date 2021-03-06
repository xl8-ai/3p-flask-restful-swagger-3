# flask-restful-swagger-3


## What is flask-restful-swagger-3?

flask-restful-swagger-3 is a wrapper for [flask-restful](http://flask-restful.readthedocs.org/en/latest/) which
enables [swagger3](http://swagger.io/) support according to the [openapi 3.0.0 specification](https://swagger.io/specification/).

This project is based on [flask-restful-swagger-2](https://github.com/soerface/flask-restful-swagger-2.0), but it only
supported swagger 2.0.

## Getting started

Install:

```
pip install flask-restful-swagger-3
```

To use it, change your import from `from flask_restful import Api` to `from flask_restful_swagger_3 import Api`.

```python
from flask import Flask
# Instead of using this: from flask_restful import Api
# Use this:
from flask_restful_swagger_3 import Api

app = Flask(__name__)

# Use the swagger Api class as you would use the flask restful class.
# It supports several (optional) parameters, these are the defaults:
api = Api(app, version='0.0', api_spec_url='/api/swagger')
```

The Api class supports the following parameters:

| Parameter | Description |
| --------- | ----------- |
| `add_api_spec_resource` | Set to `True` to add an endpoint to serve the swagger specification (defaults to `True`). |
| `version` | The API version string (defaults to '0.0'). Maps to the `version` field of the [info object](http://swagger.io/specification/#infoObject). |
| `api_spec_base` | Instead of specifying individual swagger fields, you can pass in a minimal [OpenAPI Object](http://swagger.io/specification/#openapiObject) to use as a template. Note that parameters specified explicity will overwrite the values in this template. |
| `api_spec_url` | The URL path that serves the swagger specification document (defaults to `/api/swagger`). The path is appended with `.json` and `.html` (i.e. `/api/swagger.json` and `/api/swagger.html`). |
| `servers` | The server on which the API is served, it replaces `schemes`, `host` and `base_path` [server object](http://swagger.io/specification/#serverObject). |
| `schemas`| The Schema Object allows the definition of input and output data types. Maps to the [`schema`](http://swagger.io/specification/#schemaObject) |
| `content` | A list of MIME types the API can consume. Maps to the [`contents`](http://swagger.io/specification/#contentObject) field of the [components](http://swagger.io/specification/#componentObject). |
| `contact` | The contact information for the API. Maps to the `contact` field of the [info object](http://swagger.io/specification/#infoObject). |
| `description` | A short description of the application. Maps to the `description` field of the [info object](http://swagger.io/specification/#infoObject). |
| `external_docs` | Additional external documentation. Maps to the `externalDocs` field of the [operation object](http://swagger.io/specification/#operationObject). |
| `license` | The license information for the API. Maps to the `license` field of the [info object](http://swagger.io/specification/#infoObject). |
| `parameters` | The parameters that can be used across operations. Maps to the `parameters` field of the [operation object](http://swagger.io/specification/#operationObject). |
| `responses` | The responses that can be used across operations. Maps to the `responses` field of the [operation object](http://swagger.io/specification/#operationObject). |
| `security` | A declaration of which security mechanisms can be used across the API. The list of values includes alternative security requirement objects that can be used. Only one of the security requirement objects need to be satisfied to authorize a request. Individual operations can override this definition. Maps to the `security` field of the [OpenAPI Object](http://swagger.io/specification/#openapiObject). |
| `securitySchemes` | The security schemes for the API. Maps to the `securitySchemes` field of the [component object](http://swagger.io/specification/#componentsObject). |
| `tags` | A list of tags used by the specification with additional metadata. Maps to the `tags` field fo the [OpenAPI Object](http://swagger.io/specification/#openapiObject). |
| `terms` | The terms of service for the API. Maps to the `termsOfService` field of the [info object](http://swagger.io/specification/#infoObject). |
| `title` | The title of the application (defaults to the flask app module name). Maps to the `title` field of the [info object](http://swagger.io/specification/#infoObject). |

## Documenting API endpoints

Decorate your API endpoints with `@swagger.doc`. It takes a dictionary in the format of an [operation object](http://swagger.io/specification/#operationObject).

```python
class UserItemResource(Resource):
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
            }
        ],
        'responses': {
            '200': {
                'description': 'User',
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
    def get(self, user_id):
        # Do some processing
        return UserModel(id=1, name='somebody'}), 200  # generates json response {"id": 1, "name": "somebody"}

```

Use add_resource as usual.

```python
api.add_resource(UserItemResource, '/api/users/<int:user_id>')
```

## Parsing query parameters

If a resource function contains the special argument `_parser`, any `query` type parameters in the
documentation will be automatically added to a reqparse parser and assigned to the `_parser` argument.

## Using models

Create a model by inheriting from `flask_restful_swagger_3.Schema`

```python
from flask_restful_swagger_2 import Schema


class EmailModel(Schema):
    type = 'string'
    format = 'email'


class KeysModel(Schema):
    type = 'object'
    properties = {
        'name': {
            'type': 'string'
        }
    }


class UserModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64',
        },
        'name': {
            'type': 'string'
        },
        'mail': EmailModel,
        'keys': KeysModel.array()
    }
    required = ['name']
```

You can build your models according to the [swagger schema object specification](http://swagger.io/specification/#schemaObject)

It is recommended that you always return a model in your views so that your code and documentation are in sync.

## RequestParser support

You can specify RequestParser object if you want to pass its arguments to spec. In such case, there is not need to define model manually

```python
from flask_restful.reqparse import RequestParser

from flask_restful_swagger_2 import swagger, Resource


class GroupResource(Resource):
    post_parser = RequestParser()
    post_parser.add_argument('name', type=str, required=True)
    post_parser.add_argument('id', type=int, help='Id of new group')
    @swagger.doc({
        'tags': ['groups'],
        'description': 'Adds a group',
        'reqparser': {'name': 'group parser',
                      'parser': post_parser},
        'responses': {
            '201': {
                'description': 'Created group',
                'content': {
                    'application/json': {
                        'examples': {
                            'application/json': {
                                'id': 1
                            }
                        }
                    }
                }
            }
        }
    })
    def post(self):
    ...
```

Swagger schema (among other things):

```json
{"GroupsModel": {
    "properties": {
        "id": {
            "default": null,
            "description": "Id of new group",
            "name": "id",
            "required": false,
            "type": "integer"
            },
        "name": {
            "default": null,
            "description": null,
            "name": "name",
            "required": true,
            "type": "string"
        }
    },
    "type": "object"
}
```

## Using authentication

In the example above, the view `UserItemResource` is a subclass of `Resource`, which is provided by `flask_restful`. However,
`flask_restful_swagger_3` provides a thin wrapper around `Resource` to provide authentication. By using this, you can
not only prevent access to resources, but also hide the documentation depending on the provided `api_key`.

Example:

```python
# Import Api and Resource instead from flask_restful_swagger_2
from flask_restful_swagger_3 import Api, swagger, Resource

api = Api(app)
def auth(api_key, endpoint, method):
    # Space for your fancy authentication. Return True if access is granted, otherwise False
    # api_key is extracted from the url parameters (?api_key=foo)
    # endpoint is the full swagger url (e.g. /some/{value}/endpoint)
    # method is the HTTP method
    return True

swagger.auth = auth

class MyView(Resource):
    @swagger.doc({
    # documentation...
    })
    def get(self):
        return SomeModel(value=5)

api.add_resource(MyView, '/some/endpoint')
```

## Specification document

The `get_swagger_doc` method of the Api instance returns the specification document object,
which may be useful for integration with other tools for generating formatted output or client code.

## Using Flask Blueprints

To use Flask Blueprints, create a function in your views module that creates the blueprint,
registers the resources and returns it wrapped in an Api instance:

```python
from flask import Blueprint, request
from flask_restful_swagger_3 import Api, swagger, Resource

class UserResource(Resource):
...

class UserItemResource(Resource):
...

def get_user_resources():
    """
    Returns user resources.
    :param app: The Flask instance
    :return: User resources
    """
    blueprint = Blueprint('user', __name__)

    api = Api(blueprint, add_api_spec_resource=False)

    api.add_resource(UserResource, '/api/users')
    api.add_resource(UserItemResource, '/api/users/<int:user_id>')

    return api
```

In your initialization module, collect the swagger document objects for each
set of resources, then use the `get_swagger_blueprint` function to combine the
documents and specify the URL to serve them at (default is '/api/doc/swagger').
Note that the `get_swagger_blueprint` function accepts the same keyword parameters
as the `Api` class to populate the fields of the combined swagger document.
Finally, register the swagger blueprint along with the blueprints for your
resources.

```python
from flask_restful_swagger_3 import get_swagger_blueprint

...

# A list of swagger document objects
docs = []

# Get user resources
user_resources = get_user_resources()

# Retrieve and save the swagger document object (do this for each set of resources).
docs.append(user_resources.get_swagger_doc())

# Register the blueprint for user resources
app.register_blueprint(user_resources.blueprint)

# Prepare a blueprint to serve the combined list of swagger document objects and register it
app.register_blueprint(get_swagger_blueprint(docs, '/api/doc/swagger', title='Example', api_version='1'))
```

Refer to the files in the `example` folder for the complete code.

## Running and testing

To run the example project in the `example` folder:

```shell script
pip install flask-restful-swagger-3
pip install flask-cors    # needed to access spec from swagger-ui
python app.py
```

To run the example which uses Flask Blueprints:

```shell script
python app_blueprint.py
```

The swagger spec will by default be at `http://localhost:5000/api/doc/swagger.json`. You can change the URL by passing
`api_spec_url='/my/path'` to the `Api` constructor. You can use [swagger-ui](https://github.com/swagger-api/swagger-ui)
to explore your api. Try it online at [http://petstore.swagger.io/](http://petstore.swagger.io/?url=http://localhost:5000/api/swagger.json)

To run tests:

```shell script
pip install tox # needed to run pytest
tox
```
