import sqlite3

def create_connection():
    conn = sqlite3.connect('quiz.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        score INTEGER)''')
    conn.commit()
    conn.close()

def insert_score(score):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO scores (score) VALUES (?)', (score,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        conn.close()

def get_high_scores():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT score FROM scores ORDER BY score DESC LIMIT 5')
    high_scores = cursor.fetchall()
    conn.close()

    return [{'score': score[0]} for score in high_scores]