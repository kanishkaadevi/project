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
                     phone TEXT,
                     age INTEGER,
                     city TEXT,
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
    search = request.args.get('search', '')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        age = request.form['age']
        city = request.form['city']
        conn.execute('INSERT INTO users (name, email, phone, age, city) VALUES (?, ?, ?, ?, ?)',
                     (name, email, phone, age, city))
        conn.commit()
        conn.close()
        return redirect('/')
    if search:
        users = conn.execute('SELECT * FROM users WHERE name LIKE ? OR email LIKE ? OR city LIKE ? ORDER BY id DESC',
                             (f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    else:
        users = conn.execute('SELECT * FROM users ORDER BY id DESC').fetchall()
    total = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    cities = conn.execute('SELECT COUNT(DISTINCT city) FROM users').fetchone()[0]
    conn.close()
    return render_template('index.html', users=users, total=total, cities=cities, search=search)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        age = request.form['age']
        city = request.form['city']
        conn.execute('UPDATE users SET name=?, email=?, phone=?, age=?, city=? WHERE id=?',
                     (name, email, phone, age, city, id))
        conn.commit()
        conn.close()
        return redirect('/')
    conn.close()
    return render_template('edit.html', user=user)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')
