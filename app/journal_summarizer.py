import asyncio
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

def save_csv(file_path, data):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

async def summarize_text(text):
    messages = [
        {"role": "system", "content": "You are a helpful journaling assistant."},
        {"role": "user", "content": f"Summarize the following journal entries:\n\n{text}"}
    ]

    client = openai.AsyncOpenAI()
    response = await client.chat.completions.create(model="gpt-4", messages=messages,temperature=0)
    summary = response.choices[0].message.content
    return summary

async def recommend_text(text):
    messages = [
        {"role": "system", "content": "You are a helpful journaling assistant."},
        {"role": "user", "content": f"Recommend ways to improve and create a detailed action plan with tracking steps:\n\n{text}"}
    ]

    client = openai.AsyncOpenAI()
    response = await client.chat.completions.create(model="gpt-4", messages=messages,temperature=0)
    summary = response.choices[0].message.content
    return summary

async def commentsummary_async(entries=None):
    if entries != None:
        return [{'recommend':await recommend_text(entries)}]
    
    summaries = []
    if entries is None:
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
                summary = await summarize_text(entry_text)
                summaries.append({'summary': summary})
            final_summary = await summarize_text(summaries)
            final_sum = [{'summary':final_summary}]
            save_csv(os.path.join('data', 'summary.csv'), final_sum)
            print(final_sum)
    return final_sum

def commentsummary(entries=None):
    return asyncio.run(commentsummary_async(entries))
