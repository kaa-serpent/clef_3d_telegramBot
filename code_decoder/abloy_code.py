# made by Clefmentine january 2024
# I am not responsible for bad usage of this code, I shared it to prove a security flow in Abloy key copy system
# you can visually decode a key and ask the factory to make a new oe proving the right number for the property card
import json

card = False


def translate_cut_to_code(cut, table):
    code = []
    for index, i in enumerate(cut):
        # pick the i list from table and the same index
        code.append(table[i][index])
    return code


def translate_code_to_cut(code, table):
    cut = []
    for index, digit in enumerate(code):
        # Find the index of the digit in the corresponding list of the table
        for ind, i in enumerate(table):
            if i[index] == digit:
                cut.append(ind)
    return cut


# Read the JSON data from the file
with open("abloy/table.json", 'r') as json_file:
    data = json.load(json_file)
    translation_table = data['table']


def decode(message: str, bot, chat_id, msg_id) -> str:
    if 'help' in message or '' in message:
        result = "Permet de passer du code de coupe au code de la carte de propiétée ou vise versa \n" \
                 "Ajouer `carte` à la suite permet de passer du code de la carte de propietée au code de coupe\n" \
                 "ex:\n`/abloycode 6126540133` \n `/abloycode 7464636107 carte` \n\n"
        bot.telegram_bot_sendtext(result, chat_id, msg_id)
        # send picture of key cut
        return "code_decoder/abloy/disc_decode_final_font.png"

    message = message.replace(' ', '')

    if 'carte' in message:
        card = True
        message = message.replace("carte", "")

    message = list(message)

    # check if the list contains 11
    if len(message) == 11:
        message = message.pop(0)
        listmes = list(map(int, message))
        if card:
            resultlist = translate_cut_to_code(listmes, translation_table)
            code = "Le numéro de carte de propiétée est : 0" + str(resultlist)
        else:
            resultlist = translate_code_to_cut(listmes, translation_table)
            code = "Les coupes de la clef sont : 0" + str(resultlist)

    else:
        result = "Permet de passer du code de coupe au code de la carte de propiétée ou vise versa \n" \
                 "Ajouer `carte` à la suite permet de passer du code de la carte de propietée au code de coupe\n" \
                 "ex:\n`/abloycode 6126540133` \n `/abloycode 7464636107 carte` \n\n"
        bot.telegram_bot_sendtext(result, chat_id, msg_id)
        # send picture of key cut
        return "code_decoder/abloy/disc_decode_final_font.png"

    return code


if __name__ == "__main__":
    # Example cut input
    cut_input = [5, 3, 5, 3, 1, 2, 0, 2, 6, 4]
    # code_input = [7, 4, 6, 4, 6, 3, 6, 1, 0, 7]
    print(translate_cut_to_code(cut_input, translation_table))
