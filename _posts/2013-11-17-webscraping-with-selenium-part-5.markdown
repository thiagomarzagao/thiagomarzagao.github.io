---
comments: true
layout: post
title: webscraping with Selenium - part 5
---

This the final part of our Selenium tutorial. Here we will cover headless browsing and parallel webscraping.

<strong>why switch to headless browsing</strong>

While you are building and testing your Selenium script you want to use a conventional browser like Chrome or Firefox. That way you can see whether the browser is doing what you want it do. You can see it clicking the buttons, filling out the text fields, etc. But once you are ready to release your bot into the wild you should consider switching to a headless browser. Headless browsers are browsers that you don't see. All the action happens in the background; there are no windows.

Why would anyone want that? Two reasons.

First, you decrease the probability of errors. Your bot will be doing only one thing: interacting with the HTML code behind the website. Opening windows and rendering content can always result in errors, so why do these things now that your script is functional? This is especially the case if you are parallelizing your webscraping. You don't want five or six simultaneous Chrome windows. That would make it five or six times more likely that you get a graphics-related error.

Second, it makes it easier to use remote computers. Like Amazon EC2, Google Compute Engine, or your university's supercomputing center. Remote computers have no displays, the standard way to use them is via the command line interface. To use software that has a graphical user interface, like Chrome or Firefox, you need workarounds like X11 forwarding and virtual displays. Since a headless browser doesn't have a graphical user interface you don't need to worry about any of that. So why complicate things?

I know, it sounds weird to not see the action. But really, you've built and tested your script, you know it works, so now it's time to get rid of the visual. In the words of Master Kenobi, "stretch out with your feelings".

<iframe width="420" height="315" src="https://www.youtube.com/embed/X69NCLxwLEY" frameborder="0" allowfullscreen></iframe>

<strong>using a headless browser</strong>

There are several headless browsers, like ZombieJS, EnvJS, and PhantomJS (they tend to be written in JavaScript - hence the JS in the names). PhantomJS is the most popular, so that's my pick (the more popular the tool the more documented and tested it is and the more people can answer your questions on [StackOverflow](http://stackoverflow.com/)). 

Download [PhantomJS](http://phantomjs.org/) and save the binary to the same folder where you downloaded chromedriver before. That binary contains both the browser itself and the Selenium driver, so there is no need to download a "phantomjsdriver" (actually they call it [ghostdriver](https://github.com/detro/ghostdriver); it used to be a separate thing but now it's just embedded in the PhantomJS binary, for your convenience).

You can start PhantomJS the same way you start Chrome.

{% highlight python %}
path_to_phantomjs = '/Users/yourname/Desktop/phantomjs' # change path as needed
browser = webdriver.PhantomJS(executable_path = path_to_phantomjs)
{% endhighlight %}

But you don't want that. Websites know which browser you are using. And they know that humans use Chrome, Firefox, Safari, etc. But PhantomJS? ZombieJS? Only bots use these. Hence many websites refuse to deal with headless browsers. We want the website to think that we are using something else. To do that we need to change the user-agent string.

{% highlight python %}
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
     "(KHTML, like Gecko) Chrome/15.0.87")
{% endhighlight %}

Now we start PhantomJS but using the modified user-agent string.

{% highlight python %}
path_to_phantomjs = '/Users/yourname/Desktop/phantomjs' # change path as needed
browser = webdriver.PhantomJS(executable_path = path_to_phantomjs, desired_capabilities = dcap)
{% endhighlight %}

And that's it. The rest of your code doesn't change. The only difference is that when you run your script you won't see any windows popping up.

<strong>parallel webscraping</strong>

If you have tons of searches to do you may launch multiple instances of your code and have them run in parallel. Webscraping is a case of [embarrassingly parallel](http://en.wikipedia.org/wiki/Embarrassingly_parallel) problem, since no communication is required between the tasks. You don't even need to write a parallel script, you can simply copy and paste your script into n different files and have each do 1/n of the searches. The math is simple: if you divide the work by two you get done in half the time, if you divide the work by 10 you get done in a tenth of the time, and so on.

That is all very tempting and our first instinct is to parallelize as much as possible. We want to launch hundreds or thousands of simultaneous searches and be done in only a fraction of the time. We want to build and deploy a big, scary army of bots.

[![](http://i.imgur.com/vhqO1Vp.jpg)](http://imgur.com/vhqO1Vp)

But you shouldn't do that, both for your own sake and for the sake of others.

First of all you don't want to disrupt the website's operation. Be especially considerate with websites that normally don't attract a lot of vistors. They don't have that many servers, so if you overparallelize you can cause the whole thing to shut down. This is really bad karma. Remember that other human beings also need that website - to make a living (if they are the ones running it) or for their own research needs (people like you). Be nice.

Second, if you overparallelize your bots may lose their human façade. Humans can only handle a couple of simultaneous searches, so if the webadmins see 300 simultaneous searches coming from the same IP address they will know that something is off. So even if you don't bring the website down you can still get in trouble. You worked hard to put your Selenium script together, you don't want your bots to lose their cover now.

So, proceed gently. How many parallel bots is safe? I have no idea. That depends entirely on the website, on how many IPs you are using, on whether you have proper delays between your searches (see part 4), etc. As a general rule I wouldn't have more than three or four parallel bots per IP address (because that's what a human being could manage).

Multiple IPs don't mean you are safe though. If those IP addresses are all from the same place - say, your campus - then you are not fooling anyone. Suppose your university subscribes to LexisNexis and that, on average, about 500 people use it everyday on campus. Then you deploy 500 parallel bots. The LexisNexis webadmins will see that there is a sudden 100% increase in traffic coming from your campus. It doesn't matter whether you are using 1 or 500 IP addresses.

If you get caught things can get ugly. LexisNexis, for instance, may cut off your entire university if they catch even one person webscraping. Imagine being the person who caused your entire university to lose access to LexisNexis. Or to Factiva. Or to any other major database on which thousands of people in your campus rely for their own research needs. Bad, bad karma.

By the way, LexisNexis' terms of use explicitly prohibit webscraping; check item 2.2. It's safe to have up to 3 or 4 parallel bots; as long as you have proper delays between searches (see part 4) no one can tell your 3-4 bots from a human being. Remember: Selenium doesn't connect to the site directly but through the browser, so all that LexisNexis sees is Chrome or Firefox or Safari. But if you overparallelize then you may become the person who caused LexisNexis to cut off your entire university.

(A quick rant: item 2.2 is immoral. Universities pay millions of dollars to LexisNexis in subscriptions but then when we really need to use the content they say we can't? That's like selling 1000 gallons of water but delivering only one drop at a time. This is especially outrageous now that we have the hardware and software to text-mine millions of texts. The optimal answer here is buyers' collusion but I don't see that happening. So I see our webscraping LexisNexis as a legitimate act of civil disobedience.)

In sum, parallelizing can speed things up but you need to be careful and mindful of others when doing it.



* * *



This is it. I hope you have found this tutorial useful. There is a lot I haven't covered, like interacting with hidden elements and executing arbitrary JavaScript code, but at this point you can figure out anything by yourself.

I wrote this tutorial because even though Selenium is perhaps the most powerful webscraping tool ever made it's still somewhat unknown to webscrapers. If you found it useful as well then help spread the word.

Comments are always welcome. 

Happy webscraping!