import data.roles as rls


def test_get_roles():
    roles = rls.get_roles()
    assert isinstance(roles,dict)
    