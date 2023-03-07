import json
import requests

# read credential json
with open('credentials.json') as f:
    data = json.load(f)
    BOT_TOKEN = data['BOT_TOKEN']


def telegram_bot_sendtext(bot_message, chat_id, msg_id):
    """Function that sends a message to a specific telegram group"""
    data = {
        'chat_id': chat_id,
        'text': bot_message,
        'reply_to_message_id': msg_id,
        'parse_mode': 'Markdown'
    }
    response = requests.post(
        'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage',
        params=data,
    )
    return response.json()


def telegram_bot_sendimage(image_url, group_id, msg_id):
    """Function that sends an image to a specific telegram group"""
    data = {
        'chat_id': group_id,
        'photo': image_url,
        'reply_to_message_id': msg_id,
    }
    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendPhoto'

    response = requests.post(url, data=data)
    return response.json()
