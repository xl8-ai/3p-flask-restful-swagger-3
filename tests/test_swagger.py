import pytest
from flask_restful import inputs
import flask_restful_swagger_3.swagger as swagger

from tests.models import SwaggerTestModel


def test_should_set_nested():
    d = {'openapi': '3.0.0'}
    swagger.set_nested(d, 'info.title', 'API')
    assert d == {'openapi': '3.0.0', 'info': {'title': 'API'}}


def test_should_get_data_type_str():
    assert swagger.get_data_type({'schema': {'type': 'string'}}) == str


def test_should_get_data_type_str_date():
    assert swagger.get_data_type({'schema': {'type': 'string', 'format': 'date'}}) == inputs.date


def test_should_get_data_type_str_date_time():
    assert swagger.get_data_type({'schema': {'type': 'string', 'format': 'date-time'}}) == inputs.datetime_from_iso8601


def test_should_get_data_type_int():
    assert swagger.get_data_type({'schema': {'type': 'integer'}}) == int


def test_should_get_data_type_bool():
    assert swagger.get_data_type({'schema': {'type': 'boolean'}}) == inputs.boolean


def test_should_get_data_type_float():
    assert swagger.get_data_type({'schema': {'type': 'number', 'format': 'float'}}) == float


def test_should_get_data_type_double():
    assert swagger.get_data_type({'schema': {'type': 'number', 'format': 'double'}}) == float


def test_should_get_data_type_invalid():
    assert swagger.get_data_type({}) is None


def test_should_get_parser_arg():
    param = {
        'name': 'name',
        'description': 'Name to filter by',
        'schema': {
            'type': 'string',
        },
        'in': 'query'
    }

    expected = ('name', {
        'dest': 'name',
        'type': str,
        'location': 'args',
        'help': 'Name to filter by',
        'required': False,
        'default': None,
        'action': 'store'
    })

    assert swagger.get_parser_arg(param) == expected


def test_should_get_parser_args():
    params = [
        {
            'name': 'body',
            'description': 'Request body',
            'in': 'path',
            'required': True,
        },
        {
            'name': 'name',
            'description': 'Name to filter by',
            'schema': {
                'type': 'string'
            },
            'in': 'query'
        }
    ]

    expected = [('name', {
        'dest': 'name',
        'type': str,
        'location': 'args',
        'help': 'Name to filter by',
        'required': False,
        'default': None,
        'action': 'store'
    })]

    assert swagger.get_parser_args(params) == expected


def test_array_get_parser_args():
    params = [
        {
            'name': 'body',
            'description': 'Request body',
            'in': 'path',
            'required': True,
        },
        {
            'name': 'name',
            'description': 'Name to filter by',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'string'
                },
            },
            'in': 'query'
        }
    ]

    expected = [('name', {
        'dest': 'name',
        'type': str,
        'location': 'args',
        'help': 'Name to filter by',
        'required': False,
        'default': None,
        'action': 'append'
    })]

    assert swagger.get_parser_args(params) == expected


def test_should_validate_path_item_object_invalid_field():
    with pytest.raises(swagger.ValidationError):
        assert swagger.validate_path_item_object({'some_invalid_field': 1})


def test_should_validate_operation_object_invalid_field():
    with pytest.raises(swagger.ValidationError):
        assert swagger.validate_operation_object({'some_invalid_field': 1})


def test_should_validate_operation_object_no_responses():
    obj = {
        'description': 'Returns all users',
        'parameters': [
            {
                'name': 'name',
                'description': 'Name to filter by',
                'type': 'string',
                'in': 'query'
            }
        ]
    }

    with pytest.raises(swagger.ValidationError):
        assert swagger.validate_operation_object(obj)


def test_should_validate_parameter_object_invalid_field():
    with pytest.raises(swagger.ValidationError):
        assert swagger.validate_parameter_object({'some_invalid_field': 1})


def test_should_validate_parameter_object_no_name_field():
    obj = {
        'description': 'Name to filter by',
        'type': 'string',
        'in': 'query'
    }

    with pytest.raises(swagger.ValidationError):
        swagger.validate_parameter_object(obj)


def test_should_validate_parameter_object_no_in_field():
    obj = {
        'name': 'name',
        'description': 'Name to filter by',
        'type': 'string',
    }

    with pytest.raises(swagger.ValidationError):
        swagger.validate_parameter_object(obj)


def test_should_validate_parameter_object_invalid_in_field():
    obj = {
        'name': 'name',
        'description': 'Name to filter by',
        'type': 'string',
        'in': 'some_invalid_field'
    }

    with pytest.raises(swagger.ValidationError):
        swagger.validate_parameter_object(obj)


def test_should_validate_parameter_object_body_no_schema():
    obj = {
        'name': 'name',
        'description': 'Name to filter by',
        'type': 'string',
        'in': 'body'
    }

    with pytest.raises(swagger.ValidationError):
        swagger.validate_parameter_object(obj)


def test_should_validate_parameter_object_no_type_field():
    obj = {
        'description': 'Name to filter by',
        'in': 'query'
    }

    with pytest.raises(swagger.ValidationError):
        swagger.validate_parameter_object(obj)


def test_should_validate_parameter_object_array_no_items_field():
    obj = {
        'name': 'name',
        'description': 'Name to filter by',
        'type': 'array',
        'in': 'query',
    }

    with pytest.raises(swagger.ValidationError):
        swagger.validate_parameter_object(obj)


def test_should_validate_reference_object_no_ref_field():
    with pytest.raises(swagger.ValidationError):
        swagger.validate_reference_object({})


def test_should_validate_reference_object_multiple_keys():
    with pytest.raises(swagger.ValidationError):
        swagger.validate_reference_object({'$ref': 1, 'other_field': 2})


def test_should_validate_response_object_invalid_field():
    with pytest.raises(swagger.ValidationError):
        swagger.validate_response_object({'some_invalid_field': 1})


def test_should_validate_response_object_no_description():
    obj = {
        'examples': {
            'application/json': [
                {
                    'id': 1,
                    'name': 'somebody'
                }
            ]
        }
    }

    with pytest.raises(swagger.ValidationError):
        swagger.validate_response_object(obj)


def test_should_validate_schema_object_required_not_list():
    obj = {
        "properties": {
            "id": {
                "format": "int64",
                "type": "integer"
            },
            "keys": {
                "items": {
                    "$ref": "#/definitions/KeysModel"
                },
                "type": "array"
            },
            "mail": {
                "$ref": "#/definitions/EmailModel"
            },
            "name": {
                "type": "string"
            }
        },
        "required": "name",
        "type": "object"
    }

    with pytest.raises(swagger.ValidationError):
        swagger.validate_schema_object(obj)


def test_should_extract_swagger_path():
    assert swagger.extract_swagger_path('/path/<parameter>') == '/path/{parameter}'


def test_should_extract_swagger_path_extended():
    assert swagger.extract_swagger_path(
        '/<string(length=2):lang_code>/<string:id>/<float:probability>') == '/{lang_code}/{id}/{probability}'


def test_should_sanitize_doc():
    assert swagger.sanitize_doc('line1\nline2\nline3') == 'line1<br/>line2<br/>line3'


def test_should_sanitize_doc_multi_line():
    assert swagger.sanitize_doc(['line1\nline2', None, 'line3\nline4']) == 'line1<br/>line2<br/>line3<br/>line4'


def test_should_parse_method_doc():
    def test_func(a):
        """
        Test function
        :param a: argument
        :return: Nothing
        """

    assert swagger.parse_method_doc(test_func, {}) == 'Test function'


def test_should_parse_method_doc_append_summary():
    def test_func(a):
        """
        Test function
        :param a: argument
        :return: Nothing
        """

    assert swagger.parse_method_doc(test_func, {'summary': 'Summary'}) == 'Summary<br/>Test function'


def test_should_parse_schema_doc():
    test_model = SwaggerTestModel()
    assert swagger.parse_schema_doc(test_model, {}) == 'Test schema model.'


def test_should_parse_schema_doc_existing_description():
    test_model = SwaggerTestModel()
    assert swagger.parse_schema_doc(test_model, {'description': 'Test description'}) is None
