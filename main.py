import time
import requests
import json
import os
import utils.telegram_bot as bot
from utils import connect_locksport as locksport

# get credential from json file
with open('credentials.json') as f:
    data = json.load(f)
    BOT_TOKEN = data['BOT_TOKEN']
    LOCKSPORT_USERNAME = data['LOCKSPORT_USERNAME']
    LOCKSPORT_PASSWORD = data['LOCKSPORT_PASSWORD']

s = requests.Session()


def Chatbot():
    """
    Function that retrieves the latest requests from users in a Telegram group,
    generates a response, and sends the response back to the group.
    """
    cwd = os.getcwd()
    filename = cwd + '/lastupdate.txt'
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("1")
    else:
        print("File Exists")

    with open(filename) as f:
        last_update = f.read()

    # Check for new messages in Telegram group
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update}'
    response = requests.get(url)
    data = json.loads(response.content)

    for result in data['result']:
        try:
            # Checking for new message
            if float(result['update_id']) > float(last_update):
                # Checking for new messages that did not come from chatGPT
                if not result['message']['from']['is_bot']:
                    last_update = str(int(result['update_id']))
                    # Retrieving message ID of the sender of the request
                    msg_id = str(int(result['message']['message_id']))
                    # Retrieving the chat ID
                    chat_id = str(result['message']['chat']['id'])

                    if '/help' in result['message']['text']:
                        bot_response = "Hi, I am ChikaaGPT, I am a chatbot that uses OpenAI to generate responses. \n\n - /gpt generate a text response from me \n - /img generate an image from the provided text \n\n I am still learning so please be patient with me."
                        print(bot.telegram_bot_sendtext(bot_response, chat_id, msg_id))

                    if '/cle' or '/clef' or '/clé' in result['message']['text']:
                        prompt = result['message']['text'].replace("/cle", "").replace("/clef", "").replace("/clé", "")
                        result = locksport.search_on_locksport(prompt)
                        print(bot.telegram_bot_sendtext(result, chat_id, msg_id))

                    if 'lp' in result['message']['text']:
                        prompt = result['message']['text'].replace("lp", "")
                        bot_response = "https://www.youtube.com/@lockpickinglawyer/search?query=" + prompt
                        print(bot.telegram_bot_sendtext(bot_response, chat_id, msg_id))

                    # Checking if user wants an image
                    if '/img' in result['message']['text']:
                        prompt = result['message']['text'].replace("/img", "")
                        bot_response = openAImage(prompt)
                        print(bot.telegram_bot_sendimage(bot_response, chat_id, msg_id))

        except Exception as e:
            print(e)

    # Updating file with last update ID
    with open(filename, 'w') as f:
        f.write(last_update)

    return "done"


def main():
    """Function that runs the Chatbot function every 5 seconds unless it is in call"""
    while True:
        Chatbot()
        time.sleep(5)


if __name__ == "__main__":
    main()
