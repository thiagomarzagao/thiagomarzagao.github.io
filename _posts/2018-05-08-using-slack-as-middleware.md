---
comments: true
layout: post
title: using Slack as middleware
---

I started working remote a few weeks ago. It's sheer awesomeness - no distractions, no commute, no shabby cafeteria lunch. But there was one minor glitch: I was having trouble accesing my organization's proprietary data. Being a government agency, we hoard tons of sensitive data on people - addresses, taxpayer IDs, personal income, etc. So, naturally, we restrict access to our databases. There is no URL I can go to when I need to run some database query; I need to be inside my organization's network to run database queries.

I can use a VPN to log into my office PC from any machine. And once I'm logged into my office PC I can access whatever I want. But that means being forced to use my lame, old office PC instead of my sleak, fast MacBook Pro. Using the VPN also means enduring a maddening lag. It's only a fraction of a second, but it's noticeable and it can drive you insane. Finally, using the VPN means I have no *local* internet access - while I'm in the VPN my laptop has no other contact with the outside world, which results in my not being able to use Spotify and a bunch of other stuff. And I need my 90s Eurodance playlists to be in the proper mindset for writing code.

After enduring all that (I know, tiny violin...) for a couple of weeks I decided to do something about it. I realized that I needed a "bridge" between the data and my laptop. Some web service of sorts that could receive data requests and respond to them. Now, I'd never trust myself to build something like that. I don't know nearly enough about information security to go about building that sort of tool. I don't wanna be the guy who caused every Brazilian's monthly income to be exposed to the world.

Then it hit me: I don't need to build anything like that, these tools have already been built and we already use them to exchange sensitive data. I'm talking about messaging apps like Slack, Telegram, and the like. My office PC can access Slack. My personal laptop can access Slack. Slack is what my team [uses](https://twitter.com/tmarzagao/status/983389581776125954) for communication, which means sensitive information already circulates through it. In sum, the middleman I needed was already in place. All I had to do was to repurpose it. And that's what I did. What follows bellow is a brief account of how I did it, in case other people may be in the same situation.

**step 1: stuff that doesn't involve code**

The first thing you need to create are the Slack channels that will handle the data requests. I chose to create two - `#incoming`, to receive the data requests, and `#outgoing`, to send the requested data. I made them private, so as not to annoy my teammates with notifications and messages they don't need to see. Alternatively, you could create an entirely new Slack workspace; that way you isolate human messaging from bot messaging.

Once you've created the channels you'll need to create a Slack bot. It's this bot that will: a) read the data requests that arrive on `#incoming`; and b) post the requested data to `#outgoing`. Slack lets you choose between two types of bots: "app bots" and "custom bots". They nudge you towards the former but the latter is a lot more straightforward to set up: just click [here](https://my.slack.com/apps/A0F7YS25R-bots), click "Add Configuration", and follow the instructions. When you're done, write down your bot's API token - it's the string that starts with `xoxb-` -, and, on your Slack workspace, invite your bot to join `#incoming` and `#outgoing`.

**step 2: testing your bot**

We need to make sure that your Slack bot can read from `#incoming` and post to `#outgoing`.

Let's start with reading. There are a number of ways to go about this - Slack has a number of APIs. I think the [Web API](https://api.slack.com/web) is the best pick for the impatient. Now, the documentation doesn't have a quickstart or many useful examples. The explanations are verbose and frustratingly unhelpful if you just want to "get it done" quick. So instead of making you read the docs I'll just give you what you need to know: make a GET request to `https://slack.com/api/groups.history?token=xoxb-your-bot-token&channel=id_of_incoming`, where `xoxb-your-bot-token` is the token you wrote down in step 1 and `id_of_incoming` is the ID of the `#incoming` channel (it's the endpoint of the channel's URL). That will return to you the channel's messages (up to 100 messages). If there are no messages in `#incoming` you won't get anything interesting back. If that's the case, just post anything to the channel first.

In real life you won't be using Terminal/cmd for this, you'll be using a Python or R script or something along these lines. Here's how to do that in Python:

{% highlight python %}
import requests

def read_messages():
    slack_token = 'xoxb-your-bot-token'
    slack_url = 'https://slack.com/api/groups.history'
    params = {
        'token': slack_token,
        'channel': 'id_of_incoming'
        }
    response = requests.get(slack_url, params = params, verify = False)
    if response.status_code == 200:
        return response.json()

response = read_messages()
{% endhighlight %}

What you get back is a Python dict which should have a key named 'messages'. So, `if 'messages' in 'response'`, then inside `response['messages']` you'll find a list of dicts, each dict being a message, each dict's key being an attribute of said message (timestamp, text, user who posted it, etc).

Now, you don't want to access `#incoming`'s entire history every time you poll it. You can include a parameter named `oldest` in the `params` dict and assign a timestamp to it. Then `read_messages` won't return messages older than the specified timestamp.

(A little gotcha: what you pass as `channel` is not the channel's name but the channel's ID, which you can get from its URL. Some Slack methods do accept the channel's name but I never remember which ones, so it's easier to just use the channel's ID for everything.)

(Because you went with a custom bot instead of an app bot you won't have to deal with a bunch of error messages having to do with something Slack calls "scope". You won't waste two days in a mad loop of trying to get the scopes right, failing, cursing Slack, refusing to read the API documentation, failing, cursing Slack, refusing to read the API documentation. I envy you.)

Alright then, let's move on to posting. Here's how you do it: make a POST request to `https://slack.com/api/chat.postMessage`, using your bot's token, your channel's ID, and the message of the text as payload. Like this:

{% highlight python %}
import requests

def post_to_outgoing(message):
    slack_token = 'xoxb-your-bot-token'
    slack_url = 'https://slack.com/api/chat.postMessage'
    payload = {
        'token': slack_token,
        'channel': 'id_of_outgoing',
        'text': message
        }
    requests.post(slack_url, data = payload, verify = False)

post_to_outgoing('hey macarena')
{% endhighlight %}

There. Once you run this code you should see the message "hey macarena" appear in `#outgoing`.

**step 3: receiving `#incoming` messages**

Alright, now you need a server-side program that will check `#incoming` for new messages - say, every five seconds or so. By server-side I mean it will run inside your company's network; it needs to run from a machine that has access to your company's databases. Here's an example:

{% highlight python %}
import time
import requests

def read_messages(timestamp):
    slack_token = 'xoxb-your-bot-token'
    slack_url = 'https://slack.com/api/groups.history'
    params = {
        'token': slack_token,
        'channel': 'id_of_incoming',
        'oldest': timestamp
        }
    response = requests.get(slack_url, params = params, verify = False)
    if response.status_code == 200:
        return response.json()

while True:
    timestamp = time.time() - 5
    new_msg = read_request(timestamp)
    if new_msg:
        print('new message(s) received:', new_msg['messages'])
    time.sleep(5)
{% endhighlight %}

Now, you probably want this "listener" to run in the background, so that you can log off without killing it. If you're running it on a Linux machine the simplest solution is to use [tmux](https://hackernoon.com/a-gentle-introduction-to-tmux-8d784c404340). It lets you create multiple "sessions" and run each session in the background. If you're doing it on a Windows machine you can use [cygwin](https://stackoverflow.com/a/9591514/2453555) or, if that's Windows 10, you can use tmux with the [native Ubuntu binaries](https://stackoverflow.com/a/39538685/2453555).

**step 4: processing `#incoming` messages**

Receiving messages is not enough, your script needs to do something about them. The simple, quick-and-dirty solution is to have your `#incoming` messages be the very database queries you want to run. An `#incoming` message could be, say, `SELECT [some_column] FROM [some].[table] WHERE [some_other_column] = 0`. Then the listener (the server-side program we created before) would read the query and use an ODBC package - like pyodbc or rodbc - to run it. If that works for you, here's how you'd amend the listener we created before to have it handle SQL queries:

{% highlight python %}
import time
import pyodbc
import requests

def read_messages(timestamp):
    slack_token = 'xoxb-your-bot-token'
    slack_url = 'https://slack.com/api/groups.history'
    params = {
        'token': slack_token,
        'channel': 'id_of_incoming',
        'oldest': timestamp
        }
    response = requests.get(slack_url, params = params, verify = False)
    if response.status_code == 200:
        return response.json()

def run_query(query):
    cnxn = pyodbc.connect(
        driver = 'name of your ODBC driver',
        server = 'path-to-your-database-server',
        database = 'name_of_your_database,
        uid = 'uid',
        pwd = 'pwd'
        )
    cursor = cnxn.cursor()
    cursor.execute(query)
    resultset = cursor.fetchall()
    return resultset

while True:
    timestamp = time.time() - 5
    r = read_request(timestamp)
    if r:
        for message in r['messages']:
            resultset = run_query(message['text'])
            print('query:', message['text'])
            print('results:', resultset)
    time.sleep(5)
{% endhighlight %}

Ok, I'm glossing over a bunch of details here. First you'll need to set up an ODBC driver, which isn't always easy to get right the first time - it depends on what SQL engine you have (SQL Server, MySQL, etc), on whether your script is running on Linux or Windows, and on what credentials you're using to connect to your SQL engine. I can't really help you out on this, you'll have to google your way around. If you've never set up an ODBC connection before this is probably the part that's going to take up most of your time.

Once the ODBC part is taken care of, leave the script above running and post some SQL query on `#incoming`. You should see the the result set of the query. Well done then, everything is working so far.

**step 5: replying to `#incoming` messages**

Alright, so you now have a script that receives queries and executes them. Now your script needs to post the result sets to `#outgoing`. There really isn't much mystery here - we already wrote `post_to_outgoing` above. The only thing left is to convert our result set into a string, so that Slack can accept it. In Python the `json` module handles that for us: `json.dumps(your_data)` takes a list or dict (or list of dicts, or dict of lists) and turns it into a string. It's all below.

{% highlight python %}
import json
import time
import pyodbc
import requests

def read_messages(timestamp):
    slack_token = 'xoxb-your-bot-token'
    slack_url = 'https://slack.com/api/groups.history'
    params = {
        'token': slack_token,
        'channel': 'id_of_incoming',
        'oldest': timestamp
        }
    response = requests.get(slack_url, params = params, verify = False)
    if response.status_code == 200:
        return response.json()

def run_query(query):
    cnxn = pyodbc.connect(
        driver = 'name of your ODBC driver',
        server = 'path-to-your-database-server',
        database = 'name_of_your_database',
        uid = 'uid',
        pwd = 'pwd'
        )
    cursor = cnxn.cursor()
    cursor.execute(query)
    resultset = cursor.fetchall()
    return resultset

def post_to_outgoing(message):
    slack_token = 'xoxb-your-bot-token'
    slack_url = 'https://slack.com/api/chat.postMessage'
    payload = {
        'token': slack_token,
        'channel': 'id_of_outgoing',
        'text': message
        }
    requests.post(slack_url, data = payload, verify = False)

while True:
    timestamp = time.time() - 5
    r = read_request(timestamp)
    if r:
        for message in r['messages']:
            resultset = run_query(message['text'])
            for result in resultset:
                output = json.dumps(list(result))
                post_to_outgoing(output)
    time.sleep(5)
{% endhighlight %}

Ta-da. As long as this script is running continuously inside your company's network you no longer need a VPN to query `name_of_your_database`. If you want more flexibility you can tweak `run_query` so that it takes the name of the database as a second argument. And you should sprinkle `try/except` statements here and there to capture database errors and the like.

You've taken remote work one step further. It's not only you who can work remote now: *the applications you develop no longer need to live inside your company's network*. You can develop on whatever machine and environment you choose and have your applications post their queries to `#incoming` and retrieve the result sets from `#outgoing`.

One gotcha here: Slack automatically breaks up long messages, so if your query exceeds Slack's maximum length it will be truncated and `run_query` will probably (hopefully) raise an error. Keep it short.

**step 6: make it neat**

Alright, you have a functioning "bridge" between you and your company's databases. But that's still a crude tool, especially if you will develop applications on top of it. You don't want your apps to post raw SQL queries on Slack - that's a lot of unnecessary characters being passed back and forth. Instead of a `run_query` function you should have a `get_data` function that stores a "template" of the query and only adds to it, say, the part that comes after the `WHERE [something] = `. Something like this:

{% highlight python %}
def get_data(input):
    query = 'SELECT [some_column] FROM [some_database].[some_table] WHERE [other_column] = ' + input
    cnxn = pyodbc.connect(
        driver = 'name of your ODBC driver',
        server = 'path-to-your-database-server',
        database = 'name_of_your_database',
        uid = 'uid',
        pwd = 'pwd'
        )
    cursor = cnxn.cursor()
    cursor.execute(query)
    resultset = cursor.fetchall()
    return resultset
{% endhighlight %}

This is still too crude to be called an API but it's a first step in that direction. The idea is to make the Slack-your_app interface as tight as possible, so as to minimize the types of errors you will encounter and to minimize the exchange of unnecessary strings. If you know exactly the sort of stuff that will be passed to `get_data` it's easier to reason about what the code is doing.

I think this is it. Happy remoting!