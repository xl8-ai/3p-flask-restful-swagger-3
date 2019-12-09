import pytest
from tests.models import SchemaTestModel


def test_should_validate_schema_valid():
    assert SchemaTestModel(**{'id': 1, 'name': 'somebody'}) == {'id': 1, 'name': 'somebody'}


def test_should_validate_schema_missing_required():
    with pytest.raises(ValueError):
        assert SchemaTestModel(**{'name': 'somebody'})


def test_should_validate_schema_invalid_type():
    with pytest.raises(ValueError):
        assert SchemaTestModel(**{'id': '1'})
