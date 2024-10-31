# need to check import version 
from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest

from data.people import NAME 

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

def test_get_people():
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    resp_json = resp.get_json()
    for _id in resp_json:
        assert isinstance(_id, str)
        assert len(_id) > 0
        #assert NAME in person

def test_create_text_entry():
    new_text_entry = {
        'key': 'TestPage',
        'title': 'Test Page Title',
        'text': 'This is the content of the test page.',
        'email': 'test@journal.com'
    }
    
    resp = TEST_CLIENT.put(ep.TEXT_EP + '/create', json=new_text_entry)
    resp_json = resp.get_json()

    assert 'Return' in resp_json
    assert resp_json['Return']['key'] == new_text_entry['key']
    assert resp_json['Return']['title'] == new_text_entry['title']
    assert resp_json['Return']['text'] == new_text_entry['text']
    assert resp_json['Return']['email'] == new_text_entry['email']
