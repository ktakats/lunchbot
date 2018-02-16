import os
import time
import re
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
lunchbot_id = None
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_commands(slack_events, lunchbot_id):
    print(slack_events)
    for event in slack_events:
        if event["type"]=="message" and not "subtype" in event:
            user_id, msg = parse_direct_mention(event["text"])
            print(user_id, lunchbot_id)
            print(user_id == lunchbot_id)
            if user_id == lunchbot_id:
                print(msg)
                return msg, event["channel"]
    return None, None

def parse_direct_mention(msg_text):
    matches = re.search(MENTION_REGEX, msg_text)
    if matches:
        return (matches.group(1), matches.group(2).strip())
    return (None, None)

def handle_command(command, channel):
    default_response = "I don't understand."
    response = None
    if command.startswith("do"):
        response = "Yay"
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


def main():
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
