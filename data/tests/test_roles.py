import pytest
import data.roles as rls


@pytest.fixture
def valid_roles():
    """Fixture for valid roles dictionary."""
    return rls.get_roles()

@pytest.fixture
def masthead_roles():
    """Fixture for masthead roles dictionary."""
    return rls.get_masthead_roles()


def test_get_roles(valid_roles):
    assert isinstance(valid_roles, dict)
    assert len(valid_roles) > 0
    for code, role in valid_roles.items():
        assert isinstance(code, str)
        assert isinstance(role, str)


def test_get_masthead_roles(masthead_roles):
    assert isinstance(masthead_roles, dict)
    assert len(masthead_roles) > 0


def test_get_role_codes():
    codes = rls.get_role_codes()
    assert isinstance(codes, list)
    for code in codes:
        assert isinstance(code, str)


def test_is_valid():
    assert rls.is_valid(rls.TEST_CODE)
