import datetime
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def launch():
    speech_text = 'Welcome to the SleepyTime App. Repeat wakeup times'
    return question(speech_text)

@ask.intent('WakeupIntent')
def wakeup():
    currentTime = datetime.datetime.now()
    timeDelta = datetime.timedelta(hours=9, minutes=14)
    wakeupTime = currentTime + timeDelta
    return statement('Wake up at {} tomorrow'.format(wakeupTime.hour))

@ask.session_ended
def session_ended():
    return "", 200;

if __name__ == '__main__':
    app.run(debug=True)

