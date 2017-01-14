import datetime
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, '/')

def getTimeToWake(cycles=6):
    hoursOfSleep = 1.5 * cycles

    currentTime = datetime.datetime.now()
    timeDelta = datetime.timedelta(hours=hoursOfSleep, minutes=14)

    wakeupTime = currentTime + timeDelta

    return wakeupTime


@ask.launch
def launch():
    speech_text = 'Welcome to the SleepyTime App. Repeat wakeup times'
    return question(speech_text)

@ask.intent('WakeupIntent')
def wakeup():
    wakeupTime = getTimeToWake()
    return statement('<speak>Wake up at {}<break strength="medium"/>{:02d} tomorrow</speak>'.\
            format(wakeupTime.hour, wakeupTime.minute))

@ask.session_ended
def session_ended():
    return "", 200;

if __name__ == '__main__':
    app.run(debug=True)

