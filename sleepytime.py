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

def getTimeOfDay(time):
    timeOfDay = ''
    if (time.hour > 1) and (time.hour < 12):
        timeOfDay = 'in the morning'
    elif (time.hour >= 12) and (time.hour < 7):
        timeOfDay = 'in the afternoon'
    else:
        timeOfDay = 'at night'
    return timeOfDay

def limitCycles(cyclesIn):
    cycleList = []
    if cyclesIn <= 0:
        cycleList = [5, 6]
    elif cyclesIn > 23:
        cycleList = [23]
    else:
        cycleList = [cyclesIn]
    return cycleList

def oClock(minutes):
    if minutes == '00':
        minutes = 'o clock'
    return minutes


@ask.launch
def launch():
    speech_text = '<speak>Welcome to SleepyTime. Please say you are going '\
                    'to sleep now'\
                    '<break strength="medium" />or<break strength="medium"/>'\
                    'say the time you are waking up. '\
                    'You may also specify the number of sleep cycles</speak>'
    return question(speech_text).simple_card(title='Welcome to Sleepy Time', content=\
            'Sleep cycles are in 1.5 hour increments with 14 minutes for '\
            'falling asleep. '
            'Try saying "I wake up at eight" or "going to sleep now for 5 cycles "'\
            'or "what time should I wake up".')

#INTENDED IF SLEEPING NOW
@ask.intent('WakeupIntent', convert={'cycles': int}, default={'cycles': 0})
def wakeup(cycles):
    cycleList = []
    outputString = '<speak>'
    cardString = ''

    if convert_errors or not isinstance(cycles, int):
        return question("Please repeat your request")

    cycleList = limitCycles(cycles)

    for i in cycleList:
        wakeupTime = getFinalTime(i, 1)

        hour = datetime.datetime.strftime(wakeupTime, "%-I")
        minute = datetime.datetime.strftime(wakeupTime, "%M")
        minute = oClock(minute)

        outputString += 'For {} sleep cycles wake up at {}'\
            '<break strength="medium"/>{} {}'\
            '<break strength="strong"/>'\
            .format(i, hour, minute, getTimeOfDay(wakeupTime))

        cardString += 'For {} sleep cycles wake up at {}:{} {}. '\
                .format(i, hour, minute, getTimeOfDay(wakeupTime))

    outputString += '</speak>' 

    return statement(outputString).simple_card(\
            title='Goodnight!', content=cardString)

#INTENDED IF YOU KNOW WHEN YOU'RE WAKING UP
@ask.intent('SleepIntent', convert={'timeAwake': 'time', 'cycles': int}, default={'cycles': 0})
def timeToSleep(timeAwake, cycles):
    cycleList = []
    outputString = '<speak>'
    cardString = ''

    if convert_errors or not isinstance(timeAwake, datetime.time):
        return question("Please repeat your request")

    cycleList = limitCycles(cycles)

    timeAwake = datetime.datetime.combine(datetime.date.today(), timeAwake)
    
    wakeHour = datetime.datetime.strftime(timeAwake, "%-I")
    wakeMinute = datetime.datetime.strftime(timeAwake, "%M")
    wakeMinute = oClock(wakeMinute)

    for i in cycleList:
  
        timeToSleep = getFinalTime(i, -1, timeAwake)

        sleepHour = datetime.datetime.strftime(timeToSleep, "%-I")
        sleepMinute = datetime.datetime.strftime(timeToSleep, "%M")
        sleepMinute = oClock(sleepMinute)

        outputString += 'For {} sleep cycles go to bed at {}'\
            '<break strength="medium"/>{} {}, if you wake up at'\
            '{}<break strength="medium"/>{}<break strength="strong"/>'\
            .format(i, sleepHour, sleepMinute, getTimeOfDay(timeToSleep), wakeHour, wakeMinute)

        cardString += 'For {} sleep cycles go to bed at '\
                '{}:{} {} if you wake up at {}:{}. '.format(\
                i, sleepHour, sleepMinute, getTimeOfDay(timeToSleep),\
                wakeHour, wakeMinute)


    outputString += '</speak>'
    return statement(outputString).simple_card(\
            title='Go to sleep at...', content=cardString)

@ask.session_ended
def session_ended():
    return "", 200;

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

