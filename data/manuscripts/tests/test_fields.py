import pytest
from unittest.mock import patch
import data.manuscripts.fields as mflds


def test_get_flds():
    assert isinstance(mflds.get_flds(), dict)


def test_get_fld_names():
    assert isinstance(mflds.get_fld_names(), list)


@patch('data.manuscripts.fields.get_disp_name', autospec=True, return_value="Title")
def test_get_disp_name(mock_get_disp_name):
    result = mflds.get_disp_name("title")
    assert result == "Title"
    assert isinstance(result, str)


@patch('data.manuscripts.fields.get_disp_name', autospec=True, return_value=None)
def test_get_disp_name_invalid(mock_get_disp_name):
    result = mflds.get_disp_name("invalid_field")
    assert result is None, "Expected None for invalid field name"


def test_is_field_valid():
    assert mflds.is_field_valid("title")
    assert not mflds.is_field_valid("invalid_field")


def test_add_field():
    assert mflds.add_field("new_field", "New Field")
    assert mflds.is_field_valid("new_field")
    assert not mflds.add_field("new_field", "Duplicate Field")


def test_update_field():
    mflds.add_field("field_to_update", "Old Name")
    assert mflds.update_field("field_to_update", "New Name")
    assert mflds.get_disp_name("field_to_update") == "New Name"
    assert not mflds.update_field("non_existent_field", "Should Fail")


def test_del_field():
    mflds.add_field("field_to_delete", "Delete Me")
    assert mflds.del_field("field_to_delete")
    assert not mflds.is_field_valid("field_to_delete")
    assert not mflds.del_field("non_existent_field")
