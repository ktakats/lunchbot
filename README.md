# Lunchbot

A simple slack bot to organize your lunch groups written in python.

### Install and run the bot on your computer:

1. Start a virtual environment.
```
virtualenv -p python3 mylunchbot
```

2. Clone the code,
```
cd mylunchbot
git clone https://github.com/ktakats/lunchbot.git
```

3. Install the requirements
```
cd lunchbot
pip install -r requirements.txt
```

4. Create a new app on Slack (https://api.slack.com/apps), add a bot user, install the app to your workspace. Add the token of the bot user as an environmental variable as SLACK_BOT_TOKEN, eg.
```
export SLACK_BOT_TOKEN="xoxb-<your-token>"
```

5. Start the bot
```
python lunchbot.py
```

6. Invite the bot to your chosen channel. Chat away.

+1 Run the tests
```
pytest test.py
```

### Using the bot

Available commands:

* help - lists all the commands
* start - starts collecting who want to go to lunch
* in - signs you up for lunch
* stop - stops collecting sign-ups and creates the groups
* set - sets autorun, the bot will start collecting sign-ups automatically on Thursday at 10:00.
* unset - stops autorun. Now you have to start collecting lunch sign-ups with the 'start' command.
