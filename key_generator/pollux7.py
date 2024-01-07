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


def generate(message: str) -> str:
    """Function that generates a key from a given message"""
    # check message format
    if message == '':
        return "Pas de mot(s) a rechercher fourni(s)"

    # extract the list from the message to a list
    message = utils.clean_message(message)

    # check if the list contains 7
    if len(message) != 7:
        return "La liste doit contenir 7 coupes"

    for element in message:
        if not float(element):
            return "La liste doit contenir uniquement des nombres : " + str(element)

    # the list is valid, generate the key
    # Define the OpenSCAD script as a string clef_pollux7(8,0,8,6.5,3,4,3);
    openscad_script = '''
use <clef_pollux7.scad>;
clef_pollux7({},{},{},{},{},{},{});'''.format(message[0], message[1], message[2],
                                                                   message[3], message[4], message[5], message[6])
    # delete the previous key
    if "pollux7_file.stl" in os.listdir():
        os.remove("pollux7_file.stl")

    # Write the OpenSCAD script to a file
    with open('generate_pollux7.scad', 'w') as file:
        file.write(openscad_script)

    # Generate the key
    subprocess.run([openscad_path, '-o', 'pollux7_file.stl', 'generate_pollux7.scad'])

    # if file name does not exist, there was an error during the generation
    if "pollux7_file.stl" not in os.listdir():
        return "Erreur lors de la génération de la clef"

    return "pollux7_file.stl"