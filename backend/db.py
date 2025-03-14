import sqlite3
DB_PATH = "/app/db/database.db"

try:
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
except sqlite3.OperationalError:
    con = sqlite3.connect("../db/database.db", check_same_thread=False)

def get_ytb_url(country, style) -> str:
    cur = con.cursor()
    cur.execute("SELECT URL FROM YTB_URL WHERE COUNTRY=:c and STYLE=:s ORDER BY RANDOM() LIMIT 1;", 
                {"c": country, "s": style})
    
    row = cur.fetchone()  # Récupération unique
    
    cur.close()
    
    return row[0] if row else "_tr5wNHYpNk"


def get_all_ytb_urls():
    try:
        con = sqlite3.connect("../db/database.db", check_same_thread=False)
    except sqlite3.OperationalError:
        con = sqlite3.connect("./db/database.db", check_same_thread=False)
    
    cur = con.cursor()
    cur.execute("SELECT * FROM YTB_URL;")
    rows = cur.fetchall()
    cur.close()
    con.close()
    
    return rows


def create_table_ytb():
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS YTB_URL (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                URL TEXT UNIQUE NOT NULL,
                COUNTRY TEXT NOT NULL,
                STYLE TEXT NOT NULL
            );""")
    cur.close()
    con.commit()

def create_table_trash():
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS TRASH (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                URL TEXT UNIQUE NOT NULL
            );""")
    cur.close()
    con.commit()

def insert_table(datas):
    cur = con.cursor()
    count = 0
    for data in datas:
        try:
            cur.execute("INSERT INTO YTB_URL (URL, COUNTRY, STYLE) VALUES (?, ?, ?);", data)
        except sqlite3.IntegrityError:
            count+=1
    print("error: ", count, " duplicate entry or constraint issue")
    con.commit()
    cur.close()

def insert_table_trash(url):
    print(url)
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO TRASH (URL) VALUES (?);", (url,))
    except sqlite3.IntegrityError:
        pass
    con.commit()
    cur.close()


def drop_table_ytb():
    cur = con.cursor()
    cur.execute("DROP TABLE YTB_URL;")
    cur.close()
    con.commit()

def drop_table_trash():
    cur = con.cursor()
    cur.execute("DROP TABLE TRASH;")
    cur.close()
    con.commit()


def display_trash_urls():
    cur = con.cursor()
    
    # Récupère toutes les URL dans la table TRASH
    cur.execute("SELECT URL FROM TRASH;")
    rows = cur.fetchall()
    
    if rows:
        print("URLs in TRASH:")
        for row in rows:
            print(row)
    cur.close()
