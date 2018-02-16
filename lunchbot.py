import os
import time
import re
from slackclient import SlackClient
from commands import respond_command

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
lunchbot_id = None
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
#Keeps track if it's time to collect answers or not
COLLECTING = False

def parse_commands(slack_events, lunchbot_id):
    """
    Looks for message events, and if they are addressed to the bot returns the message and the channel id.
    """
    for event in slack_events:
        if event["type"]=="message" and not "subtype" in event:
            user_id, msg = parse_direct_mention(event["text"])
            if user_id == lunchbot_id:
                return msg, event["channel"]
    return None, None

def parse_direct_mention(msg_text):
    """
    Separates the mention id and the rest of the message text.
    """
    matches = re.search(MENTION_REGEX, msg_text)
    if matches:
        return (matches.group(1), matches.group(2).strip())
    return (None, None)

def handle_command(command, channel):
    """
    Gets the response from the respond_command function, and sends the answer.
    """
    response, COLLECTING = respond_command(command, COLLECTING)
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


def main():
    """
    Connects to slack, obtains the bot id and listens for events.
    """
    if slack_client.rtm_connect(with_team_state=False):
        print("Bot is connected and running!")
        lunchbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_commands(slack_client.rtm_read(), lunchbot_id)
            if command:
                handle_command(command, channel)
            time.sleep(1)
    else:
        print("Connection failed!")

if __name__=="__main__":
    main()
