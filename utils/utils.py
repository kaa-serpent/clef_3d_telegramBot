
def clean_message(message):
    # extract the list from the message to a list
    message = message.replace(' ', '')
    message = message.replace('[', '')
    message = message.replace(']', '')
    message = message.replace('(', '')
    message = message.replace(')', '')
    message = message.replace('{', '')
    message = message.replace('}', '')
    message = message.split(',')
    return message