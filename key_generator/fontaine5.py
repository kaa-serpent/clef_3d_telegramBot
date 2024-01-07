import subprocess
import os
import json
import platform

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
    message = message.replace(' ', '')
    message = message.replace('[', '')
    message = message.replace(']', '')
    message = message.split(',')

    # check if the list contains 5 elements or 6 and protected
    if len(message) != 5:
        if len(message) == 6:
            if message[5].lower() != 'protected':
                return "La liste doit contenir 5 coupes protected"
        return "La liste doit contenir 5 coupes"

    # check if the list contains only numbers
    for element in message:
        if not element.isnumeric():
            return "La liste doit contenir uniquement des nombres"

    # check if the list contains only numbers between 0 and 10
    for element in message:
        if float(element) < 0 or float(element) > 10:
            return "La liste doit contenir uniquement des nombres entre 0 et 10"

    # the list is valid, generate the key
    # Define the OpenSCAD script as a string clef_fontaine(8,0,8,6.5,3, protected=true);
    if len(message) == 6:
        if message[5].lower() == 'protected':
            message[5] = 'true'
            openscad_script = '''
                use <clef_fontaine.scad>;
                clef_fontaine({},{},{},{},{}, protected={});'''.format(message[0], message[1], message[2],
                                                                       message[3], message[4], message[5])
    else:
        openscad_script = '''
use <clef_fontaine.scad>;
clef_fontaine({},{},{},{},{});'''.format(message[0], message[1], message[2],
                                                                   message[3], message[4])
    # delete the previous key
    if "fontaine5_file.stl" in os.listdir():
        os.remove("fontaine5_file.stl")

    # Write the OpenSCAD script to a file
    with open('generate_fontaine.scad', 'w') as file:
        file.write(openscad_script)

    # Generate the key
    subprocess.run(['C:\\Program Files (x86)\\OpenSCAD\\openscad.exe', '-o', 'fontaine5_file.stl', 'generate_fontaine.scad'])

    # if file name does not exist, there was an error during the generation
    if "fontaine5_file.stl" not in os.listdir():
        return "Erreur lors de la génération de la clef"

    return "fontaine5_file.stl"