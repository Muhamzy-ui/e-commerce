import sqlite3, os
p = 'db.sqlite3'
if not os.path.exists(p):
    print('NO DB FILE')
    raise SystemExit(1)
conn = sqlite3.connect(p)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cur.fetchall()]
print('tables:', tables)
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(t, 'rows =', cur.fetchone()[0])
    except Exception as e:
        print(t, 'error counting rows:', e)
conn.close()
print('db size:', os.path.getsize(p))
