import pandas as pd
from datetime import datetime, timedelta
import pytz
from slack_sdk import WebClient
import os
import requests
import logging

#TODO: Post an update Sunday night with the upcoming birthdays for the week
#TODO: Automatically update it's own birthday list by scraping the website
#TODO: write with customized appearance
#TODO: react to everything in the channel with emojis

# Setup logging
logging.basicConfig(level=logging.INFO)

class GPTError(Exception):
    pass

PROMPT = """Today is {date}. {first_name} {last_name} is turning a year older. 
Wish them a happy birthday! Keep your response short and sweet. Don't include their 
age in the message in case they are sensitive about it. You post a birthday message every 
few days so make each message unique. Do things like include emojis, 
write a short poem, or make a joke."""

def get_gpt_message(first_name, last_name, date):
    prompt = PROMPT.format(date=date.strftime('%B %d'), first_name=first_name, last_name=last_name)
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        logging.error(f"Error with OpenAI API: {response.status_code} - {response.text}")
        raise GPTError("Error with OpenAI API")
    return response.json()['choices'][0]['message']['content']

def send_slack_message(client, channel, text):
    client.chat_postMessage(channel=channel, text=text)

def prepare_data():
    data = pd.read_csv('birthdays.csv', parse_dates=['Date'], dayfirst=True)
    data['Date'] = pd.to_datetime(data['Date'] + ' ' + str(datetime.now().year), format='%d %b %Y')
    data[['Last Name', 'First Name']] = data['Name'].str.split(', ', expand=True) #TODO: this leaves middle names attached to first names
    return data

def check_for_birthdays(date=None):
    data = prepare_data()
    utah = pytz.timezone('America/Denver')
    date = date or datetime.now(utah).date()
    todays_birthdays = data[(data['Date'].dt.month == date.month) & (data['Date'].dt.day == date.day)]
    if todays_birthdays.empty:
        logging.info(f"No birthdays on {date}")
        return
    
    slack_token = os.environ['SLACK_BOT_TOKEN']
    client = WebClient(token=slack_token)
    channel = 'C03S8HDLWK1' if os.environ['env'] == 'production' else 'C0621KYQ09M'

    for _, row in todays_birthdays.iterrows():
        try:
            message = get_gpt_message(row['First Name'], row['Last Name'], row['Date'])
        except GPTError:
            message = f"Happy Birthday to {row['First Name']} {row['Last Name']}! 🎂"
            logging.error("Error in getting GPT message, using default message")
        send_slack_message(client, channel, message)
        logging.info(f"Sent message to {row['First Name']} {row['Last Name']}")
        
def lambda_handler(event, context):
    test = event.get('test', None)
    if test:
        for i in range(1, 8):
            check_for_birthdays(datetime.now() + timedelta(days=i))
    else:
        check_for_birthdays()

if __name__ == "__main__":
    check_for_birthdays()
    
    