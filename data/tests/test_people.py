import pytest

import data.people as ppl

from data.roles import TEST_CODE

NO_AT = 'jkajsd'
NO_NAME = '@kalsj'
NO_DOMAIN = 'kajshd@'
NO_SUB_DOMAIN = 'kajshd@com'
DOMAIN_TOO_SHORT = 'kajshd@nyu.e'
DOMAIN_TOO_LONG = 'kajshd@nyu.eedduu'

TEMP_EMAIL = 'temp_person@temp.org'

@pytest.fixture(scope='function')
def temp_person():
    ret = ppl.create_person('Joe Smith', 'NYU', TEMP_EMAIL, TEST_CODE)
    yield ret
    ppl.delete_person(ret)


def test_is_valid_email_no_at():
    assert not ppl.is_valid_email(NO_AT)

def test_is_valid_no_name():
    assert not ppl.is_valid_email(NO_NAME)

def test_is_valid_np_domain():
    assert not ppl.is_valid_email(NO_DOMAIN)

def test_is_valid_no_sub_domain():
    assert not ppl.is_valid_email(NO_SUB_DOMAIN)

def test_is_valid_email_domain_too_short():
    assert not ppl.is_valid_email(DOMAIN_TOO_SHORT)

def test_is_valid_email_domain_too_long():
    assert not ppl.is_valid_email(DOMAIN_TOO_LONG)

def test_is_valid_emai():
    assert ppl.is_valid_email('dg3729@nyu.edu')
      
def test_get_people():
    people = ppl.get_people()
    assert isinstance(people, dict)
    assert len(people) > 0
    # check for string IDs:
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person

def test_get_one_not_there():
    assert ppl.get_one("Don't recognize that email!") is None


def test_get_one(temp_person):
    assert ppl.get_one(temp_person) is not None


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

VALID_ROLES = ['ED', 'AU']

@pytest.mark.skip('Skip because it is not done')
def test_update(temp_person):
    ppl.update('Buffalo Bill', 'Ubuffalo', temp_person, VALID_ROLES)


def test_create_bad_email():
    with pytest.raises(ValueError):
        ppl.create_person('Do not care about name',
                          'Or affiliation', 'bademail', TEST_CODE)


def test_get_masthead():
    mh = ppl.get_masthead()
    assert isinstance(mh, dict)


def test_get_mh_fields():
    flds = ppl.get_mh_fields()
    assert isinstance(flds,list)
    assert len(flds) > 0

    
