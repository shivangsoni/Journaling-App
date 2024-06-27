from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
import os
from datetime import datetime

main = Blueprint('main', __name__)

CSV_FILE = os.path.join('data', 'journal_entries.csv')

@main.route('/')
def index():
    entries = []
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        entries = df.to_dict('records')

    # Group entries by date
    grouped_entries = {}
    for entry in entries:
        date = entry['date']
        if date not in grouped_entries:
            grouped_entries[date] = []
        grouped_entries[date].append(entry)

    return render_template('index.html', grouped_entries=grouped_entries)

@main.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        entry_text = request.form['entry']
        mood = request.form['mood']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_entry(entry_text, mood, date)
        return redirect(url_for('main.index'))
    return render_template('entry.html')

@main.route('/entry/<int:entry_id>', methods=['GET'])
def view_entry(entry_id):
    if os.path.exists(CSV_FILE):
        entries = pd.read_csv(CSV_FILE)
        entry = entries.iloc[entry_id].to_dict()
    else:
        entry = None
    return render_template('view_entry.html', entry=entry)

@main.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = df.drop(df.index[entry_id])
        df.to_csv(CSV_FILE, index=False)
    return redirect(url_for('main.index'))

@main.route('/summary')
def summary():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        summary_data = df.groupby('mood').size().to_dict()
    else:
        summary_data = {}
    return render_template('summary.html', summary_data=summary_data)

@main.route('/recommendations')
def recommendations():
    # Placeholder recommendations
    recommendations_list = [
        "Write more consistently.",
        "Focus on positive events.",
        "Reflect on your entries to find patterns.",
        "Try journaling at the same time each day."
    ]
    return render_template('recommendations.html', recommendations=recommendations_list)

def save_entry(entry_text, mood, date):
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['entry', 'mood', 'date'])
        df.to_csv(CSV_FILE, index=False)
    
    new_entry = pd.DataFrame({'entry': [entry_text], 'mood': [mood], 'date': [date]})
    new_entry.to_csv(CSV_FILE, mode='a', header=False, index=False)
