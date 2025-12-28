import pytest
from user_accounts import hash_password, User, Administrator, RegularUser, GuestUser, AccessControl
def test_hash_password_same_input_same_hash():
    assert hash_password("123")==hash_password("123")
def test_hash_password_different_input_different_hash():
    assert hash_password("123")!=hash_password("124")
def test_user_verify_password_true():
    u=User("a","pass")
    assert u.verify_password("pass") is True
def test_user_verify_password_false():
    u=User("a","pass")
    assert u.verify_password("no") is False
def test_admin_has_permission_true():
    a=Administrator("adm","p",permissions=["ban","edit"])
    assert a.has_permission("ban") is True
def test_admin_has_permission_false():
    a=Administrator("adm","p",permissions=["ban","edit"])
    assert a.has_permission("read") is False
def test_regular_user_set_last_login_now_sets_value():
    r=RegularUser("u","p")
    assert r.last_login is None
    r.set_last_login_now()
    assert r.last_login is not None
def test_regular_user_last_login_is_string():
    r=RegularUser("u","p")
    r.set_last_login_now()
    assert isinstance(r.last_login,str)
def test_guest_can_read_only_true():
    g=GuestUser("g")
    assert g.can_read_only() is True
def test_guest_default_password_authenticates():
    ac=AccessControl()
    g=GuestUser("guest1")
    ac.add_user(g)
    assert ac.authenticate_user("guest1","guest") is not None
def test_accesscontrol_add_user_stores_user():
    ac=AccessControl()
    u=User("x","p")
    ac.add_user(u)
    assert "x" in ac.users
def test_accesscontrol_authenticate_success():
    ac=AccessControl()
    u=User("x","p")
    ac.add_user(u)
    assert ac.authenticate_user("x","p") is u
def test_accesscontrol_authenticate_wrong_password_none():
    ac=AccessControl()
    u=User("x","p")
    ac.add_user(u)
    assert ac.authenticate_user("x","bad") is None
def test_accesscontrol_authenticate_no_user_none():
    ac=AccessControl()
    assert ac.authenticate_user("no","p") is None
def test_accesscontrol_authenticate_inactive_none():
    ac=AccessControl()
    u=User("x","p",is_active=False)
    ac.add_user(u)
    assert ac.authenticate_user("x","p") is None