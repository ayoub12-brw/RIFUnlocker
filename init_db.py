import sqlite3

def init_db():
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        credits INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 0,
        role TEXT DEFAULT 'User',
        activation_token TEXT,
        reset_token TEXT,
        email_code TEXT,
        api_key TEXT,
        is_admin INTEGER DEFAULT 0
    )''')
    # جدول الطلبات
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        service TEXT,
        phone TEXT,
        imei TEXT,
        details TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        username TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    # جدول طلبات الشحن
    c.execute('''CREATE TABLE IF NOT EXISTS recharge_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        method TEXT,
        amount INTEGER,
        proof TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    # جدول سجل الرصيد
    c.execute('''CREATE TABLE IF NOT EXISTS credit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        amount INTEGER,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    # جدول الخدمات
    c.execute('''CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        description TEXT,
        price REAL,
        delivery_time TEXT,
        image_url TEXT,
        terms TEXT,
        is_active INTEGER DEFAULT 1
    )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('Database initialized.')
