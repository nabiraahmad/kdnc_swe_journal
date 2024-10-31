import pytest

import data.people as ppl

from data.roles import TEST_CODE

NO_AT = 'jkajsd'
NO_NAME = '@kalsj'
NO_DOMAIN = 'kajshd@'

def test_is_valid_email_no_at():
    assert not ppl.is_valid_email(NO_AT)

def test_is_valid_no_name():
    assert not ppl.is_valid_email(NO_NAME)

def test_is_valid_np_domain():
    assert not ppl.is_valid_email(NO_DOMAIN)

     
def test_get_people():
    people = ppl.get_people()
    assert isinstance(people, dict)
    assert len(people) > 0
    # check for string IDs:
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


def test_delete():
    people = ppl.get_people()
    old_len = len(people)
    ppl.delete_person(ppl.DEL_EMAIL)
    people = ppl.get_people()
    assert len(people) < old_len
    assert ppl.DEL_EMAIL not in people


ADD_EMAIL = 'bill@nyu.edu'


def test_create_person():
    people = ppl.get_people()
    assert ADD_EMAIL not in people
    ppl.create_person('Bill Smith', 'NYU', ADD_EMAIL, TEST_CODE)
    people = ppl.get_people()
    assert ADD_EMAIL in people


def test_create_duplicate_person():
    with pytest.raises(ValueError):
        ppl.create_person('Do not care about name', 
                          'Or affiliation', ppl.TEST_EMAIL, TEST_CODE)


def test_create_bad_email():
    with pytest.raises(ValueError):
        ppl.create_person('Do not care about name',
                          'Or affiliation', 'bademail', TEST_CODE)
