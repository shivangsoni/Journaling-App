import pandas as pd
import openai
import os
from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
import uuid

# Import the commentsummary function from journal_summarizer using relative import
from .journal_summarizer import commentsummary

main = Blueprint('main', __name__)

CSV_FILE = os.path.join('data', 'journal_entries.csv')

@main.route('/')
def index():
    entries = []
    active_date = request.args.get('date', None)

    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        try:
            df = pd.read_csv(CSV_FILE)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date', ascending=False)
            entries = df.to_dict('records')
        except pd.errors.EmptyDataError:
            entries = []

    grouped_entries = {}
    for entry in entries:
        date = entry['date'].strftime('%Y-%m-%d')
        if date not in grouped_entries:
            grouped_entries[date] = []
        grouped_entries[date].append(entry)

    return render_template('index.html', grouped_entries=grouped_entries, active_date=active_date)

@main.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        entry_text = request.form['entry']
        mood = request.form['mood']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_entry(entry_text, mood, date)
        return redirect(url_for('main.index'))
    return render_template('entry.html')

@main.route('/entry/<string:entry_id>', methods=['GET'])
def view_entry(entry_id):
    entry = None
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        try:
            df = pd.read_csv(CSV_FILE)
            entry = df[df['id'] == entry_id].to_dict('records')
            entry = entry[0] if entry else None
        except pd.errors.EmptyDataError:
            entry = None
    return render_template('view_entry.html', entry=entry)

@main.route('/delete/<string:entry_id>', methods=['POST'])
def delete(entry_id):
    entry_date = None
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        try:
            df = pd.read_csv(CSV_FILE)
            entry = df[df['id'] == entry_id].to_dict('records')
            if entry:
                entry_date = entry[0]['date'].split()[0]
            df = df[df['id'] != entry_id]
            df.to_csv(CSV_FILE, index=False)
        except pd.errors.EmptyDataError:
            pass
    return redirect(url_for('main.index', date=entry_date))

@main.route('/summary')
def summary():
    summary_data = {}
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        try:
            df = pd.read_csv(CSV_FILE)
            summary_data = commentsummary().to_dict()##df.groupby('mood').size().to_dict()
        except pd.errors.EmptyDataError:
            summary_data = {}
    return render_template('summary.html', summary_data=summary_data)

@main.route('/recommendations')
def recommendations():
    recommendations_list = [
        "Write more consistently.",
        "Focus on positive events.",
        "Reflect on your entries to find patterns.",
        "Try journaling at the same time each day."
    ]
    return render_template('recommendations.html', recommendations=recommendations_list)

def save_entry(entry_text, mood, date):
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['id', 'entry', 'mood', 'date'])
        df.to_csv(CSV_FILE, index=False)
    
    unique_id = str(uuid.uuid4())
    new_entry = pd.DataFrame({'id': [unique_id], 'entry': [entry_text], 'mood': [mood], 'date': [date]})
    new_entry.to_csv(CSV_FILE, mode='a', header=False, index=False)
