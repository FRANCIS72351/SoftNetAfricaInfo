import sqlite3
import uuid

class ShortLinkDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("CREATE TABLE IF NOT EXISTS shortlinks (code TEXT PRIMARY KEY, url TEXT)")
        self.conn.commit()

    def get_or_create_short_link(self, url):
        cur = self.conn.cursor()
        cur.execute("SELECT code FROM shortlinks WHERE url=?", (url,))
        row = cur.fetchone()
        if row:
            return f"/r/{row[0]}"
        code = uuid.uuid4().hex[:8]
        cur.execute("INSERT INTO shortlinks VALUES (?, ?)", (code, url))
        self.conn.commit()
        return f"/r/{code}"

    def get_url(self, code):
        cur = self.conn.cursor()
        cur.execute("SELECT url FROM shortlinks WHERE code=?", (code,))
        row = cur.fetchone()
        return row[0] if row else None
