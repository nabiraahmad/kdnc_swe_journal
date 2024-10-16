"""
This module interfaces to our user data.
"""

# fields
KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'

TEST_KEY = 'HomePage'
DEL_KEY = 'DeletePage'

text_dict = {
    TEST_KEY: {
        KEY: TEST_KEY,
        TITLE: 'Home Page',
        TEXT: 'This is a journal about health and fitness.',
        EMAIL: 'contact@healthjournal.com',
    },
    DEL_KEY: {
        KEY: DEL_KEY,
        TITLE: 'Delete Page',
        TEXT: 'This is a journal about health and fitness.',
        EMAIL: 'admin@healthjournal.com',
    },
}


def read():
    text = text_dict
    return text
