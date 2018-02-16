import os
import time
import re
import math
import random
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
lunchbot_id = None
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
#Keeps track if it's time to collect answers or not
collecting = False
COMMANDS = ["help", "start", "in", "stop"]
lunchers = []

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
    global collecting
    global lunchers
    response, collecting, lunchers = respond_command(command, user, collecting, lunchers)
    if response:
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )

def respond_command(command, user, collecting, lunchers):
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
        collecting = True
        lunchers = []
        response = "Ey! who is going to have lunch out today? Say 'in' to join!"
    elif command == COMMANDS[2]:
        if collecting==True:
            if user not in lunchers:
                lunchers.append(user)
        else:
            response = "It's not lunchtime yet."
    elif command == COMMANDS[3]:
        collecting = False
        groups = make_groups(lunchers)
        response = "The lunch groups are: \n"
        for i,group in enumerate(groups):
            response += "Group "+str(i)+ ": "
            for member in group:
                response += "<@"+member + "> ,"
            response +="\n"
    return response, collecting, lunchers

def make_groups(lunchers):
    N=len(lunchers)
    num_groups = math.ceil(N/7.)
    groups=[]
    print(groups)
    if num_groups==1:
        groups.append(lunchers)
    else:
        #Make random groups
        for i in range(num_groups):
            g=[]
            for j in range(int(N/num_groups)):
                if len(lunchers)>0:
                    random_index=random.randint(0,len(lunchers)-1)
                    g.append(lunchers.pop(random_index))
            groups.append(g)

    return groups

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
