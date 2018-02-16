COMMANDS = ["help", "start", "in", "stop"]
LUNCHERS = []

def respond_command(command, COLLECTING):
    """
    Returns a response to be forwarded to slack depending on the received command.
    """
    response = None
    if command not in COMMANDS:
        response = "I don't understand. Type 'help' to see the available commands."
    elif command == COMMANDS[0]:
        response = """
        Available commands:\n
        start - starts collecting responses,\n
        in - signs up the user for lunch,\n
        stop - stops collecting responses and creates lunch groups.
        """
    elif command == COMMANDS[1]:
        COLLECTING = True
        LUNCHERS = []
        response = "Ey! who is going to have lunch out today? Say 'in' to join!"
    elif command == COMMANDS[2]:
        if COLLECTING==True:
            response = "collecting"
        else:
            response = "It's not lunchtime yet."
    elif command == COMMANDS[3]:
        COLLECTING = False
        response = "Time to make groups"
    return response, COLLECTING
