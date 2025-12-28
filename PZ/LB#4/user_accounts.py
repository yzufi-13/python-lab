import hashlib
from datetime import datetime
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
class User:
    def __init__(self, username, password, is_active=True):
        self.username=username
        self.password_hash=hash_password(password)
        self.is_active=is_active
    def verify_password(self,password):
        return self.password_hash==hash_password(password)
class Administrator(User):
    def __init__(self, username, password, is_active=True, permissions=None):
        super().__init__(username,password,is_active)
        self.permissions=permissions if permissions is not None else []
    def has_permission(self,perm):
        return perm in self.permissions
class RegularUser(User):
    def __init__(self, username, password, is_active=True, last_login=None):
        super().__init__(username,password,is_active)
        self.last_login=last_login
    def set_last_login_now(self):
        self.last_login=datetime.now().isoformat()
class GuestUser(User):
    def __init__(self, username, password="guest", is_active=True):
        super().__init__(username,password,is_active)
    def can_read_only(self):
        return True
class AccessControl:
    def __init__(self):
        self.users={}
    def add_user(self,user):
        self.users[user.username]=user
    def authenticate_user(self,username,password):
        user=self.users.get(username)
        if user is None:
            return None
        if not user.is_active:
            return None
        if user.verify_password(password):
            return user
        return None