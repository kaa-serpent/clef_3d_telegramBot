import shutil
import time
import requests
import json
import os
import platform
import utils.telegram_bot as bot
import key_generator.fontaine5 as fontaine5
from code_decoder import abloy_code
from key_generator import pollux7, pollux5, dynaxis

# get credential from json file
with open('credentials.json') as f:
    data = json.load(f)
    BOT_TOKEN = data['BOT_TOKEN']

with open('paths.json') as json_file:
    paths = json.load(json_file)

current_os = platform.system()
s = requests.Session()

# Copy scad_modules to OpenSCAD library folder
scad_modules_folder = 'scad_modules'
if current_os.lower() == 'windows':
    openscad_library_folder = os.path.join(os.path.expanduser('~'), 'Documents', 'OpenSCAD', 'libraries')
else:
    openscad_library_folder = os.path.join(os.path.expanduser('~'), '.local', 'share', 'OpenSCAD', 'libraries')

# Ensure the destination folder exists
os.makedirs(openscad_library_folder, exist_ok=True)

# Copy files and overwrite if they already exist
for file_name in os.listdir(scad_modules_folder):
    source_file = os.path.join(scad_modules_folder, file_name)
    destination_file = os.path.join(openscad_library_folder, file_name)
    # Check if the item is a file before copying
    if os.path.isfile(source_file):
        shutil.copy2(source_file, destination_file)


def chatbot():
    """
    Function that retrieves the latest requests from users in a Telegram group,
    generates a response, and sends the response back to the group.
    """
    cwd = os.getcwd()
    filename = cwd + '/lastupdate.txt'
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("1")
    # else:
       # print(".")

    with open(filename) as f:
        last_update = f.read()

    # Check for new messages in Telegram group
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update}'

    try:
        response = requests.get(url)
    except NameError:
        # network error
        print("Potential network error : " + NameError)
        return "done"

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

                    print('- - - - -')
                    text = result['message']['text']
                    print(result['message']['from']['first_name'] + " : " + text)

                    if '/help' in text or '/start' in text:
                        bot_response = "*Hello c'est Clefmentine un bot pour aider avec les clefs* \n\n " \
                                       "`/genhelp` Liste les differentes clef possible de générer et leurs commande pour les générer \n\n" \
                                       "`/codehelp` Liste les code disponible à traduire de code de coupe à carte de propiétée \n\n "
                        bot.telegram_bot_sendtext(bot_response, chat_id, msg_id)

                    elif '/genhelp' in text:
                        bot_response = "`/fontaine5 help`\n" \
                                       "`/dynaxis help`\n" \
                                       "`/pollux5 help`\n" \
                                       "`/pollux7 help`\n" \
                                       "- plus de générateurs de clefs a venir et des photos d'illustrations\n\n"
                        bot.telegram_bot_sendtext(bot_response, chat_id, msg_id)

                    elif '/codehelp' in text:
                        bot_response = "`/abloycode` code de coupe d'un clef abloy (protect, disclock etc...)\n " \
                                       "- plus de codes disponible prochainement\n\n"
                        bot.telegram_bot_sendtext(bot_response, chat_id, msg_id)

                    elif '/fontaine5' in text:
                        result = fontaine5.generate(text.replace("/fontaine5", ""), bot, chat_id, msg_id)
                        # if result contains "fontaine5" then it is a valid response
                        if 'fontaine5_file.stl' in result:
                            bot.send_one_stl(result, chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    elif '/dynaxis' in text:
                        result = dynaxis.generate(text.replace("/dynaxis", ""), bot, chat_id, msg_id)
                        if 'dynaxis_file.stl' in result:
                            bot.send_one_stl(result, chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    elif '/pollux7' in text:
                        result = pollux7.generate(text.replace("/pollux7", ""), bot, chat_id, msg_id)
                        if 'pollux7_file.stl' in result:
                            bot.send_one_stl(result, chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    elif '/pollux5' in text:
                        result = pollux5.generate(text.replace("/pollux5", ""), bot, chat_id, msg_id)
                        if 'pollux5_file.stl' in result:
                            bot.send_one_stl(result, chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    elif '/cavith' in text:
                        result = pollux7.generate(text.replace("/cavith", ""))
                        if 'cavith_file.stl' in result:
                            bot.send_one_stl(result, chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    elif '/abloycode' in text:
                        result = abloy_code.decode(text.replace("/abloycode", ""), bot, chat_id, msg_id)
                        if result == "code_decoder/abloy/disc_decode_final_font.png":
                            bot.telegram_bot_sendimage("code_decoder/abloy/disc_decode_final_font.png", chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    elif '/dislock' in text:
                        result = abloy_code.decode(text.replace("/dislock", ""), bot, chat_id, msg_id)
                        if "abloy_dislock_pro.stl" in result:
                            bot.send_one_stl(result, chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    else:
                        bot.telegram_bot_sendtext("Commande non reconnue. \n `/help`", chat_id, msg_id)

        except Exception as e:
            print(e)

    # Updating file with last update ID
    with open(filename, 'w') as f:
        f.write(last_update)

    return "done"


def main():
    """Function that runs the Chatbot function every 5 seconds unless it is in call"""
    while True:
        chatbot()
        time.sleep(5)


if __name__ == "__main__":
    main()
