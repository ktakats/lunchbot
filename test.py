import pytest
from lunchbot import parse_commands, handle_command

LUNCHBOT_ID = "U123"
CHANNEL_ID ="C999999"

class TestCommandParser(object):
    def test_no_event_returns_none(self):
        events=[]
        command, channel = parse_commands(events, "<@U123>")
        assert command is None
        assert channel is None

    def test_event_returns_not_none(self):
        events = [{'type': 'message', 'text': "<@"+LUNCHBOT_ID+"> hello", 'user': "<@"+LUNCHBOT_ID+">" ,'channel': CHANNEL_ID}]
        command, channel = parse_commands(events, LUNCHBOT_ID)
        assert command is not None
        assert channel is not None

    def test_event_returns_correct_command_and_channel(self):
        events = [{'type': 'message', 'text': "<@"+LUNCHBOT_ID+"> hello", 'user': "<@"+LUNCHBOT_ID+">" ,'channel': CHANNEL_ID}]
        command, channel = parse_commands(events, LUNCHBOT_ID)
        assert command == "hello"
        assert channel == CHANNEL_ID
