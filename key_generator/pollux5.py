import subprocess
import os
import json
import platform

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
        bot.telegram_bot_sendimage("key_generator/help/pollux5.jpg", chat_id, msg_id)
        return " Génération d'une clef pollux 5 aillettes 3d\n" \
               "donnez les profondeurs des coupes [1,2,3,4,5 en mm] dans le sens horraire, 1 est en bas à gauche\n" \
               "séparez les chiffres par des virgules\n" \
               "exemple :\n /pollux5 1,5,4,3,4,2,7"

    # extract the list from the message to a list
    message = utils.clean_message(message)

    # check if the list contains 5 elements or 6 and protected
    if len(message) != 5:
        if len(message) == 6:
            if message[5].lower() != 'protected':
                return "La liste doit contenir 5 coupes protected"
        return "La liste doit contenir 5 coupes"

    for element in message:
        if not float(element) or element == 0:
            return "La liste doit contenir uniquement des nombres : " + str(element)

    # the list is valid, generate the key
    # Define the OpenSCAD script as a string clef_fontaine(8,0,8,6.5,3, protected=true);
    if len(message) == 6:
        if message[5].lower() == 'protected':
            message[5] = 'true'
            openscad_script = '''
                use <clef_pollux5.scad>;
                clef_pollux5({},{},{},{},{}, protected={});'''.format(message[0], message[1], message[2],
                                                                       message[3], message[4], message[5])
    else:
        openscad_script = '''
use <clef_pollux5.scad>;
clef_pollux5({},{},{},{},{});'''.format(message[0], message[1], message[2],
                                                                   message[3], message[4])
    # delete the previous key
    if "pollux5_file.stl" in os.listdir():
        os.remove("pollux5_file.stl")

    # Write the OpenSCAD script to a file
    with open('generate_pollux5.scad', 'w') as file:
        file.write(openscad_script)

    # Generate the key
    subprocess.run([openscad_path, '-o', 'pollux5_file.stl', 'generate_pollux5.scad'])

    # if file name does not exist, there was an error during the generation
    if "pollux5_file.stl" not in os.listdir():
        return "Erreur lors de la génération de la clef"

    return "pollux5_file.stl"