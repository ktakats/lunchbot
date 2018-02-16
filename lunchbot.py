import os
import time
import re
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
lunchbot_id = None
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
#Keeps track if it's time to collect answers or not
COLLECTING = False
COMMANDS = ["help", "start", "in", "stop"]
LUNCHERS = []

def parse_commands(slack_events, lunchbot_id):
    """
    Looks for message events, and if they are addressed to the bot returns the message and the channel id.
    """
    for event in slack_events:
        if event["type"]=="message" and not "subtype" in event:
            user_id, msg = parse_direct_mention(event["text"])
            if user_id == lunchbot_id:
                return msg, event["channel"], event['user']
    return None, None, None

def parse_direct_mention(msg_text):
    """
    Separates the mention id and the rest of the message text.
    """
    matches = re.search(MENTION_REGEX, msg_text)
    if matches:
        return (matches.group(1), matches.group(2).strip())
    return (None, None)

def handle_command(command, channel, user):
    """
    Gets the response from the respond_command function, and sends the answer.
    """
    global COLLECTING
    response, COLLECTING = respond_command(command, user, COLLECTING)
    if response:
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )

def respond_command(command, user, COLLECTING):
    """
    Returns a response to be forwarded to slack depending on the received command.
    """
    response = None
    global LUNCHERS
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
            if user not in LUNCHERS:
                LUNCHERS.append(user)
        else:
            response = "It's not lunchtime yet."
    elif command == COMMANDS[3]:
        COLLECTING = False
        response = "Time to make groups"
    return response, COLLECTING

def main():
    """
    Connects to slack, obtains the bot id and listens for events.
    """
    if slack_client.rtm_connect(with_team_state=False):
        print("Bot is connected and running!")
        lunchbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel, user = parse_commands(slack_client.rtm_read(), lunchbot_id)
            if command:
                handle_command(command, channel, user)
            time.sleep(1)
    else:
        print("Connection failed!")

if __name__=="__main__":
    main()
