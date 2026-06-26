import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DATABASE = os.path.join('/tmp', 'database.db')

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     name TEXT NOT NULL, 
                     email TEXT NOT NULL,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_db_connection():
    init_db()
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()
        return redirect('/')
    users = conn.execute('SELECT * FROM users ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')
