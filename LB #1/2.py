inventory={"apple":10,"bread":3,"milk":6}
def update_product(name,qty):
    if name in inventory:
        inventory[name]+=qty
    else:
        inventory[name]=qty
    if inventory[name]<=0:
        del inventory[name]
print("Поточний склад:")
print(inventory)
print("Введіть назву продукту:")
name=input()
print("Введіть кількість (додати або відняти):")
qty=int(input())
update_product(name,qty)
print("Оновлений склад:")
print(inventory)
low=[]
for k,v in inventory.items():
    if v<5:
        low.append(k)
print("Продукти з кількістю менше 5:")
print(low)