import sqlite3

def migrate_orders_to_db():
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    # إنشاء جدول الطلبات مع حالات متعددة (Pending, Processing, Done, Failed)
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        service TEXT,
        name TEXT,
        phone TEXT,
        imei TEXT,
        details TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate_orders_to_db()
    print('Orders table with status created.')
