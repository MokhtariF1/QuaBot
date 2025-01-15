from sqlite3 import connect


db = connect("bot.db")
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (user_id, phone, name, city)")