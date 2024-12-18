import pytest
from unittest.mock import patch
import data.manuscripts.fields as mflds


@patch('data.db_connect.read_dict', return_value={"title": {"disp_name": "Title"}})
def test_get_flds(mock_read_dict):
    assert isinstance(mflds.get_flds(), dict)
    mock_read_dict.assert_called_once()


@patch('data.db_connect.read_dict', return_value={"title": {"disp_name": "Title"}})
def test_get_fld_names(mock_read_dict):
    assert isinstance(mflds.get_fld_names(), list)
    assert "title" in mflds.get_fld_names()
    assert mock_read_dict.call_count == 2

@patch('data.db_connect.get_one', return_value={"field_name": "title", "disp_name": "Title"})
def test_get_disp_name(mock_get_one):
    result = mflds.get_disp_name("title")
    assert result == "Title"
    assert isinstance(result, str)
    mock_get_one.assert_called_once_with("fields", {"field_name": "title"})


@patch('data.db_connect.get_one', return_value=None)
def test_get_disp_name_invalid(mock_get_one):
    result = mflds.get_disp_name("invalid_field")
    assert result == "Unknown Field"
    mock_get_one.assert_called_once_with("fields", {"field_name": "invalid_field"})


@patch('data.db_connect.get_one', side_effect=[{"field_name": "title"}, None])
def test_is_field_valid(mock_get_one):
    assert mflds.is_field_valid("title")
    assert not mflds.is_field_valid("invalid_field")
    assert mock_get_one.call_count == 2


@patch('data.db_connect.create', return_value=True)
@patch('data.db_connect.get_one', return_value=None)
def test_add_field(mock_get_one, mock_create):
    assert mflds.add_field("new_field", "New Field")
    assert mock_create.called
    mock_create.assert_called_with("fields", {"field_name": "new_field", "disp_name": "New Field"})


@patch('data.db_connect.update_doc', return_value=True)
@patch('data.db_connect.get_one', return_value={"field_name": "field_to_update", "disp_name": "Old Name"})
def test_update_field(mock_get_one, mock_update_doc):
    assert mflds.update_field("field_to_update", "New Name")
    mock_update_doc.assert_called_once_with(
        "fields", {"field_name": "field_to_update"}, {"disp_name": "New Name"}
    )


@patch('data.db_connect.del_one', return_value=1)
@patch('data.db_connect.get_one', return_value={"field_name": "field_to_delete", "disp_name": "Delete Me"})
def test_del_field(mock_get_one, mock_del_one):
    assert mflds.del_field("field_to_delete")
    mock_del_one.assert_called_once_with("fields", {"field_name": "field_to_delete"})
