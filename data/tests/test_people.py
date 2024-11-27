import pytest

import data.people as ppl

from data.roles import TEST_CODE as TEST_ROLE_CODE

NO_AT = 'jkajsd'
NO_NAME = '@kalsj'
NO_DOMAIN = 'kajshd@'
NO_SUB_DOMAIN = 'kajshd@com'
DOMAIN_TOO_SHORT = 'kajshd@nyu.e'
DOMAIN_TOO_LONG = 'kajshd@nyu.eedduu'

TEMP_EMAIL = 'temp_person@temp.org'

@pytest.fixture(scope='function')
def temp_person():
    email = ppl.create_person('Joe Smith', 'NYU', TEMP_EMAIL, TEST_ROLE_CODE)
    yield email
    try:
        ppl.delete_person(email)
    except:
        print('Person already deleted.')

def test_get_mh_fields():
    flds = ppl.get_mh_fields()
    assert isinstance(flds, list)
    assert len(flds) > 0

def test_create_mh_rec(temp_person):
    person_rec = ppl.get_one(temp_person)
    mh_rec = ppl.create_mh_rec(person_rec)
    assert isinstance(mh_rec, dict)
    for field in ppl.MH_FIELDS:
        assert field in mh_rec

def test_has_role(temp_person):
    person_rec = ppl.get_one(temp_person)
    assert ppl.has_role(person_rec, TEST_ROLE_CODE)

def test_doesnt_have_role(temp_person):
    person_rec = ppl.get_one(temp_person)
    assert not ppl.has_role(person_rec, 'Not a good role!')

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
    email = 'joe@nyu.edu'
    ppl.create_person('Joe Smith', 'NYU', email, 'ED')
    people = ppl.get_people()
    assert isinstance(people, dict)
    assert len(people) > 0
    # check for string IDs:
    for email, person in people.items():
        assert isinstance(email, str)
        assert ppl.NAME in person
    ppl.delete_person(email)

def test_get_one_not_there():
    assert ppl.get_one("Don't recognize that email!") is None

def test_get_one(temp_person):
    assert ppl.get_one(temp_person) is not None

def test_exists(temp_person):
    assert ppl.exists(temp_person)

def test_delete(temp_person):
    ppl.delete_person(temp_person)
    assert not ppl.exists(temp_person)


ADD_EMAIL = 'bill@nyu.edu'


def test_create_person():
    ppl.create_person('Joe Smith', 'NYU', ADD_EMAIL, TEST_ROLE_CODE)
    assert ppl.exists(ADD_EMAIL)
    ppl.delete_person(ADD_EMAIL)

def test_create_duplicate_person(temp_person):
    with pytest.raises(ValueError):
        ppl.create_person('Do not care about name',
                          'Or affiliation', temp_person,
                          TEST_ROLE_CODE)

VALID_ROLES = ['ED', 'AU']

TEST_UPDATE_NAME = 'Buffalo Bill'

def test_update(temp_person):
    ppl.update_person(TEST_UPDATE_NAME, 'UBuffalo', temp_person, VALID_ROLES)
    updated_rec = ppl.get_one(temp_person)
    assert updated_rec[ppl.NAME] == TEST_UPDATE_NAME

def test_update_not_there(temp_person):
    with pytest.raises(ValueError):
        ppl.update_person('Will Fail', 'University of the Void',
                   'Non-existent email', VALID_ROLES)

def test_create_bad_email():
    with pytest.raises(ValueError):
        ppl.create_person('Do not care about name',
                          'Or affiliation', 'bademail', TEST_ROLE_CODE)

def test_get_masthead():
    mh = ppl.get_masthead()
    assert isinstance(mh, dict)
