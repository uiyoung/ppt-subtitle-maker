import sqlite3

# DB 생성 (오토 커밋)
conn = sqlite3.connect("jeil.db", isolation_level=None)
# 커서 획득
c = conn.cursor()
# 테이블 생성 (데이터 타입은 TEST, NUMERIC, INTEGER, REAL, BLOB 등)
c.execute("CREATE TABLE IF NOT EXISTS lyrics\
    (id integer PRIMARY KEY AUTOINCREMENT, title text NOT NULL, lyrics text NOT NULL, type text NOT NULL, memo text)")

# insert
# c.execute("INSERT INTO lyrics(title, lyrics) values ('hi', 'there')")

c.execute("SELECT * FROM lyrics")
# print(c.fetchone())
# print(c.fetchone())
print(c.fetchall())

# for row in c.fetchall():
# print(row)

conn.close()
