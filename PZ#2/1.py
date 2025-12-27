import hashlib
class User:
    def __init__(self,username,password):
        self.username=username
        self.password_hash=hashlib.sha256(password.encode()).hexdigest()
        self.is_active=True
    def verify_password(self,password):
        return self.password_hash==hashlib.sha256(password.encode()).hexdigest()
class Administrator(User):
    def __init__(self,username,password):
        super().__init__(username,password)
        self.permissions=["ALL"]
class RegularUser(User):
    def __init__(self,username,password):
        super().__init__(username,password)
        self.last_login=None
class GuestUser(User):
    def __init__(self,username,password):
        super().__init__(username,password)
class AccessControl:
    def __init__(self):
        self.users={}
    def add_user(self,user):
        if user.username in self.users:
            return False
        self.users[user.username]=user
        return True
    def authenticate_user(self,username,password):
        if username not in self.users:
            return None
        user=self.users[username]
        if not user.is_active:
            return None
        if not user.verify_password(password):
            return None
        return user
ac=AccessControl()
while True:
    print("1 додати користувача")
    print("2 вхід")
    print("3 список користувачів")
    print("0 вихід")
    c=input()
    if c=="1":
        u=input("імя користувача:")
        p=input("пароль:")
        r=input("роль admin/user/guest:")
        if r=="admin":
            user=Administrator(u,p)
        elif r=="user":
            user=RegularUser(u,p)
        else:
            user=GuestUser(u,p)
        if ac.add_user(user):
            print("користувача додано")
        else:
            print("такий користувач вже існує")
    elif c=="2":
        u=input("імя користувача:")
        p=input("пароль:")
        user=ac.authenticate_user(u,p)
        if user:
            print("вхід успішний",type(user).__name__)
        else:
            print("помилка входу")
    elif c=="3":
        for u in ac.users.values():
            print(u.username,u.is_active,type(u).__name__)
    elif c=="0":
        break