import pytest
from lunchbot import parse_commands, handle_command, make_groups, pick_leaders
from lunchbot import respond_command
import random
import math

LUNCHBOT_ID = "U123"
CHANNEL_ID ="C999999"
USER_ID = "U987"

class TestCommandParser(object):

    def test_no_event_returns_none(self):
        events=[]
        command, channel, user = parse_commands(events, "<@U123>")
        assert command is None
        assert channel is None

    def test_event_returns_not_none(self):
        events = [{'type': 'message', 'text': "<@"+LUNCHBOT_ID+"> hello", 'user': "<@"+LUNCHBOT_ID+">" ,'channel': CHANNEL_ID, 'user': USER_ID}]
        command, channel, user = parse_commands(events, LUNCHBOT_ID)
        assert command is not None
        assert channel is not None

    def test_event_returns_correct_command_and_channel(self):
        events = [{'type': 'message', 'text': "<@"+LUNCHBOT_ID+"> hello", 'user': USER_ID ,'channel': CHANNEL_ID}]
        command, channel, user = parse_commands(events, LUNCHBOT_ID)
        assert command == "hello"
        assert channel == CHANNEL_ID

class TestCommandResponse(object):
    def test_nonexistent_command(self):
        command = "hi"
        response, _, l = respond_command(command, USER_ID, False, [])
        assert response == "I don't understand. Type 'help' to see the available commands."

    def test_help_command(self):
        command = "help"
        response, _, l = respond_command(command, USER_ID, False, [])
        assert "start" in response
        assert "stop" in response
        assert "in" in response

    def test_start_command_response(self):
        command = "start"
        response, c, l = respond_command(command, USER_ID, False, [])
        assert response == "Ey! who is going to have lunch out today? Say 'in' to join!"
        assert c == True

    def test_start_command_resets_luncher_list(self):
        response, _, l = respond_command("start", USER_ID, False, [USER_ID])
        assert len(l)==0

    def test_in_command_before_start(self):
        command = "in"
        response, _, l = respond_command(command, USER_ID, False, [])
        assert response == "It's not lunchtime yet."


    def test_in_command_when_collecting(self):
        response, _, l = respond_command("in", USER_ID, True, [])
        assert response == None
        assert len(l)>0
        assert USER_ID in l

    def test_stop_command_response(self):
        lunchers = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10", "user11"]
        response, c, l= respond_command("stop", USER_ID, True, lunchers)
        assert c==False
        print(response)
        assert "The lunch groups are" in response
        assert "leader" in response

class TestGroupMaking(object):
    def test_zero_people_lunching(self):
        lunchers=[]
        groups=make_groups(lunchers)
        assert len(groups)==0

    def test_less_than_7_lunchers(self):
        lunchers = [USER_ID]
        groups= make_groups(lunchers)
        assert len(groups)==1

    def test_more_than_7(self):
        lunchers=[]
        N=random.randint(8,100)
        print(N)
        for i in range(N):
            lunchers.append(USER_ID)
        groups = make_groups(lunchers)
        assert len(groups)==math.ceil(N/7.)



"""
8 - 4 4
9 - 4 5
10 - 5 5
11 - 5 6
12 - 6 6
13 - 6 7
14 - 7 7
15 - 5 5 5

num groups ceil(N/7)
N/numg,
"""
