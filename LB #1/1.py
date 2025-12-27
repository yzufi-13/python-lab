def count_words(s):
    d={}
    for w in s.lower().split():
        d[w]=d.get(w,0)+1
    return d
print("Введіть рядок з текстом:")
text=input()
result=count_words(text)
print("Словник слів і кількості:")
print(result)
more=[]
for k,v in result.items():
    if v>3:
        more.append(k)
print("Слова що зустрічаються більше 3 разів:")
print(more)