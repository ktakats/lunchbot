import pytest
from lunchbot import parse_commands, handle_command
from lunchbot import respond_command

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
        response, _ = respond_command(command, False)
        assert response == "I don't understand. Type 'help' to see the available commands."

    def test_help_command(self):
        command = "help"
        response, _ = respond_command(command, False)
        assert "start" in response
        assert "stop" in response
        assert "in" in response

    def test_start_command_response(self):
        command = "start"
        response, c = respond_command(command, False)
        assert response == "Ey! who is going to have lunch out today? Say 'in' to join!"
        assert c == True

    def test_in_command_before_start(self):
        command = "in"
        response, _ = respond_command(command, False)
        assert response == "It's not lunchtime yet."

    def test_in_command_when_collecting(self):
        response, _ = respond_command("in", True)
        assert response == "collecting"

    def test_stop_command_response(self):
        response, c= respond_command("stop", True)
        assert c==False
        assert response == "Time to make groups"
