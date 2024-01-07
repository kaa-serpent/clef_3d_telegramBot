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

    # check if the list contains only numbers
    for element in message:
        if not element.isnumeric():
            return "La liste doit contenir uniquement des nombres"

    # check if the list contains only numbers between 0 and 10
    for element in message:
        if not float(element):
            return "La liste doit contenir uniquement des nombres : " + str(element)

    # the list is valid, generate the key
    # Define the OpenSCAD script as a string clef_dynaxis(8,0,8,6.5,3,4,3);
    openscad_script = '''
use <clef_dynaxis.scad>;
clef_dynaxis({},{},{},{},{},{},{});'''.format(message[0], message[1], message[2],
                                                                   message[3], message[4], message[5], message[6])
    # delete the previous key
    if "dynaxis_file.stl" in os.listdir():
        os.remove("dynaxis_file.stl")

    # Write the OpenSCAD script to a file
    with open('generate_dynaxis.scad', 'w') as file:
        file.write(openscad_script)

    # Generate the key
    subprocess.run([openscad_path, '-o', 'dynaxis_file.stl', 'generate_dynaxis.scad'])

    # if file name does not exist, there was an error during the generation
    if "dynaxis_file.stl" not in os.listdir():
        return "Erreur lors de la génération de la clef"

    return "dynaxis_file.stl"