nspiration
Every night I check an app on my phone on the optimal time to wake up. It does this by calculating sleep cycles in 1.5 hour increments. This is because humans tend to cycle between rapid eye movement and non-rapid eye movement, which translates to light sleep and heavy sleep. Waking up while in a light sleep is much easier than in a heavy sleep and makes you feel better throughout the day. By integrating this functionality into Alexa, I can ask for the time and then ask to set the alarm instead of needing to check different apps.

## What it does
The app's name is sleepy time. You invoke the app by saying
> ***Alexa, ask Sleepy Time [...]***

The app has functionality for both saying you're sleeping now and wanting to know when to wake up, as well as you know when you wake up and want to know when you can sleep. You can specify the number of sleep cycles (in 1.5 hour increments) if you want to sleep for longer or shorter.

---
You might say:
> ***Alexa, tell Sleepy Time I am going to sleep now***

to which it would reply
> For 5 sleep cycles wake up at 8:38 in the morning. For 6 sleep cycles wake up at 10:08 in the morning.
---
You might also say:
> ***Alexa, tell Sleepy Time I am waking up at 9 tomorrow***

to which it would reply
> For 5 sleep cycles go to bed at 1:16 at night if you wake up at 9:o clock.
For 6 sleep cycles go to bed at 11:46 at night if you wake up at 9:o clock
---
Or specify cycle count:
> ***Alexa, tell Sleepy Time I am sleeping now for 4 cycles***

to which it would reply
>For 4 sleep cycles wake up at 7:16 in the morning.
---

There are also convenient "cards" that show up in the Alexa app that give you the information in a visual format. This is useful if you can't want to repeat yourself or provide feedback to Amazon and the developer.

## How I built it
The project is written in Python 3 on top of the Flask web server which is running in a Heroku instance.

The Flask-Ask library provides a convenient way to interface with the Alexa service. It communicates with a Flask server that Alexa can interface with. 

I started by setting up the development environment, which included using ngrok to forward their https domain to my localdomain for testing. The core functionality was built and then integrated with the Alexa system. Alexa requires a JSON interaction model that maps 'Intents' to different functions in your program. You also specify the data type here.

Next you come up with sample utterances. This is what someone might say when interacting with your application. Even though the function is the same there are many different ways you might call for it in language. These utterances look like this:
> SleepIntent sleep for {cycles} cycles and wake up at {timeAwake}

This maps the SleepIntent to that phrase and passes in the appropriate arguments.

After some more networking configuration there's a lot of testing in the service simulator. This simulator allows you to send the JSON data to the Amazon Alexa service to test the feedback you will get without having to talk to the Alexa device each time you test.


## Challenges I ran into
Deploying was quite a challenge that took a lot of time to figure out. The Amazon Alexa service directly integrates with Amazon's Lambda service, which allows you to easily enter code online to be called on demand. Setting up Alexa and Lambda is as simple as pasting code and using the default Alexa settings.

However, Lambda only supports Python 2.7, and unfortunately both Flask-Ask and my code was written in Python 3. Alexa allows you to interface with another web service as long as it's over HTTPS and port 443.

Heroku allows for easy command line deployment through Git and has a free plan that is comprehensive enough to handle my skill. I first ran into trouble setting up an existing Git repo with Heroku, but through trial and error and documentation got my code uploaded and running on Heroku's server.

The big problem came with getting Alexa to communicate with Flask on Heroku. Flask binds itself to port 5000 by default, but Alexa requires you to use port 443. The way I solved this was through checking which port Heroku offers and then binding to that. Then Heroku automatically forwards the requests, which took me a while to realize, but now works flawlessly. I can push the master commits to Heroku and have the Alexa service keep running without stops.

## Accomplishments that I'm proud of
The biggest accomplishment is finishing the project and it being something I will use every day. There's lots of projects that I start that are cool but there already exists better alternatives, that end up feeling a bit like homework. I already use the functionality every night and now have built a skill that improves the experience.

Finishing projects is always difficult because once core functionality is built it's not always fun to polish and package. However, Amazon is giving away sweatshirts if you submit your skill in the month of January, and that was big incentive to get this skill shipped.

## What I learned
I learned a lot when deploying the app. I work a lot with websites but haven't had to deploy a non-web program before. I wasn't even really sure how as all the code I've written has has a visual interface and accessed through the browser. I learned a lot roubleshooting the ports on Heroku about how the server instance works.

Interestingly, I also had think a bit about language and how we say things. To get the skill accepted in the Alexa skill store, it has to be polished, and sound natural. I had to work through challenges like saying nine o'clock instead of nine zero zero (9:00).

## What's next for Sleepy Time Alexa Skill
The next step is to get submit to the Alexa skill store and use it at home! This will be my first time publishing a program like this and I'm looking forward to it.

