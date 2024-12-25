from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

@app.route('/', methods=['GET', 'POST'])
def index():
    conn, cursor = get_db_connection()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In real app, HASH this!
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect(url_for('login'))  # Redirect to login after registration
        except sqlite3.IntegrityError:
            return "Username already exists."
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn, cursor = get_db_connection()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In real app, compare HASHES!
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            return "Login successful!"  # In real app, use sessions
    else:
        return "Invalid username or password."
    conn.close()
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)