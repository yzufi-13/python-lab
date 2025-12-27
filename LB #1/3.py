sales=[
    {"product":"apple","quantity":30,"price":20},
    {"product":"bread","quantity":10,"price":35},
    {"product":"apple","quantity":25,"price":20},
    {"product":"milk","quantity":15,"price":40},
    {"product":"bread","quantity":50,"price":35}
]
def revenue_by_product(sales_list):
    r={}
    for s in sales_list:
        p=s["product"]
        r[p]=r.get(p,0)+s["quantity"]*s["price"]
    return r
print("Продажі:")
print(sales)
revenue=revenue_by_product(sales)
print("Загальний дохід по продуктах:")
print(revenue)
big=[]
for k,v in revenue.items():
    if v>1000:
        big.append(k)
print("Продукти з доходом більше 1000:")
print(big)