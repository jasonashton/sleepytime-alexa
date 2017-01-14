import datetime
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, '/')

def getTimeToWake(cycles):
    hoursOfSleep = 1.5 * cycles

    currentTime = datetime.datetime.now()
    timeDelta = datetime.timedelta(hours=hoursOfSleep, minutes=14)

    wakeupTime = currentTime + timeDelta

    return wakeupTime


@ask.launch
def launch():
    speech_text = 'Welcome to the SleepyTime App. Repeat wakeup times'
    return question(speech_text)

@ask.intent('WakeupIntent', convert={'cycles': int}, default={'cycles': None})
def wakeup(cycles=0):
    cycleList = []
    outputString = '<speak>'
    if cycles is None:
        cycleList = [5, 6]
    else:
        cycleList = [cycles]
    for i in cycleList:
        wakeupTime = getTimeToWake(i)
        outputString += 'For {} cycles wake up at {}'\
            '<break strength="medium"/>{:02d} tomorrow'\
            '<break strength="strong"/>'\
            .format(i, wakeupTime.hour, wakeupTime.minute)

    outputString += '</speak>' 
    return statement(outputString)

@ask.session_ended
def session_ended():
    return "", 200;

if __name__ == '__main__':
    app.run(debug=True)

