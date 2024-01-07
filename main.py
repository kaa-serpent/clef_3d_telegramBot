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
    else:
        print("last message id file exists.")

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
                        bot_response = "*Hello c'est Clefmentine un bot pour aider avec les clefs* \n\n " \
                                       "-`/genhelp` Liste les differentes clef possible de générer et leurs commande pour les générer \n" \
                                       "-`/codehelp` Liste les code disponible à traduire de code de coupe à carte de propiétée \n "
                        print(bot.telegram_bot_sendtext(bot_response, chat_id, msg_id))

                    if '/genhelp' in result['message']['text']:
                        bot_response = "-```/fontaine5``` Génération d'une clef fontaine 5 aillettes 3d donner les profondeurs des coupes [1,2,3,4,5] dans le sens horraire, 1 est en bas à gauche, séparez les chiffres par des virgules \n " \
                                       "-```/dynaxis``` Génération d'une clef dynaxis 7 aillettes 3d donner les profondeurs des coupes [1,2,3,4,5,6,7 en mm] dans le sens horraire, 1 est en bas à gauche, séparez les chiffres par des virgules\n " \
                                       "- plus de générateurs de clefs a venir et des photos d'illustrations\n\n"
                        print(bot.telegram_bot_sendtext(bot_response, chat_id, msg_id))

                    if '/codehelp' in result['message']['text']:
                        bot_response = "- ```/abloycode``` Traduction du code de coupe d'un clef abloy (protect, disclock etc...) à un code de carte de propiétée ou vise versa. fournir une liste de 10 chiffres ex: [6,1,2,6,5,4,0,1,3,3], pour obtenir les coupes depuis la carte de proprietée ajouter `carte` à la fin de la liste ex: \n`/abloycode 6,1,2,6,5,4,0,1,3,3` \n`/abloycode 7,4,6,4,6,3,6,1,0,7,carte` \n\n " \
                                       "- plus de codes disponible prochainement\n\n"
                        print(bot.telegram_bot_sendtext(bot_response, chat_id, msg_id))

                    print(result['message']['text'])

                    if '/fontaine5' in result['message']['text']:
                        result = fontaine5.generate(result['message']['text'].replace("/fontaine5", ""))
                        # if result contains "fontaine5" then it is a valid response
                        if 'fontaine5_file.stl' in result:
                            bot.send_one_stl(result, chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    if '/dynaxis' in result['message']['text']:
                        result = dynaxis.generate(result['message']['text'].replace("/dynaxis", ""))
                        if 'dynaxis_file.stl' in result:
                            bot.send_one_stl(result, chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    if '/pollux7' in result['message']['text']:
                        result = pollux7.generate(result['message']['text'].replace("/pollux7", ""))
                        if 'pollux7_file.stl' in result:
                            bot.send_one_stl(result, chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    if '/pollux5' in result['message']['text']:
                        result = pollux5.generate(result['message']['text'].replace("/pollux5", ""))
                        if 'pollux5_file.stl' in result:
                            bot.send_one_stl(result, chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    if '/cavith' in result['message']['text']:
                        result = pollux7.generate(result['message']['text'].replace("/cavith", ""))
                        if 'cavith_file.stl' in result:
                            bot.send_one_stl(result, chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

                    if '/abloycode' in result['message']['text']:
                        result = abloy_code.decode(result['message']['text'].replace("/abloycode", ""))
                        if result == "code_decoder/abloy/disc_decode_final_font.png":
                            bot.telegram_bot_sendimage("code_decoder/abloy/disc_decode_final_font.png", chat_id, msg_id)
                        else:
                            bot.telegram_bot_sendtext(result, chat_id, msg_id)

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
