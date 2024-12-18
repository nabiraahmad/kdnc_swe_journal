# need to check import version
from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
    CREATED,
)

from unittest.mock import patch

import pytest

from data.people import NAME

from data.manuscripts.fields import DISP_NAME

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json

def test_title():
    resp = TEST_CLIENT.get(ep.TITLE_EP)
    resp_json = resp.get_json()
    assert ep.TITLE_RESP in resp_json
    assert isinstance(resp_json[ep.TITLE_RESP], str)
    assert len(resp_json[ep.TITLE_RESP]) > 0

@patch('data.people.get_people', autospec=True,
       return_value={'id': {NAME: 'Joe Schmoe'}})
def test_get_people(mock_get_people):
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert NAME in person

@patch('data.people.get_one', autospec=True,
       return_value={NAME: 'Joe Schmoe'})
def test_get_one(mock_get_people):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == OK

@patch('data.people.get_one', autospec=True, return_value=None)
def test_get_one_not_found(mock_get_people):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == NOT_FOUND

def test_read_texts():
    with patch('data.text.read', return_value={'TestPage': {'key': 'TestPage', 'title': 'Test Title'}}):
        resp = TEST_CLIENT.get(f'{ep.TEXT_EP}/read')
        assert resp.status_code == OK
        assert 'TestPage' in resp.get_json()

def test_get_text():
    with patch('data.text.get_one', return_value={'key': 'TestPage', 'title': 'Test Title'}):
        resp = TEST_CLIENT.get(f'{ep.TEXT_EP}/TestPage')
        assert resp.status_code == OK
        assert resp.get_json()['key'] == 'TestPage'

def test_get_text_not_found():
    with patch('data.text.get_one', return_value={}):
        resp = TEST_CLIENT.get(f'{ep.TEXT_EP}/NonExistentPage')
        assert resp.status_code == NOT_FOUND

def test_create_text():
    with patch('data.text.create', return_value={'key': 'NewPage', 'title': 'New Title'}):
        new_text = {
            'key': 'NewPage',
            'title': 'New Title',
            'text': 'New Content',
            'email': 'new@example.com'
        }
        resp = TEST_CLIENT.put(f'{ep.TEXT_EP}/create', json=new_text)
        assert resp.status_code == CREATED

def test_create_text_duplicate():
    with patch('data.text.create', side_effect=ValueError("Duplicate key")):
        new_text = {'key': 'DuplicatePage', 'title': 'Duplicate Title'}
        resp = TEST_CLIENT.put(f'{ep.TEXT_EP}/create', json=new_text)
        assert resp.status_code == BAD_REQUEST

def test_update_text():
    with patch('data.text.update', return_value={'key': 'TestPage', 'text': 'Updated Content'}):
        update_data = {'text': 'Updated Content'}
        resp = TEST_CLIENT.patch(f'{ep.TEXT_EP}/update/TestPage', json=update_data)
        assert resp.status_code == OK

def test_update_text_not_found():
    with patch('data.text.update', side_effect=ValueError("Key not found")):
        update_data = {'text': 'Should fail'}
        resp = TEST_CLIENT.patch(f'{ep.TEXT_EP}/update/NonExistentPage', json=update_data)
        assert resp.status_code == NOT_FOUND

def test_delete_text():
    with patch('data.text.delete', return_value='TestPage'):
        resp = TEST_CLIENT.delete(f'{ep.TEXT_EP}/delete/TestPage')
        assert resp.status_code == OK

def test_delete_text_not_found():
    with patch('data.text.delete', side_effect=ValueError("Key not found")):
        resp = TEST_CLIENT.delete(f'{ep.TEXT_EP}/delete/NonExistentPage')
        assert resp.status_code == NOT_FOUND

@patch('data.manuscripts.fields.get_flds', autospec=True)
def test_get_fields(mock_get_flds):
    mock_get_flds.return_value = {'title': {DISP_NAME: 'Title'}}
    resp = TEST_CLIENT.get(ep.MANUSCRIPT_FIELDS_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    for field_name, details in resp_json.items():
        assert isinstance(field_name, str)
        assert DISP_NAME in details

@patch('data.manuscripts.fields.add_field', autospec=True)
def test_create_field(mock_add_field):
    new_field = {'field_name': 'abstract', 'display_name': 'Abstract'}
    mock_add_field.return_value = True
    resp = TEST_CLIENT.post(ep.MANUSCRIPT_FIELDS_EP, json=new_field)
    assert resp.status_code == 201
    assert resp.get_json()['message'] == f'Field "{new_field["field_name"]}" added successfully.'

@patch('data.manuscripts.fields.update_field', autospec=True)
def test_update_field(mock_update_field):
    update_data = {'display_name': 'Updated Abstract'}
    mock_update_field.return_value = True
    resp = TEST_CLIENT.patch(f'{ep.MANUSCRIPT_FIELDS_EP}/abstract', json=update_data)
    assert resp.status_code == OK

@patch('data.manuscripts.fields.del_field', autospec=True)
def test_delete_field(mock_del_field):
    mock_del_field.return_value = True
    resp = TEST_CLIENT.delete(f'{ep.MANUSCRIPT_FIELDS_EP}/abstract')
    assert resp.status_code == OK
