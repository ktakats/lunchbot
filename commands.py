COMMANDS = ["help", "start", "in", "stop"]

def respond_command(command):
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
    return response
