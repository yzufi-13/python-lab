import hashlib
users={}
def add_user():
    print("Введіть логін:")
    login=input()
    print("Введіть пароль:")
    password=input()
    print("Введіть повне ПІБ:")
    full_name=input()
    users[login]={
        "password":hashlib.md5(password.encode()).hexdigest(),
        "full_name":full_name
    }
def check_user():
    print("Введіть логін:")
    login=input()
    print("Введіть пароль:")
    password=input()
    if login not in users:
        print("Користувача не знайдено")
        return
    h=hashlib.md5(password.encode()).hexdigest()
    if h==users[login]["password"]:
        print("Аутентифікація успішна")
        print("ПІБ:",users[login]["full_name"])
    else:
        print("Невірний пароль")
while True:
    print("1 - додати користувача")
    print("2 - перевірити пароль")
    print("0 - вихід")
    choice=input()
    if choice=="1":
        add_user()
    elif choice=="2":
        check_user()
    elif choice=="0":
        break
    else:
        print("Невірний вибір")