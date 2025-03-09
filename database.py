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

def create_contact_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def update_contact(contact_id, name, phone_number):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE contacts
        SET name = ?, phone_number = ?
        WHERE id = ?
    ''', (name, phone_number, contact_id))
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
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

def add_contact(name, phone_number):
    if not name or not phone_number:
        raise ValueError("Name and phone number cannot be empty.")
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contacts (name, phone_number)
        VALUES (?, ?)
    ''', (name, phone_number))
    conn.commit()
    conn.close()

def get_contacts():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts')
    contacts = cursor.fetchall()
    conn.close()
    return contacts

def get_logs():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages')
    logs = cursor.fetchall()
    conn.close()
    return logs

if __name__ == "__main__":
    create_table()
    create_contact_table()
