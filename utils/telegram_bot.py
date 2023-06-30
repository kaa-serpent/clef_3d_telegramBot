import json
import os

import requests

# read credential json
with open('credentials.json') as f:
    data = json.load(f)
    BOT_TOKEN = data['BOT_TOKEN']


def check_html_status_code(response_test, chat_id, msg_id):
    """Checks if the given response has a status code of 200."""
    if response_test.status_code != 200:
        print(f'Error: {response_test.status_code}')
        text_error_message = f'Error: {response_test.status_code}' + " " + f'{response_test.json()}'
        data_statue_check = {
            'chat_id': chat_id,
            'text': f'```{text_error_message}```',
            'reply_to_message_id': msg_id,
            'parse_mode': 'Markdown'
        }
        response = requests.post(
            'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage',
            params=data_statue_check,
        )
        response.json()


def prepare_message(message):
    clean_text = ''
    for line in message:
        if "->" in line:
            line = line.split("->")
            clean_text += line[0] + "->" + f'```\n{line[1]}\n```'
        else:
            clean_text += line
    return clean_text


def telegram_bot_sendtext(bot_message, chat_id, msg_id):
    """Function that sends a message to a specific telegram group"""
    clean_message = prepare_message(bot_message)
    data = {
        'chat_id': chat_id,
        'text': clean_message,
        'reply_to_message_id': msg_id,
        'parse_mode': 'Markdown'
    }
    response = requests.post(
        'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage',
        params=data,
    )
    check_html_status_code(response, chat_id, msg_id)
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


def send_screenshots(group_id, msg_id):
    """Function that sends screenshots located in the ./picture folder to a specific telegram group"""
    folder_path = './pictures'
    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendPhoto'

    image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if
                   file.endswith('.jpg') or file.endswith('.png')]

    # Iterate over the image files and send them to the chat
    for image_file in image_files:
        with open(image_file, 'rb') as f:
            response = requests.post(url, data={'chat_id': group_id}, files={'photo': f})
            check_html_status_code(response, group_id, msg_id)
            print(response.json())


def send_one_stl(stl_file_name, group_id, msg_id):
    """Function that sends the .stl file located to a specific telegram group"""
    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendDocument'

    with open(stl_file_name, 'rb') as f:
        response = requests.post(url, data={'chat_id': group_id}, files={'document': f})
        check_html_status_code(response, group_id, msg_id)
        print(response.json())
