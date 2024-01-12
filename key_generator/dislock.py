import subprocess
import os
import json
import platform
import time

from utils import utils

with open('paths.json') as json_file:
    paths = json.load(json_file)

current_os = platform.system()

# Select the appropriate path based on the operating system
openscad_path = paths.get(f"{current_os.lower()}_path_openscad", None)


def generate(message: str, bot, chat_id, msg_id) -> str:
    """Function that generates a key from a given message"""
    # check message format

    if 'help' in message or message == '':
        bot.telegram_bot_sendimage("key_generator/help/abloy_dislock.jpg", chat_id, msg_id)
        return " Génération d'une abloy dislock / dislock pro 3d\n" \
               "donnez les coupes de 1 à 11\n" \
               "exemple :\n /dislock 01234560543\n" \
               "La génération peut prendre plusieurs minutes merci de patienter\n"

    message = message.replace(' ', '')
    message = list(message)

    # check if the list contains 11
    if len(message) != 11:
        return "La liste doit contenir 11 coupes"

    message = [int(element) for element in message]
    if not [isinstance(element, int) for element in message]:
        return "La liste doit contenir uniquement des chiffres"

    # the list is valid, generate the key
    # Define the OpenSCAD script as a string abloy_dislock_pro([0,1,2,3,4,5,6,0,5,4,3]);;
    openscad_script = '''use <abloy_dislock.scad>;
abloy_dislock_pro({});'''.format(message)

    # Write the OpenSCAD script to a file
    with open('generate_abloy_dislock_pro.scad', 'w') as file:
        file.write(openscad_script)

    # delete the previous key
    if "abloy_dislock_pro.stl" in os.listdir():
        os.remove("abloy_dislock_pro.stl")

    # Generate the key
    subprocess.run([openscad_path, '-o', 'abloy_dislock_pro.stl', 'generate_abloy_dislock_pro.scad'])

    # if file name does not exist, there was an error during the generation
    if "abloy_dislock_pro.stl" not in os.listdir():
        return "Erreur lors de la génération de la clef"

    return "abloy_dislock_pro.stl"