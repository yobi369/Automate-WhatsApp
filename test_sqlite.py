import sqlite3

def test_sqlite():
    try:
        conn = sqlite3.connect(':memory:')  # Create a new in-memory database
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)')
        cursor.execute('INSERT INTO test (name) VALUES (?)', ('Test Name',))
        cursor.execute('SELECT * FROM test')
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    print(test_sqlite())
