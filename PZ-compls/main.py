import sqlite3
from datetime import datetime,timedelta
import random
DB_NAME="security_logs.db"
def conn():
    c=sqlite3.connect(DB_NAME)
    c.execute("PRAGMA foreign_keys=ON")
    return c
def init_db():
    c=conn()
    cur=c.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS EventSources(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        location TEXT,
        type TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS EventTypes(
        id INTEGER PRIMARY KEY,
        type_name TEXT UNIQUE,
        severity TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS SecurityEvents(
        id INTEGER PRIMARY KEY,
        timestamp DATETIME,
        source_id INTEGER,
        event_type_id INTEGER,
        message TEXT,
        ip_address TEXT,
        username TEXT,
        FOREIGN KEY(source_id) REFERENCES EventSources(id),
        FOREIGN KEY(event_type_id) REFERENCES EventTypes(id)
    )
    """)
    c.commit()
    c.close()
def seed_event_types():
    items=[
        ("Login Success","Informational"),
        ("Login Failed","Warning"),
        ("Port Scan Detected","Warning"),
        ("Malware Alert","Critical")
    ]
    c=conn()
    cur=c.cursor()
    for t,s in items:
        cur.execute("INSERT OR IGNORE INTO EventTypes(type_name,severity) VALUES(?,?)",(t,s))
    c.commit()
    c.close()
def add_source(name,location,stype):
    c=conn()
    cur=c.cursor()
    try:
        cur.execute("INSERT INTO EventSources(name,location,type) VALUES(?,?,?)",(name,location,stype))
        c.commit()
        print("OK: джерело додано")
    except sqlite3.IntegrityError:
        print("Помилка: джерело з такою назвою вже існує")
    c.close()
def add_event_type(type_name,severity):
    c=conn()
    cur=c.cursor()
    try:
        cur.execute("INSERT INTO EventTypes(type_name,severity) VALUES(?,?)",(type_name,severity))
        c.commit()
        print("OK: тип події додано")
    except sqlite3.IntegrityError:
        print("Помилка: такий тип події вже існує")
    c.close()
def get_source_id_by_name(name):
    c=conn()
    cur=c.cursor()
    cur.execute("SELECT id FROM EventSources WHERE name=?",(name,))
    r=cur.fetchone()
    c.close()
    return r[0] if r else None
def get_event_type_id_by_name(name):
    c=conn()
    cur=c.cursor()
    cur.execute("SELECT id FROM EventTypes WHERE type_name=?",(name,))
    r=cur.fetchone()
    c.close()
    return r[0] if r else None
def add_security_event(source_name,event_type_name,message,ip=None,username=None):
    sid=get_source_id_by_name(source_name)
    etid=get_event_type_id_by_name(event_type_name)
    if sid is None:
        print("Помилка: джерело не знайдено. Спочатку додай EventSources.")
        return
    if etid is None:
        print("Помилка: тип події не знайдено. Спочатку додай EventTypes.")
        return
    ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c=conn()
    cur=c.cursor()
    cur.execute("""
    INSERT INTO SecurityEvents(timestamp,source_id,event_type_id,message,ip_address,username)
    VALUES(?,?,?,?,?,?)
    """,(ts,sid,etid,message,ip,username))
    c.commit()
    c.close()
    print("OK: подію записано")
def list_sources():
    c=conn()
    cur=c.cursor()
    cur.execute("SELECT id,name,location,type FROM EventSources ORDER BY id")
    rows=cur.fetchall()
    c.close()
    if not rows:
        print("Порожньо")
        return
    for r in rows:
        print(r)
def list_event_types():
    c=conn()
    cur=c.cursor()
    cur.execute("SELECT id,type_name,severity FROM EventTypes ORDER BY id")
    rows=cur.fetchall()
    c.close()
    if not rows:
        print("Порожньо")
        return
    for r in rows:
        print(r)
def q_login_failed_24h():
    c=conn()
    cur=c.cursor()
    cur.execute("""
    SELECT se.id,se.timestamp,es.name,et.type_name,se.ip_address,se.username,se.message
    FROM SecurityEvents se
    JOIN EventTypes et ON et.id=se.event_type_id
    JOIN EventSources es ON es.id=se.source_id
    WHERE et.type_name='Login Failed'
      AND se.timestamp>=datetime('now','-1 day')
    ORDER BY se.timestamp DESC
    """)
    rows=cur.fetchall()
    c.close()
    if not rows:
        print("Немає подій")
        return
    for r in rows:
        print(r)
def q_bruteforce_ips():
    c=conn()
    cur=c.cursor()
    cur.execute("""
    SELECT se.ip_address,
           strftime('%Y-%m-%d %H:00:00',se.timestamp) AS hour_bucket,
           COUNT(*) AS cnt
    FROM SecurityEvents se
    JOIN EventTypes et ON et.id=se.event_type_id
    WHERE et.type_name='Login Failed'
      AND se.ip_address IS NOT NULL
      AND se.timestamp>=datetime('now','-1 day')
    GROUP BY se.ip_address,hour_bucket
    HAVING cnt>5
    ORDER BY cnt DESC
    """)
    rows=cur.fetchall()
    c.close()
    if not rows:
        print("Немає підозрілих IP")
        return
    for r in rows:
        print(r)
def q_critical_week_grouped():
    c=conn()
    cur=c.cursor()
    cur.execute("""
    SELECT es.name,COUNT(*) AS cnt
    FROM SecurityEvents se
    JOIN EventTypes et ON et.id=se.event_type_id
    JOIN EventSources es ON es.id=se.source_id
    WHERE et.severity='Critical'
      AND se.timestamp>=datetime('now','-7 day')
    GROUP BY es.name
    ORDER BY cnt DESC
    """)
    groups=cur.fetchall()
    if not groups:
        c.close()
        print("Немає Critical за тиждень")
        return
    print("Групи (джерело, кількість):")
    for g in groups:
        print(g)
    print("Деталі:")
    cur.execute("""
    SELECT se.id,se.timestamp,es.name,et.type_name,et.severity,se.ip_address,se.username,se.message
    FROM SecurityEvents se
    JOIN EventTypes et ON et.id=se.event_type_id
    JOIN EventSources es ON es.id=se.source_id
    WHERE et.severity='Critical'
      AND se.timestamp>=datetime('now','-7 day')
    ORDER BY es.name,se.timestamp DESC
    """)
    rows=cur.fetchall()
    c.close()
    for r in rows:
        print(r)
def q_search_keyword(keyword):
    c=conn()
    cur=c.cursor()
    cur.execute("""
    SELECT se.id,se.timestamp,es.name,et.type_name,se.ip_address,se.username,se.message
    FROM SecurityEvents se
    JOIN EventTypes et ON et.id=se.event_type_id
    JOIN EventSources es ON es.id=se.source_id
    WHERE se.message LIKE ?
    ORDER BY se.timestamp DESC
    """,(f"%{keyword}%",))
    rows=cur.fetchall()
    c.close()
    if not rows:
        print("Нічого не знайдено")
        return
    for r in rows:
        print(r)
def seed_sources_and_events():
    c=conn()
    cur=c.cursor()
    sources=[
        ("Firewall_A","10.0.0.1","Firewall"),
        ("Web_Server_Logs","10.0.0.20","Web Server"),
        ("IDS_Sensor_B","10.0.0.50","IDS")
    ]
    for s in sources:
        cur.execute("INSERT OR IGNORE INTO EventSources(name,location,type) VALUES(?,?,?)",s)
    c.commit()
    cur.execute("SELECT id,type_name FROM EventTypes")
    et=cur.fetchall()
    cur.execute("SELECT id,name FROM EventSources")
    es=cur.fetchall()
    if not et or not es:
        c.close()
        return
    et_map={name:i for i,name in et}
    es_map={name:i for i,name in es}
    ips=["185.11.22.33","203.0.113.7","198.51.100.9","10.0.0.123",None]
    users=["admin","student","root","anton",None,"guest","test","user1","user2"]
    base=datetime.now()
    for i in range(12):
        src=random.choice(list(es_map.keys()))
        t=random.choice(["Login Success","Login Failed","Port Scan Detected","Malware Alert"])
        ip=random.choice(ips)
        u=random.choice(users)
        if t=="Login Failed":
            msg=f"Невдала спроба входу користувача {u} з IP {ip}"
        elif t=="Login Success":
            msg=f"Успішний вхід користувача {u} з IP {ip}"
        elif t=="Port Scan Detected":
            msg=f"Виявлено сканування портів з IP {ip}"
        else:
            msg=f"Підозра на шкідливе ПЗ, файл: sample_{i}.exe, IP {ip}"
        dt=(base-timedelta(minutes=random.randint(0,60*24*6))).strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
        INSERT INTO SecurityEvents(timestamp,source_id,event_type_id,message,ip_address,username)
        VALUES(?,?,?,?,?,?)
        """,(dt,es_map[src],et_map[t],msg,ip,u))
    ip="185.11.22.33"
    u="admin"
    src_id=es_map["Web_Server_Logs"]
    et_id=et_map["Login Failed"]
    anchor=datetime.now().replace(minute=30,second=0,microsecond=0)
    for i in range(7):
        dt=(anchor-timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S")
        msg=f"Невдала спроба входу користувача {u} з IP {ip}"
        cur.execute("""
        INSERT INTO SecurityEvents(timestamp,source_id,event_type_id,message,ip_address,username)
        VALUES(?,?,?,?,?,?)
        """,(dt,src_id,et_id,msg,ip,u))
    c.commit()
    c.close()
    print("OK: додано тестові джерела і події")
def menu():
    while True:
        print("\n1-ініціалізація БД")
        print("2-додати джерело")
        print("3-додати тип події")
        print("4-записати подію безпеки")
        print("5-показати джерела")
        print("6-показати типи подій")
        print("7-запит: Login Failed за 24 години")
        print("8-запит: IP з >5 Login Failed за 1 годину")
        print("9-запит: Critical за тиждень згруповано за джерелом")
        print("10-пошук по ключовому слову в message")
        print("11-додати тестові дані")
        print("0-вихід")
        ch=input("Вибір: ").strip()
        if ch=="1":
            init_db()
            seed_event_types()
            print("OK: БД готова")
        elif ch=="2":
            name=input("name: ").strip()
            loc=input("location: ").strip()
            t=input("type: ").strip()
            add_source(name,loc,t)
        elif ch=="3":
            tn=input("type_name: ").strip()
            sev=input("severity: ").strip()
            add_event_type(tn,sev)
        elif ch=="4":
            s=input("source name: ").strip()
            t=input("event type_name: ").strip()
            msg=input("message: ").strip()
            ip=input("ip (можна пусто): ").strip()
            if ip=="":
                ip=None
            u=input("username (можна пусто): ").strip()
            if u=="":
                u=None
            add_security_event(s,t,msg,ip,u)
        elif ch=="5":
            list_sources()
        elif ch=="6":
            list_event_types()
        elif ch=="7":
            q_login_failed_24h()
        elif ch=="8":
            q_bruteforce_ips()
        elif ch=="9":
            q_critical_week_grouped()
        elif ch=="10":
            k=input("keyword: ").strip()
            q_search_keyword(k)
        elif ch=="11":
            init_db()
            seed_event_types()
            seed_sources_and_events()
        elif ch=="0":
            break
        else:
            print("Невірний вибір")
if __name__=="__main__":
    menu()