import pytest
import data.text as txt

def test_read():
    text = txt.read()
    assert isinstance(text, dict)
    assert len(text) > 0

    # Check that all expected keys and values are present and of correct types
    for _key, content in text.items():
        assert isinstance(_key, str)
        assert txt.KEY in content
        assert txt.TITLE in content
        assert txt.TEXT in content
        assert txt.EMAIL in content

        # Check that all values are of correct types
        assert isinstance(content[txt.KEY], str)
        assert isinstance(content[txt.TITLE], str)
        assert isinstance(content[txt.TEXT], str)
        assert isinstance(content[txt.EMAIL], str)

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

