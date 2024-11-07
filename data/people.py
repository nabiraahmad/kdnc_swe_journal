"""
This module interfaces to our user data.
"""
import re

import data.roles as rls

MIN_USER_NAME_LEN = 2

# people fields:
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

TEST_EMAIL = 'na2819@nyu.edu'
DEL_EMAIL = 'dg3729@nyu.edu'

MH_FIELDS = [NAME, AFFILIATION]

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

CHAR_OR_DIGIT = '[A-Za-z0-9]'
VALID_CHARS = '[A-Za-z0-9_.]'


def is_valid_email(email: str) -> bool:
    return re.fullmatch(f"{VALID_CHARS}+@{CHAR_OR_DIGIT}+"
                        + "\\."
                        + f"{CHAR_OR_DIGIT}"
                        + "{2,3}", email)


def get_people():
    people = TEST_PERSON_DICT
    return people


def get_one(email: str) -> dict:
    """
    Return a person record if email is present in the DB
    else return none"""
    return TEST_PERSON_DICT.get(email)


def delete_person(_id):
    people = get_people()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None


def has_role(person: dict, role: str) -> bool:
    if role in person.get(ROLES):
        return True
    return False


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


def is_valid_person(name: str, affiliation: str, email: str,
                    role: str = None, roles: list = None) -> bool:

    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    if role:
        if not rls.is_valid(role):
            raise ValueError(f'Invalid role: {role}')
    elif roles:
        for role in roles:
            if not rls.is_valid(role):
                raise ValueError(f'Invalid role: {role}')

    return True


def create_person(name: str, affiliation: str, email: str, role: str):
    people = get_people()
    if email in people:
        raise ValueError(f'Adding duplicate {email=}')
    if is_valid_person(name, affiliation, email, role):

        roles = []
        if role:
            roles.append(role)
        people[email] = {
            NAME: name,
            AFFILIATION: affiliation,
            EMAIL: email,
            ROLES: [role]
        }
        return email


def update(name: str, affiliation: str, email: str, roles: list):
    people = get_people()
    if email not in people:
        raise ValueError('Updating non-existing person: {email=}')
    if is_valid_person(name, affiliation, email, roles=roles):
        people[email] = {
            NAME: name,
            AFFILIATION: affiliation,
            EMAIL: email,
            ROLES: roles
        }

        return email


def create_mh_rec(person: dict) -> dict:
    mh_rec = {}
    for field in MH_FIELDS:
        mh_rec[field] = person.get(field, '')
    return mh_rec


def get_masthead() -> dict:
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_w_role = {}
        people = get_people()
        for _id, person in people.items():
            if has_role(person, mh_role):
                rec = create_mh_rec(person)
                people_w_role.append(rec)
        masthead[text] = people_w_role
    return masthead


def main():
    print(get_masthead())


if __name__ == '__main__':
    main()
