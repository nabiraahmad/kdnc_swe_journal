"""
This module interfaces to our user data.
"""
import re

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

CHAR_OR_DIGIT = r"^(?![a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$).*"


def is_valid_email(email: str) -> bool:
    return re.match(f"{CHAR_OR_DIGIT}.*@{CHAR_OR_DIGIT}.*", email)


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


def update_person(name: str, affiliation: str, email: str):
    people = get_people()
    if email in people:
        # Update the existing person's details
        people[email][NAME] = name
        people[email][AFFILIATION] = affiliation
        return people[email]  # Return the updated person's details
    else:
        # If the person does not exist, raise an error
        raise ValueError(f'Person with email {email} does not exist')


def is_valid_person(name: str, affiliation: str, email: str) -> bool:
    people = get_people()
    if email in people:
        raise ValueError(f'Adding duplicate {email=}')
    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    return True


def create_person(name: str, affiliation: str, email: str):
    people = get_people()
    if email in people:
        raise ValueError(f'Adding a duplicate user with email {email=}')
    people[email] = {NAME: name, AFFILIATION: affiliation, EMAIL: email}
    return email


def main():
    print(get_people())


if __name__ == '__main__':
    main()
