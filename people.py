"""
This module interfaces to our user data.
"""

MIN_USER_NAME_LEN = 2

# people fields:
NAME = 'name'
ROLES = 'roles'
AFFILIATION  = 'affiliation'
EMAIL = 'email'

TEST_EMAIL = 'na2819@nyu.edu'
TEST_PERSON_DICT = {
	TEST_EMAIL: {
		NAME: 'Nabira Ahmad',
		ROLES: [],
		AFFILIATION: 'NYU',
		EMAIL: TEST_EMAIL,
	},
}

"""
PARAMETERS: None
RETURNS: Dictionary of users keyed on user email
NOTE: Each user email is a key for another dictionary
"""

def get_people():
	users = TEST_PERSON_DICT
	return users
