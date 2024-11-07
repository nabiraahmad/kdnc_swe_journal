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
    return text_dict


def create(key, title, text, email):
    if key in text_dict:
        raise ValueError(f"Entry with key '{key}' already exists.")
    text_dict[key] = {
        KEY: key,
        TITLE: title,
        TEXT: text,
        EMAIL: email,
    }
    return text_dict[key]


def get_one(key: str) -> dict:
    """
    Takes a key and returns the page dict for that key
    Returns an empty dict is key doesn't exist
    """
    result = {}
    if key in text_dict:
        result = text_dict[key]
    return result


def update(key, title=None, text=None, email=None):
    if key not in text_dict:
        raise ValueError(f"Entry with key '{key}' does not exist.")
    if title:
        text_dict[key][TITLE] = title
    if text:
        text_dict[key][TEXT] = text
    if email:
        text_dict[key][EMAIL] = email
    return text_dict[key]


def delete(key):
    if key not in text_dict:
        raise ValueError(f"Entry with key '{key}' does not exist.")
    del text_dict[key]
    return key


def main():
    print(read())


if __name__ == '__main__':
    main()
