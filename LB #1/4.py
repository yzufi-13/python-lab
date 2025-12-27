tasks={}
def add_task():
    print("Введіть назву задачі:")
    name=input()
    print("Введіть статус (виконано / в процесі / очікує):")
    status=input()
    tasks[name]=status
def delete_task():
    print("Введіть назву задачі для видалення:")
    name=input()
    if name in tasks:
        del tasks[name]
    else:
        print("Такої задачі немає")
def change_status():
    print("Введіть назву задачі:")
    name=input()
    if name in tasks:
        print("Введіть новий статус (виконано / в процесі / очікує):")
        status=input()
        tasks[name]=status
    else:
        print("Такої задачі немає")
def show_waiting():
    waiting=[]
    for k,v in tasks.items():
        if v=="очікує":
            waiting.append(k)
    print("Задачі зі статусом 'очікує':")
    print(waiting)
while True:
    print("1 - додати задачу")
    print("2 - видалити задачу")
    print("3 - змінити статус задачі")
    print("4 - показати задачі 'очікує'")
    print("5 - показати всі задачі")
    print("0 - вихід")
    choice=input()
    if choice=="1":
        add_task()
    elif choice=="2":
        delete_task()
    elif choice=="3":
        change_status()
    elif choice=="4":
        show_waiting()
    elif choice=="5":
        print(tasks)
    elif choice=="0":
        break
    else:
        print("Невірний вибір")