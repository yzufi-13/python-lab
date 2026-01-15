from telethon import TelegramClient
import asyncio
api_id= Test
api_hash="Test"
session_name="session"
async def main():
    print("1) старт програми")
    client=TelegramClient(session_name,api_id,api_hash)
    print("2) підключення до Telegram")
    try:
        await client.start()
    except Exception as e:
        print("помилка входу:",type(e).__name__,e)
        return
    try:
        me=await client.get_me()
        print("3) увійшов, id:",me.id)
    except Exception as e:
        print("помилка після входу:",type(e).__name__,e)
        return
    chat=input("введи чат або паблік (@username, посилання або me): ").strip()
    try:
        entity=await client.get_entity(chat)
        print("4) чат знайдено")
    except Exception as e:
        print("помилка пошуку чата:",type(e).__name__,e)
        await client.disconnect()
        return
    limit_text=input("скільки користувачів показати (наприклад 50): ").strip()
    limit=int(limit_text) if limit_text.isdigit() else 50
    print("5) отримую користувачів")
    i=0
    try:
        async for u in client.iter_participants(entity):
            i+=1
            print(i,getattr(u,"username",None),u.id)
            if i>=limit:
                break
        print("6) користувачів виведено:",i)
    except Exception as e:
        print("помилка читання користувачів:",type(e).__name__,e)
    to_user=input("написати напряму? введи username або skip: ").strip()
    if to_user!="skip":
        text=input("текст: ").strip()
        try:
            await client.send_message(to_user,text)
            print("повідомлення відправлено")
        except Exception as e:
            print("помилка відправки:",type(e).__name__,e)
    to_chat=input("написати в цей чат? (y/n): ").strip().lower()
    if to_chat=="y":
        text=input("текст: ").strip()
        try:
            await client.send_message(entity,text)
            print("повідомлення в чат відправлено")
        except Exception as e:
            print("помилка відправки в чат:",type(e).__name__,e)
    await client.disconnect()
    print("7) кінець")
if __name__=="__main__":
    asyncio.run(main())
