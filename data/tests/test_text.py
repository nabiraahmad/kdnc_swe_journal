import pytest
import data.text as txt

def test_read():
    texts = txt.read()
    assert isinstance(texts, dict)
    for key in texts:
        assert isinstance(key, str)


def test_get_one_not_existent():
    assert txt.get_one("Not a page key!") == {}


def test_create():
    key = 'NewPage'
    title = 'New Page Title'
    text = 'This is a new page.'
    email = 'new@journal.com'
    
    new_entry = txt.create(key, title, text, email)
    
    assert new_entry[txt.KEY] == key
    assert new_entry[txt.TITLE] == title
    assert new_entry[txt.TEXT] == text
    assert new_entry[txt.EMAIL] == email

def test_create_duplicate():
    key = txt.TEST_KEY
    with pytest.raises(ValueError):
        txt.create(key, 'Duplicate Title', 'Duplicate text', 'duplicate@journal.com')

def test_update():
    key = txt.TEST_KEY
    updated_text = 'Updated text for the home page.'
    
    updated_entry = txt.update(key, text=updated_text)
    
    assert updated_entry[txt.TEXT] == updated_text

def test_update_nonexistent():
    key = 'NonExistentPage'
    with pytest.raises(ValueError):
        txt.update(key, text='This should fail.')

def test_delete():
    key = 'NewPage'
    deleted_key = txt.delete(key)
    
    assert deleted_key == key
    assert key not in txt.text_dict

def test_delete_nonexistent():
    key = 'NonExistentPage'
    with pytest.raises(ValueError):
        txt.delete(key)

