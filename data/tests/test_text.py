import pytest
from unittest.mock import patch
import data.text as txt

@patch('data.text.read', autospec=True)
def test_read(mock_read):
    mock_read.return_value = {
        'TestPage': {
            txt.KEY: 'TestPage',
            txt.TITLE: 'Test Page Title',
            txt.TEXT: 'This is a test page.',
            txt.EMAIL: 'test@journal.com'
        }
    }
    texts = txt.read()
    assert isinstance(texts, dict)
    for key in texts:
        assert isinstance(key, str)

@patch('data.text.get_one', autospec=True)
def test_get_one_not_existent(mock_get_one):
    mock_get_one.return_value = {}
    assert txt.get_one("Not a page key!") == {}

@patch('data.text.create', autospec=True)
def test_create(mock_create):
    key = 'NewPage'
    title = 'New Page Title'
    text = 'This is a new page.'
    email = 'new@journal.com'
    mock_create.return_value = {
        txt.KEY: key,
        txt.TITLE: title,
        txt.TEXT: text,
        txt.EMAIL: email,
    }
    new_entry = txt.create(key, title, text, email)
    assert new_entry[txt.KEY] == key
    assert new_entry[txt.TITLE] == title
    assert new_entry[txt.TEXT] == text
    assert new_entry[txt.EMAIL] == email

@patch('data.text.create', autospec=True)
def test_create_duplicate(mock_create):
    mock_create.side_effect = ValueError("Entry with key 'DuplicateKey' already exists.")
    with pytest.raises(ValueError):
        txt.create('DuplicateKey', 'Duplicate Title', 'Duplicate text', 'duplicate@journal.com')

@patch('data.text.update', autospec=True)
def test_update(mock_update):
    key = 'TestPage'
    updated_text = 'Updated text for the test page.'
    mock_update.return_value = {
        txt.KEY: key,
        txt.TEXT: updated_text,
    }
    updated_entry = txt.update(key, text=updated_text)
    assert updated_entry[txt.TEXT] == updated_text

@patch('data.text.update', autospec=True)
def test_update_nonexistent(mock_update):
    mock_update.side_effect = ValueError("Entry with key 'NonExistentPage' does not exist.")
    with pytest.raises(ValueError):
        txt.update('NonExistentPage', text='This should fail.')

@patch('data.text.delete', autospec=True)
def test_delete(mock_delete):
    key = 'NewPage'
    mock_delete.return_value = key
    deleted_key = txt.delete(key)
    assert deleted_key == key

@patch('data.text.delete', autospec=True)
def test_delete_nonexistent(mock_delete):
    mock_delete.side_effect = ValueError("Entry with key 'NonExistentPage' does not exist.")
    with pytest.raises(ValueError):
        txt.delete('NonExistentPage')
