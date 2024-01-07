from utils import utils


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


# Define the translation table
translation_table = [
    [3, 2, 9, 8, 1, 5, 6, 2, 2, 8],
    [1, 4, 7, 2, 7, 2, 9, 1, 9, 0],
    [5, 3, 6, 1, 5, 7, 1, 0, 8, 1],
    [9, 5, 1, 7, 9, 4, 2, 8, 0, 7],
    [2, 0, 5, 5, 3, 3, 4, 3, 5, 9],
    [4, 8, 2, 6, 6, 1, 3, 4, 3, 3],
    [7, 1, 3, 4, 2, 6, 8, 5, 1, 2]
]

# Example cut input
cut_input = [6, 1, 2, 6, 5, 4, 0, 1, 3, 3]
code_input = [7, 4, 6, 4, 6, 3, 6, 1, 0, 7]


def decode(message: str) -> str:
    listmes = utils.clean_message(message)
    # check len to check id code or cut
    if len(listmes) == 10:
        # code to cut
        listmes.pop()
        resultlist = translate_code_to_cut(listmes, translation_table)
        code = "Le code de coupe est : " + str(resultlist)
    elif len(listmes) == 9:
        # cut to code
        resultlist = translate_code_to_cut(code_input, translation_table)
        code = "Le numéro de carte de propiétée est : " + str(resultlist)
    else:
        code = "Vérifiez la syntaxe je n'ai pas compris votre message."
    return code
