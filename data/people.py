"""
This module interfaces to our user data.
"""

MIN_USER_NAME_LEN = 2

# people fields:
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

TEST_EMAIL = 'na2819@nyu.edu'
DEL_EMAIL = 'dg3729@nyu.edu'

TEST_PERSON_DICT = {
    TEST_EMAIL: {
        NAME: 'Nabira Ahmad',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: TEST_EMAIL,
    },
    DEL_EMAIL: {
        NAME: 'Dariana Gonzalez',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: DEL_EMAIL,
    },
}

"""
PARAMETERS: None
RETURNS: Dictionary of users keyed on user email
NOTE: Each user email is a key for another dictionary
"""


def get_people():
    people = TEST_PERSON_DICT
    return people


def delete_person(_id):
    people = get_people()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None
