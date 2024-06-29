import pandas as pd
import openai
import os

# Define your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def read_csv(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            return df
        except pd.errors.EmptyDataError:
            print("The CSV file is empty.")
    else:
        print("The file does not exist.")
    return None

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following journal entry:\n\n{text}"}
        ]
    )
    summary = response['choices'][0]['message']['content']
    return summary

def commentsummary():
    # File path to the CSV file
    file_path = os.path.join('data', 'journal_entries.csv')

    # Read the CSV file
    df = read_csv(file_path)
    if df is not None:
        # Sort the DataFrame by date
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date', ascending=False)

        # Iterate over each entry and summarize
        for index, row in df.iterrows():
            entry_text = row['entry']
            print(f"Original Entry:\n{entry_text}\n")
            
            summary = summarize_text(entry_text)
            print(f"Summary:\n{summary}\n")
            print("="*80)
