#!/usr/local/bin/python3.4

import datetime, os
from flask import Flask, render_template
from flask_ask import Ask, convert_errors, request, session, question, statement

app = Flask(__name__)
ask = Ask(app, '/')

#direction indicates counting forward or back. 1 for forward, -1 for back
def getFinalTime(cycles, direction, startTime=None):
    hoursOfSleep = 1.5 * cycles
    if startTime is None:
        startTime = datetime.datetime.now()
    timeDelta = datetime.timedelta(hours=hoursOfSleep, minutes=14)

    finalTime = startTime + (direction * timeDelta)

    return finalTime

@ask.launch
def launch():
    speech_text = 'Welcome to the SleepyTime App. Please ask'\
                    'for the time to wake up if you sleep now'\
                    'or ask for what time to sleep if you for'\
                    'a wakeup time'
    return question(speech_text)

@ask.intent('WakeupIntent', convert={'cycles': int}, default={'cycles': 0})
def wakeup(cycles):
    cycleList = []
    outputString = '<speak>'

    if convert_errors or not isinstance(cycles, int):
        return question("Please repeat your request")

    if cycles == 0:
        cycleList = [5, 6]
    else:
        if cycles > 23:
            cycles = 23
        cycleList = [cycles]
    for i in cycleList:
        wakeupTime = getFinalTime(i, 1)

        hour = datetime.datetime.strftime(wakeupTime, "%-I")
        minute = datetime.datetime.strftime(wakeupTime, "%M")

        outputString += 'For {} cycles wake up at {}'\
            '<break strength="medium"/>{} tomorrow'\
            '<break strength="strong"/>'\
            .format(i, hour, minute)

    outputString += '</speak>' 
    return statement(outputString)

@ask.intent('SleepIntent', convert={'timeSleep': 'time'})
def timeToSleep(timeSleep):
    outputString = '<speak>'

    if convert_errors or not isinstance(cycles, int):
        return question("Please repeat your request")

    timeSleep = datetime.datetime.combine(datetime.date.today(), timeSleep)
    for i in [5, 6]:
  
        timeToSleep = getFinalTime(i, -1, timeSleep)

        hour = datetime.datetime.strftime(timeToSleep, "%-I")
        minute = datetime.datetime.strftime(timeToSleep, "%M")

        outputString += 'For {} cycles sleep at {}'\
            '<break strength="medium"/>{} tonight'\
            '<break strength="strong"/>'\
            .format(i, hour, minute)



    outputString += '</speak>'
    return statement(outputString)

@ask.session_ended
def session_ended():
    return "", 200;

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

