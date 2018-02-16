import pytest
from lunchbot import parse_commands, handle_command
from commands import respond_command

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

class TestCommandResponse(object):
    def test_nonexistent_command(self):
        command = "hi"
        response = respond_command(command)
        assert response == "I don't understand. Type 'help' to see the available commands."

    def test_help_command(self):
        command = "help"
        response = respond_command(command)
        assert "start" in response
        assert "stop" in response
        assert "in" in response
