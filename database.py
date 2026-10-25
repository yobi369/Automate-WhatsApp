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


def create_scheduled_jobs_table():
    """Create durable recurring-job storage; existing databases migrate automatically."""
    with create_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scheduled_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT NOT NULL,
                message TEXT NOT NULL,
                send_time TEXT NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(phone_number, message, send_time)
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_scheduled_jobs_enabled ON scheduled_jobs(enabled)")


def add_scheduled_job(phone_number, message, send_time):
    if not phone_number or not message or not send_time:
        raise ValueError("Phone number, message and send time are required.")
    with create_connection() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO scheduled_jobs (phone_number, message, send_time)
               VALUES (?, ?, ?)""",
            (phone_number, message, send_time),
        )
        row = conn.execute(
            """SELECT id FROM scheduled_jobs
               WHERE phone_number = ? AND message = ? AND send_time = ?""",
            (phone_number, message, send_time),
        ).fetchone()
        return row[0]


def get_scheduled_jobs(enabled_only=True):
    with create_connection() as conn:
        if enabled_only:
            rows = conn.execute(
                """SELECT id, phone_number, message, send_time, enabled, created_at
                   FROM scheduled_jobs WHERE enabled = 1 ORDER BY id"""
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT id, phone_number, message, send_time, enabled, created_at
                   FROM scheduled_jobs ORDER BY id"""
            ).fetchall()
        return rows


def delete_scheduled_job(job_id):
    with create_connection() as conn:
        conn.execute("DELETE FROM scheduled_jobs WHERE id = ?", (job_id,))


