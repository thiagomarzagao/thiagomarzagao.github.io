---
comments: true
layout: post
title: liberating Sci-Hub
---

If you do academic research but are not affiliated with an academic institution you probably know [Sci-Hub](http://sci-hub.cc/). It gives you access to over 60 million research papers - for free (no ads, no malware, no scams). Alexandra Elbakyan, its creator, has deservedly been ranked by Nature one of the top ten most relevant people in science and we independent researchers owe her a lot.

<a href="https://sci-hub.cc/"><img src="http://i.imgur.com/KNwyCEz.png"></a>

You'd think that such an invention would be welcomed by most people who are not Elsevier executives. You'd think that such an invention would be particularly welcomed at organizations that do not have an Elsevier subscription. You'd be wrong. In the Brazilian government, where I work, Sci-Hub is not only not welcomed, it is actively blocked. The firewall doesn't let me access it.

This week I finally got tired of that nonsense - dammit, I'm a data scientist, I need academic papers not only for the research I do on the side but also, and mainly, for my day job. So I decided to build an interface to Sci-Hub - an app that takes my search string, gives it to Sci-Hub, and retrieves the results. Much like I did before [in order to use Telegram](http://thiagomarzagao.com/2016/11/23/the-tyranny-of-it-departments/).

Writing the code was easy enough, it's a simple web app that does just one thing. I wrote it on Thursday evening and I was confident that the next morning I would just fire app a new project on Google App Engine, deploy the code, and be done with it in less than an hour. Oh, the hubris. I ended up working on it all Friday and all Saturday morning; only at Saturday 12:43pm the damned thing went alive.

What follows is an account of those 36 hours, largely for my own benefit in case I run into the same issues again in the future, but also in case it may be helpful to other people also looking to unblock Sci-Hub. I'm also writing this because I think those 36 hours are a good illustration of the difference between programming, on the one hand, and software development, on the other, which is something I struggled to understand when I first started writing code. Finally, I'm writing this because those 36 hours are a good example of the inefficiencies introduced when sysadmins (or their bosses) decide to block useful resources.

**le code**

If you inspect the HTML code behind Sci-Hub you can see it's really easy to scrape:

{% highlight html %}
<div id="input"><form method="POST" action="/"><input type="hidden" id="sci-hub-plugin-check" name="sci-hub-plugin-check" value=""><input type="textbox" name="request"  placeholder="enter URL, PMID / DOI or search string" autocomplete="off" autofocus></form></div>
{% endhighlight %}

All you have to do is send a POST request. If Sci-Hub's repository has the paper you are looking for, you get it in a PDF file.

So I built this minimal web app that sends a POST request to Sci-Hub and then emails me back the PDF. I chose email because getting and returning each paper takes several seconds and I didn't want the app blocked by each request. With email I can have a background process do the heavy work; that way I can send several POST requests in a row without having to wait in-between.

To achieve that I used Python's `subprocess` module. I wrote two scripts. One is the frontend, which simply takes the user's input. I didn't want any boilerplate, so I used [cherrypy](http://cherrypy.org/) as my web framework. As for the HTML code I just put it all in the frontend.py file, as a bunch of concatenated strings (#sorrynotsorry). And I used CDNs to get the CSS code (and [no JavaScript whatsoever](http://motherfuckingwebsite.com/)).

I gave my app the grandiose name of Sci-Hub Liberator.

<img src="http://i.imgur.com/fsoRQ3V.png" title="source: imgur.com" />*(Sci-Hub Liberator's front-end. This is what happens when data scientists do web development.)*

The other script is the backend. It is launched by the frontend with a call to `subprocess.Popen`. That way all requests are independent and run on separate background processes. The backend uses Python's [requests](http://docs.python-requests.org/en/master/) package to send the POST request to Sci-Hub, then [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to comb the response and find the link to the paper's PDF, then `requests` again to fetch the PDF.

{% highlight python %}
def get_pdf(user_input):
    '''
    search string -> paper in PDF format
    '''
    response_1 = requests.post('http://sci-hub.cc/', data = {'request': user_input})
    soup = BeautifulSoup(response.text)
    url_to_pdf = 'http:' + soup.find_all('iframe')[0].get('src')
    response_2 = requests.get(url_to_pdf)
    return response_2.content
{% endhighlight %}

The backend then uses Python's own `email` package to email me the PDF.

{% highlight python %}
def send_pdf(pdf):
    '''
    sends PDF to user
    '''
    sender = 'some_gmail_account_I_created_just_for_this@gmail.com'
    text = 'Your paper is attached. Thanks for using Sci-Hub Liberator! :-)'
    body = MIMEText(text, _charset = 'UTF-8')
    message = MIMEMultipart()
    message['Subject'] = Header('your paper is attached', 'utf-8')
    message['From'] = 'Sci-Hub Liberator'
    message['To'] = 'my_email_account@gmail.com'
    message.attach(body)

    part = MIMEApplication(pdf)
    part.add_header('Content-Disposition', 'attachment; filename = "paper.pdf"')
    message.attach(part)

    smtp_server = smtplib.SMTP('smtp.gmail.com:587')
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.ehlo
    smtp_server.login(sender, 'emails_password')
    smtp_server.sendmail(sender, 'my_email_account@gmail.com', message.as_string())
    smtp_server.quit()
{% endhighlight %}

Both scripts combined had 151 lines of code. Not exactly a "Hello, World!" application but not too far from it either.

**a word of caution**

Before I proceed I must ask you not to abuse Sci-Hub's easily scrapable interface. That's an amazing service they're providing to the world and if you send thousands of requests in a row you may disrupt their operations. I trust that they have defenses against that (or else Elsevier would have taken them down long ago), but still, please don't fuck up.

**things change**

Code written and tested, I turned to Google App Engine for hosting the app. With only 151 lines of code and two scripts I thought that launching the app would be a breeze. Silly me.

I wanted to use Python 3, but Google App Engine Launcher is only compatible with Python 2. I google around and it seems that they are deprecating GAE Launcher in favor of the Google Cloud SDK. Pity. GAE Launcher was a nifty little app that made deployment really easy. I had been using it since 2013 and it allowed me to focus on my app and not on deployment nonsense.

Resigned to my fate, I downloaded the Google Cloud SDK installer and... installation failed due to an SSL-related problem. It took some half an hour of googling and debugging before I could get it to work.

**things don't change**

GAE's standard environment only allows Python 2. You can only use Python 3 in GAE's flexible environment. And the flexible environment is a different ball game.

<a href="https://cloud.google.com/appengine/docs/python/"><img src="http://i.imgur.com/pFBCHtR.png"></a>

I had never used the flexible environment before (I think it only became generally available early this year), but I decided to give it a try. To make a long story short, I couldn't make it work. The exact same code that works fine on my machine returns a mysterious `Application startup error` when I try to deploy the app. The deploy attempt generates a log file but it is equally uninformative, it only says `Deployment failed. Attempting to cleanup deployment artifacts.`

Despite hours of tinkering and googling I couldn't find out what the problem is. I [declared all my dependencies](https://cloud.google.com/appengine/docs/flexible/python/using-python-libraries) in my `requirements.txt` file (and I pointed to the same versions I was using locally); I [configured](https://cloud.google.com/appengine/docs/flexible/python/configuring-your-app-with-app-yaml) my `app.yaml` file; I made sure that all of my dependencies' dependencies were allowed. I didn't know what else to look into.

Eventually I gave up in despair and decided to fall back on GAE's standard environment, which meant reverting to Python 2. That was a bummer - it's 2017, if GAE's standard environment needs to choose between 2 and 3 then it's probably time to pick 3 (assuming there is a way to do that without killing all existing Python 2 projects).

**pip issues**

[Vendoring](https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27) didn't work for BeautifulSoup. Even though I used `pip install` and not `pip3 install` what got installed was BeautifulSoup's Python 3 version. That resulted in `from bs4 import BeautifulSoup` raising `ImportError: No module named html.entities`.

After several unsuccessful attempts to point `pip install` to a specific source file I gave up on `pip`. I tested my Mac's system-wide Python 2 installation and BeautifulSoup was working just fine there. So I went to my Mac's `site-packages` and just copied the damned `bs4` folder into my app's `lib` folder. That did the trick. It's ugly and it doesn't shed any light on the causes of the problem but by then it was Friday afternoon and I was beginning to worry this deployment might take the whole day (if only!).

**sheer dumbness**

GAE has long been my default choice for hosting applications and I've always known that it doesn't allow calls to the operating system. It's a "serverless" platform; you don't need to mess with the OS, which means you also don't *get* to mess with the OS. So I can't really explain why I based the frontend-backend communication on a call to `subprocess.Popen`, which is a call to the OS. That's just not allowed on GAE. Somehow that synapse simply didn't happen in my brain.

**back to the code**

GAE has its own utilities for background tasks - that's what the [Task Queue API](https://cloud.google.com/appengine/docs/standard/python/taskqueue/) is for. It looks great and one day I want to sit down and learn how to use it. But by the time I got to this point I was entering the wee hours of Saturday. My hopes of getting it all done on Friday were long gone and I just wanted a quick fix that would let me go to bed.

So I rewrote my app to have it show the PDF on the screen instead of emailing it. That meant I would have to wait for one paper to come through before requesting another one. At that hour I was tired enough to accept it.

The change was pretty easy - it involved a lot more code deletion than code writing. It also obviated the need for a backend, so I put everything into a single script. But the wait for the PDF to be rendered was a little too much and I thought that a loading animation of sorts was required. I couldn't find a way to do that using only cherrypy/HTML/CSS, so I ended up resorting to jQuery, which made my app a lot less lean.

**Sci-Hub is smart**

After getting rid of the OS calls I finally managed to deploy. I then noticed a `requests`-related error message. After some quick googling I found out that GAE doesn't play well with `requests` and that you need to [monkey-patch](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/urlfetch/requests/main.py) it. Easy enough, it seemed.

After the patching `requests` seemed to work (as in: not raising an exception) but all the responses from Sci-Hub came back empty. The responses came through, and with status code 200, so the communication was happening. But there was no content - no HTML, no nothing.

I thought that it might be some problem with the monkey-patching, so I commented out `requests` and switched to `urrlib2` instead. No good: same empty responses. I commented out `urllib2` and tried `urlfetch`. Same result. As per the [official documentation](https://cloud.google.com/appengine/docs/standard/python/issue-requests) I had run out of packages to try.

I thought it might have to do with the size of the response - maybe it was too large for GAE's limits. But no, the papers I was requesting were under 10MB and the limit for the response is 32MB:

<a href="https://cloud.google.com/appengine/docs/standard/python/outbound-requests"><img src="http://i.imgur.com/CgsRP5L.png" /></a>

I had briefly considered the possibility of this being an `user-agent` issue: maybe Sci-Hub just doesn't deal with bots. But everything worked fine on my machine, so that couldn't be it.

Then it hit me: maybe the user-agent string on GAE is different from the user-agent string on my machine. I got a closer look at the documentation and found this:

<a href="https://cloud.google.com/appengine/docs/standard/python/outbound-requests"><img src="http://i.imgur.com/S5DyOZv.png" /></a>

Ha. 

To test my hypothesis I re-ran the app on my machine but appending `+http://code.google.com/appengine; appid: MY_APP_ID` to my user-agent string. Sure enough, Sci-Hub didn't respond with the PDF. Oddly though, I did get a non-empty response - some HTML code with Russian text about Sci-Hub (its mission, etc; or so Google Translate tells me). Perhaps Sci-Hub checks not only the request's user-agent but also some other attribute like IP address or geographical location. One way or the other, I was not going to get my PDF if I sent the request from GAE.

At that point it was around 3am and I should probably have gone to bed. But I was in the zone. The world disappeared around me and I didn't care about sleeping or eating or anything else. I was one with the code.

<img src="http://i.imgur.com/KWLea3F.gif" />

So instead of going to bed I googled around looking for ways to fool GAE and keep my user-agent string intact. I didn't find anything of the kind, but I found Tom Tasche.

<a href="https://stackoverflow.com/a/40131640/2453555"><img src="http://i.imgur.com/3GgDt3C.png" /></a>

**back to the code (again)**

I decided to steal Tom's idea. Turns out GAE has a micro-instance that you can use for free indefinitely (unlike AWS's micro instance, which ceases to be free after a year). It's not much to look at - 0.6GB of RAM - but hey, have I mentioned it's free?

I rewrote my code (again). I went back to having the frontend and backend in separate scripts. But now instead of having the backend be a Python script called by `subprocess.Popen` I had it be an API. It received the user input and returned the corresponding PDF.

{% highlight python %}
@cherrypy.expose
def get_pdf(self, pattern):
    '''
    search string -> paper in PDF format
    '''
    scihub_html = requests.post(
        'http://sci-hub.cc/', 
        data = {'request': pattern},
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'}
        )
    soup = BeautifulSoup(scihub_html.text)
    url_to_pdf = 'http:' + soup.find_all('iframe')[0].get('src')
    scihub_bytes = requests.get(ungated_url)
    return BytesIO(scihub_bytes.text)
{% endhighlight %}

I put this new backend in a GCE micro-instance and kept the frontend at GAE. I also promoted my backend's IP from ephemeral to static, lest my app stop working out of the blue.

I was confident that this was it. I was finally going to bed. Just a quick test to confirm that this would work and then I'd switch off.

I tested the new architecture and... it failed. It takes a long time for the GCE instance to send the PDF to the GAE frontend and that raises a `DeadlineExceededError`. You can tweak the time out limit by using `urlfetch.set_default_fetch_deadline(60)` but GAE imposes a hard limit of 60 seconds - if you choose any other number your choice is just ignored. And I needed more than 60 seconds.

**back to the code (yet again)**

At that point I had an epiphany: I was already using a GCE instance anyway, so why not have the backend write the PDF to disk in a subprocess - so as not to block or dealy anything - and have it return just the link to the PDF? That sounded genius and if it weren't 6am I might have screamed in triumph.

That only required a minor tweak to the code:

{% highlight python %}
@cherrypy.expose
def get_pdf(self, pattern):
    '''
    search string -> paper in PDF format
    '''
    scihub_html = requests.post(
        'http://sci-hub.cc/', 
        data = {'request': pattern},
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'}
        )
    soup = BeautifulSoup(scihub_html.text)
    url_to_pdf = 'http:' + soup.find_all('iframe')[0].get('src')
    scihub_bytes = requests.get(url_to_pdf)
    paper_id = str(randint(0,60000000))
    with open('static/paper{}.pdf'.format(paper_id), mode = 'wb') as fbuffer:
        fbuffer.write(scihub_bytes.text)
    return paper_id
{% endhighlight %}

No `DeadlineExceededError` this time. Instead I got a `MemoryError`. It seems that 0.6GB of RAM is not enough to handle 10MB objects (10MB is the space the PDF occupies on disk; things usually take up more space in memory than on disk). So much for my brilliant workaround.

**the end of fiscal responsibility**

The cheapest non-free GCE instance has 1.7GB of RAM and costs ~$14.97 a month. I got bold and launched it (I looked into AWS EC2's roughly equivalent instance and it wasn't any cheaper: $34.96.). At last, after a painful all-nighter, my app was alive.

<img src="http://i.imgur.com/katQ7Fi.gif" />

I mean, I still haven't added any error checking, but that's deliberate - I want to see what happens when Sci-Hub can't find the paper I requested or is temporarily down or whatnot. I'll add the error checks as the errors happen.

I'll hate paying these $14.97 but it beats not having access to a resource that is critical for my work. The only alternative I see is to rescue my old Lenovo from semi-retirement and that would be annoying on several grounds (I don't have a static IP address at home, I would need to leave it up and running all day, it would take up physical space, and so on). So for now $14.97 a month is reasonable. At least that money is not going to Elsevier.

Now that I'm paying for a GCE instance anyway I could move all my code to it (and maybe go back to having a single script) and be done with GAE for this project. But I have this vague goal of making this app public some day, so that other people in my situation can have access to Sci-Hub. And with GAE it's easy to scale things up if necessary. That isn't happening any time soon though.

**things I learned**

It's not so fun to pull an all-nighter when you are no longer in grad school - we get used to having a stable schedule. But I don't regret having gone through all these steps in those 36 hours. I used Google Compute Engine for the first time and I liked it. I'm used to AWS EC2's interface and GCE's looked a lot more intuitive to me (*and* I found out GCE has a free micro-instance; even though I ended up not using it for this project it may come in handy in the future). I also familiarized myself with `gcloud`, which I would have to do anyway at some point. And I also learned a thing or two about cherrypy (like the `serve_fileobj` method, which makes it really easy to serve static files from memory).

Those 36 hours were also a useful reminder of the difference between programming and software development. Programming is about learning all the things you can do with the tools your languages provide. Software development is largely about learning all the things you *cannot* do because your runtime environment won't let you. Our Courseras and Udacities do a great job of teaching the former but we must learn the latter by ourselves, by trial and error and by reading the documentation. I'm not sure that it could be otherwise: loops and lambdas are fundamental concepts that have been with us for decades, but the quirks of GAE's flexible environment will probably have changed completely in a year or less. Any course built around GAE (or GCP in general or AWS) would be obsolete too soon to make it worth it.

This is it. I hope this may be useful to other people.