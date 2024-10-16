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
