---
comments: true
layout: post
title: I need to use Google App Engine to text my girlfriend
---

This is the story of how I had to build and deploy a freaking app just so I can text my girlfriend when I'm at the office. Perhaps it'll help others who are also subject to the arbitrary rules of IT departments everywhere. (Dilberts of the world, unite!)

For some two years now my messaging app of choice has been [Telegram](https://telegram.org/). It's lightweight, end-to-end encrypted, well designed, and free; it's impossible not to love it. Now, I hate typing on those tiny on-screen keyboards, so most of the time what I actually use is [Telegram's desktop app](https://desktop.telegram.org/). Problem is, I can't use it when I'm at work. My organization's IT department blocks access to Telegram's servers (dont' ask). I can install the app, but it doesn't connect to anything; it can't send or receive messages.

So, I looked into Telegram's competitors. I tried WhatsApp, but its desktop version is blocked as well at my organization. And in any case I tried it at home and it's sheer garbage: the desktop app needs your phone to work (!) and it crashes every ~15 minutes. (I keep pestering my friends to switch from WhatsApp to Telegram but WhatsApp is hugely popular in Brazil and [network externalities](https://en.wikipedia.org/wiki/Network_effect) get in the way.)

Then it hit me: why not Slack? The IT department doesn't block it and I already use Slack for professional purposes. Why not use it to talk to my girlfriend too? I created a channel, got her to sign up, and we tried it for a couple of days.

Turns out Slack solved the desktop problem at the cost of creating a mobile problem. I don't have any issues with Slack's web interface - I keep my channels open on Chrome at all times and that works just fine. But when I switch to mobile... boy, that's one crappy iOS app. Half the time it just doesn't launch. Half the time it takes forever to sync. Granted, my iPhone 5 is a bit old. But the Telegram iOS app runs as smooth and fast as it did two years ago, so the hardware is not at fault here.

As an aside, turns out Slack's desktop app is also ridiculously heavy. I don't really use it - I use Slack's web interface instead -, but that's dispiriting nonetheless.

<a href="https://twitter.com/popey/status/793399003463516160"><img src="http://i.imgur.com/JTqVW8b.png"></a>

I tried Facebook's Messenger. Blocked. I tried a bunch of lesser-known alternatives. Blocked.

Eventually I gave up on trying different messaging apps and asked the IT department to unblock access to Telegram's servers. They said no - because, well, reasons. (In the words of Thomas Sowell, "You will never understand bureaucracies until you understand that for bureaucrats procedure is everything and outcomes are nothing".)

<a href="http://dilbert.com/strip/2007-11-16"><img src="http://i.imgur.com/H6Sd4l5.png"></a>

The IT guys told me I could appeal to a higher instance - some committee or another -, but I've been working in the government for a while and I've learned to pick my fights. Also, I believe in [Balaji Srinivasan](https://twitter.com/balajis?lang=en)'s "don't argue" policy.

<a href="https://twitter.com/balajis/status/753773388452073472"><img src="http://i.imgur.com/bSSLQNn.png"></a>

So, I rolled up my sleeves and decided to build my own solution.

I don't need to build a full-fledged messaging app. What I need is extremely simple: a middleman. Something that serves as a bridge between my office computer and Telegram's servers. I need a web app that my office computer can visit and to which I can POST strings and have those strings sent to my girlfriend's Telegram account.

That app needs to be hosted somewhere, so the first step is choosing a platform. I briefly considered using my personal laptop for that, just so I didn't have to deal with commercial cloud providers. But I worry about exposing to the world my personal files, laptop camera, browser history, and the like. Also, I want 24/7 availability and sometimes I have to bring my laptop to the office.

So I settled on [Google App Engine](https://appengine.google.com/). I used it before (to host an [app](http://democracy-scores.org/) that lets people replicate my Ph.D. research) and I liked the experience. And, more importantly, it has a free tier. GAE has changed quite a bit since the last time I used it (early 2014), but it has an interactive tutorial that got me up to speed in a matter of minutes.

You can choose a number of programming languages on GAE. I picked Python because that's what I'm fastest at. (In hindsight, perhaps I should've used this as a chance to learn some basic Go.)

Instead of starting from scratch I started with GAE's default "Hello, world!" Python app. The underlying web framework is Flask. That's my go-to framework for almost all things web and that made things easier. Using Flask, this is how you control what happens when a user visits your app's homepage:

{% highlight python %}
# this is all in the main.py file of GAE's default "Hello, world!" Python app
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, world!'
{% endhighlight %}

I don't want a static webpage though, I want to communicate with Telegram's servers. In order to do that I use a Python module called [telepot](https://github.com/nickoala/telepot). This is how it works: you [create a Telegram bot account](https://core.telegram.org/bots) and then you use telepot to control that bot. (In other words, the sender of the messages will not be you, it will be the bot.

When you create your bot you receive a token credential, which you will then pass to telepot.

{% highlight python %}
import telepot
bot = telepot.Bot('YOUR_TOKEN')
bot.getMe()
{% endhighlight %}

You can now make your bot do stuff, like sending messages. Now, Telegram enforces a sort of Asimovian law: a bot cannot text a human unless it has been texted by that human first. In other words, bots can't initiate conversations. So I created my bot, told my girlfriend its handle (`@bot_username`), and had her text it. That message (like all Telegram messages) came with metadata (see [here](http://telepot.readthedocs.io/en/latest/#receive-messages)), which included my girlfriend's Telegram ID. That's all I need to enable my bot to text her.

{% highlight python %}
girlfriend_id = 'SOME_SEQUENCE_OF_DIGITS'
bot.sendMessage(girlfriend_id, 'How you doing?')
{% endhighlight %}

Now let's merge our web app code and our telepot code in our `main.py` file:

{% highlight python %}
import telepot
from flask import Flask
app = Flask(__name__)

bot = telepot.Bot('YOUR_TOKEN')
bot.getMe()
girlfriend_id = 'SOME_SEQUENCE_OF_DIGITS'

@app.route('/')
def textGirlfriend():
    bot.sendMessage(girlfriend_id, 'How you doing?')
    return 'message sent!'
{% endhighlight %}

(This can be misused in a number of ways. You could, say, set up a cron job to text 'thinking of you right now!' to your significant other at certain intervals, several times a day. Please don't.)

The rest of the default "Hello, world!" Python app remains the same except for two changes: a) you need to install telepot; use `pip install` with the `-t` option to specify the `lib` directory in your repository; and b) you need to add `ssl` under the `libraries` header of your `app.yaml` file.

So, I created a web app that my IT department does not block and that texts my girlfriend when visited. But I don't want to text 'How you doing?' every time. So far, the app doesn't let me choose the content of the message.

Fixing that in Flask is quite simple. We just have to: a) add a text field to the homepage; b) add a 'submit' button to the homepage; and c) tell the app what to do when the user clicks 'submit'. (We could get fancy here and create HTML templates but let's keep things simple for now.)

{% highlight python %}
import telepot
from flask import Flask
from flask import request # so that we can get the user's input
app = Flask(__name__)

bot = telepot.Bot('YOUR_TOKEN')
bot.getMe()
girlfriend_id = 'SOME_SEQUENCE_OF_DIGITS'

@app.route('/')
def getUserInput():
    return '<form method="POST" action="/send"><input type="text" name="msg" size="150"><br><input type="submit" value="submit"></form>'

@app.route('/send', methods = ['POST'])
def textGirlfriend():
    bot.sendMessage(girlfriend_id, request.form['msg'])
    return 'message sent!'
{% endhighlight %}

And voilà, I can now app-text my girlfriend.

<img src="http://i.imgur.com/VeHxBPU.png" title="source: imgur.com" />

Yeah, I know, that would hardly win a design contest. But it works.

This is where I'm at right now. I did this last night, so there is still a lot of work ahead. Right now I can send messages this way, but if my girlfriend simply hit 'reply' her message goes to the bot's account and I just don't see it. I could have the app poll the bot's account every few seconds and alert me when a new message comes in, but instead I think I'll just create a Telegram group that has my girlfriend, myself, and my bot; I don't mind reading messages on my phone, I just don't like to type on my phone. Another issue is that I want to be able to text-app my family's Telegram group, which means adding radio buttons or a drop-down menu to the homepage so I can choose between multiple receivers. Finally, I want to be able to attach images to my messages - right now I can only send text. But the core is built; I'm free from the tyranny of on-screen keyboards.

This is it. In your face, IT department.

<a href="http://imgur.com/Dw0FeG5"><img src="http://i.imgur.com/Dw0FeG5.jpg" title="source: imgur.com" /></a>