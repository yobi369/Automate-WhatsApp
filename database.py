import sqlite3

def create_connection():
    conn = sqlite3.connect('whatsapp_automation.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_message(phone_number, message, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (phone_number, message, status)
        VALUES (?, ?, ?)
    ''', (phone_number, message, status))
    conn.commit()
    conn.close()

def get_logs():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages')
    logs = cursor.fetchall()
    conn.close()
    return logs

if __name__ == "__main__":
    create_table()
