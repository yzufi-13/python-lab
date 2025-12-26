import sqlite3
import hashlib
import os
DB_NAME = "users.db"
def connect():
    return sqlite3.connect(DB_NAME)
def create_db():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT UNIQUE, password TEXT, full_name TEXT)"
    )
    conn.commit()
    conn.close()
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def add_user(login, password, full_name):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)",
            (login, hash_password(password), full_name)
        )
        conn.commit()
        print("Користувача додано")
    except:
        print("Такий логін вже існує")
    conn.close()
def update_password(login, new_password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password = ? WHERE login = ?",
        (hash_password(new_password), login)
    )
    if cursor.rowcount == 0:
        print("Користувача не знайдено")
    else:
        print("Пароль оновлено")
    conn.commit()
    conn.close()
def authenticate(login):
    password = input("Введіть пароль: ")
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM users WHERE login = ?",
        (login,)
    )
    row = cursor.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        print("Успішна автентифікація")
    else:
        print("Невірний логін або пароль")
def menu():
    create_db()
    while True:
        print("1 - Додати користувача")
        print("2 - Оновити пароль")
        print("3 - Автентифікація")
        print("0 - Вихід")
        choice = input("Ваш вибір: ")
        if choice == "1":
            login = input("Логін: ")
            full_name = input("ПІБ: ")
            password = input("Пароль: ")
            add_user(login, password, full_name)
        elif choice == "2":
            login = input("Логін: ")
            new_password = input("Новий пароль: ")
            update_password(login, new_password)
        elif choice == "3":
            login = input("Логін: ")
            authenticate(login)
        elif choice == "0":
            break

menu()