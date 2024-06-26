from flask import Blueprint, render_template, request
import sqlite3
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        entry_text = request.form['entry']
        mood = request.form['mood']
        save_entry(entry_text, mood)
    return render_template('entry.html')

def save_entry(entry_text, mood):
    db_path = os.path.join('data', 'journal_entries.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY AUTOINCREMENT, entry TEXT, mood TEXT)''')
    cursor.execute('INSERT INTO entries (entry, mood) VALUES (?, ?)', (entry_text, mood))
    conn.commit()
    conn.close()
