import os
import time
import datetime
import re
import math
import random
from slackclient import SlackClient
import json

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
lunchbot_id = None
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
#Keeps track if it's time to collect answers or not
collecting = False
COMMANDS = ["help", "start", "in", "stop", "set", "unset"]
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
lunchers = []
channels = []
#Default autorun settings: Thursday at 10:00
AUTORUN = False
autorun_day = 3 #Thursday
autorun_hour = 10
autorun_minute = 0

def parse_commands(slack_events, lunchbot_id):
    """
    Looks for message events, and if they are addressed to the bot returns the message and the channel id.
    """
    for event in slack_events:
        if event["type"]=="message" and not "subtype" in event:
            user_id, msg = parse_direct_mention(event["text"])
            if user_id == lunchbot_id:
                if event['channel'] not in channels:
                    channels.append(event['channel'])
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
    global AUTORUN
    if command == "help":
        is_autorun = ""
        if AUTORUN:
            day=WEEKDAYS[autorun_day][0].upper()+WEEKDAYS[autorun_day][1:]
            is_autorun = "SET to {a}, {b}:{c}.\n".format(a=day, b=autorun_hour, c=autorun_minute)
        else:
            is_autorun = "NOT set.\n"
        response = """
        Available commands:\n
        start - starts collecting responses,\n
        in - signs up the user for lunch,\n
        stop - stops collecting responses and creates lunch groups,\n
        set - sets the bot to start at the default time, Thursday, 10:00.\n
        set DAY HOUR:MINUTE - sets the bot to start at given time. E.g. 'set Friday 11:00'.  Right now autorun is {d}.
        unset - Stops autorun. Now you have to start the bot with the start command.
        """.format(d=is_autorun)

    elif command == "start":
        collecting = True
        lunchers = []
        response = "Ey! who is going to have lunch out today? Say 'in' to join!"
    elif command == "in":
        if collecting==True:
            if user not in lunchers:
                lunchers.append(user)
        else:
            response = "It's not lunchtime yet."
    elif command == "stop":
        collecting = False
        groups = make_groups(lunchers)
        leaders=pick_leaders(groups)
        response = "The lunch groups are: \n"
        for i,group in enumerate(groups):
            response += "Group "+str(i)+ ": "
            for member in group:
                if member!=leaders[i]:
                    response += "<@"+member + ">, "
            response += "leader: <@"+leaders[i]+">"
            response +="\n"
    elif command.startswith("set"):
        AUTORUN = True
        d, h, m = set_autorun_time(command)
        d=WEEKDAYS[d]
        response = "Autorun set to: {d}, {h}:{m}".format(d=d[0].upper()+d[1:], h=h, m=m)
    elif command == "unset":
        AUTORUN = False
    else:
        response = "I don't understand. Type 'help' to see the available commands."
    return response, collecting, lunchers

def make_groups(lunchers):
    """
    Takes the list of the people that signed up for lunch, calculates the number of groups such as no group has more than 7 members, and each group is more or less the same size, then assignes the members to groups randomly. Returns a list of groups.
    """
    N=len(lunchers)
    num_groups = math.ceil(N/7.)
    groups=[]
    if num_groups==1:
        groups.append(lunchers)
    else:
        #Make random groups
        for i in range(num_groups):
            group=[]
            for j in range(int(N/num_groups)):
                if len(lunchers)>0:
                    random_index=random.randint(0,len(lunchers)-1)
                    group.append(lunchers.pop(random_index))
            groups.append(group)
    return groups

def pick_leaders(groups):
    """
    Takes the list of groups and randomly picks a leader for each group. Returns the list of leaders.
    """
    leaders = []
    for group in groups:
        leader = group[random.randint(0, len(group)-1)]
        leaders.append(leader)
    return leaders

def set_autorun_time(command):
    global autorun_day, autorun_hour, autorun_minute
    set_time = command.split(" ")
    if len(set_time)==3:
        if set_time[1].lower() in WEEKDAYS:
            try:
                time_details=set_time[2].split(":")
            except:
                time_details=[autorun_hour, autorun_minute]
            if len(time_details)==2:
                try:
                    hour = int(time_details[0])
                except:
                    hour = autorun_hour
                try:
                    minute = int(time_details[1])
                except:
                    minute = autorun_minute
                if hour>=0 and hour<23 and minute>=0 and minute<=59:
                    autorun_day = WEEKDAYS.index(set_time[1].lower())
                    autorun_hour = hour
                    autorun_minute = minute
    return autorun_day, autorun_hour, autorun_minute

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
            if AUTORUN==True and not collecting:
                now = datetime.datetime.now()
                if now.weekday()==autorun_day and now.hour==autorun_hour and now.minute==autorun_minute:
                    for channel in channels:
                        handle_command('start', channel, lunchbot_id)
            time.sleep(1)
    else:
        print("Connection failed!")

if __name__=="__main__":
    main()
