import sqlite3
from datetime import datetime

def log_credit_action(user_id, action, amount, reason):
    conn = sqlite3.connect('site.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS credit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        amount INTEGER,
        reason TEXT,
        created_at TEXT
    )''')
    c.execute('INSERT INTO credit_logs (user_id, action, amount, reason, created_at) VALUES (?, ?, ?, ?, ?)',
              (user_id, action, amount, reason, datetime.now().isoformat()))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    log_credit_action(1, 'خصم', 2, 'فتح الشبكة')
    print('Logged.')
