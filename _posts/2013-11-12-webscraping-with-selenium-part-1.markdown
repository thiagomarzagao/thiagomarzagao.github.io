---
author: thiagomarzagao
comments: true
date: 2013-11-12 21:15:23+00:00
layout: post
slug: webscraping-with-selenium-part-1
title: webscraping with Selenium - part 1
wordpress_id: 302
categories:
- LexisNexis
- Python
- webscraping
tags:
- lexisnexis
- Python
- selenium
- webscraping
---

If you are webscraping with Python chances are that you have already tried `urllib`, `httplib`, `requests`, etc. These are excellent libraries, but some websites don't like to be webscraped. In these cases you may need to disguise your webscraping bot as a human being. Selenium is just the tool for that. Selenium is a webdriver: it takes control of your browser, which then does all the work. Hence what the website "sees" is Chrome or Firefox or IE; it does not see Python or Selenium. That makes it a lot harder for the website to tell your bot from a human being.

In this tutorial I will show you how to webscrape with Selenium. This first post covers the basics: locating HTML elements and interacting with them. Later posts will cover things like downloading, error handling, dynamic names, and mass webscraping.

There are Selenium bindings for Python, Java, C#, Ruby, and Javascript. All the examples in this tutorial will be in Python, but translating them to those other languages is trivial.

<strong>installing Selenium</strong>

To install the Selenium bindings for Python, simply use PIP:

{% highlight bash %}
pip install selenium
{% endhighlight %}

You also need a "driver", which is a small program that allows Selenium to, well, "drive" your browser. This driver is browser-specific, so first we need to choose which browser we want to use. For now we will use Chrome (later we will switch to PhantomJS). Download the latest version of the [chromedriver](http://chromedriver.storage.googleapis.com/index.html), unzip it, and note where you saved the unzipped file.

<strong>choosing our target</strong>

In this tutorial we will webscrape [LexisNexis Academic](https://www.lexisnexis.com/hottopics/lnacademic/?verb=sf&sfi=AC00NBGenSrch). It's a gated database but you are probably in academia (just a guess) so you should have access to it through your university.

(Obs.: LexisNexis Academic is set to have a new interface starting December 23rd, so if you are in the future the code below may not work. It will still help you understand Selenium though. And adapting it to the new LexisNexis interface will be a nice learning exercise.)

<strong>opening a webpage</strong>

Now on to coding. First we start the webdriver:

{% highlight python %}
from selenium import webdriver

path_to_chromedriver = '/Users/yourname/Desktop/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
{% endhighlight %}

When you run this code you'll see a new instance of Chrome magically launch.

Now let's open the page we want:

{% highlight python %}
url = 'https://www.lexisnexis.com/hottopics/lnacademic/?verb=sf&amp;sfi=AC00NBGenSrch'
browser.get(url)
{% endhighlight %}

The page looks like this:

[![](http://i.imgur.com/fWbtCGO.jpg)](http://imgur.com/fWbtCGO)

<strong>locating page elements</strong>

Before we fill out forms and click buttons we need to locate these elements. This step is going to be easier if you know some HTML but that is not a pre-requisite (you will end up learning some HTML on-the-fly as you do more and more webscraping).

A page element usually has a few attributes - a name, an id, a CSS selector, an xpath, etc. (Don't worry if you've never heard of these things before.) We can use these attributes to help us locate the element we want.

How can we find what these attributes are for a given element? Simple: just right-click it and choose "Inspect Element". Your browser will then show you the corresponding HTML code. For instance, if you do this with the "Search Terms" form on the page we opened above you'll see something like this:

[![](http://i.imgur.com/rmDpfyL.jpg)](http://imgur.com/rmDpfyL)

The HTML code of the element you selected appears highlighted in blue. Let me copy and paste it below, so you can have a better look at it:

{% highlight html %}
<textarea id="terms" style="vertical-align: top;" name="terms"></textarea>
{% endhighlight %}

Ha! Now we know two attributes of the "Search Terms" form: its name is "terms" and its id is (also) "terms".

We are not ready to locate the element though. HTML pages usually contain multiple "frames" and our element is probably inside one of these frames. We need to know which one. To find out, start on that blue-highlighted line we saw before and keep scrolling up until you find `<frame`. You'll eventually find this line:

{% highlight html %}
<frame src="" name="mainFrame" id="mainFrame" title="mainFrame">
{% endhighlight %}

That means our "Search Terms" form is inside a frame named "mainFrame". Now keep scrolling up to see if "mainFrame" is inside some other frame. Here it is not, but that is always a possibility and you need to check.

The next thing we do is go to that frame. Here is how we do it:

{% highlight python %}
browser.switch_to_frame('mainFrame')
{% endhighlight %}

Once we are on the correct frame we can finally search for the element. Let's search it using its id:

{% highlight python %}
browser.find_element_by_id('terms')
{% endhighlight %}

And that's it. We have located the element.

<strong>see the beauty?</strong>

As the code above shows, Selenium is very intuitive. To switch frames we use 'switch_to_frame'. To find an element by its id we use 'find_element_by_id'. And so on.

Another great feature of Selenium is that it's very similar across all languages it supports. In Java, for instance, this is how we switch frames and find elements by id:

{% highlight java %}
browser.switchTo().frame("frameName");
browser.findElement(By.id("elementId"));
{% endhighlight %}

So even if you first learn Selenium in Python it's very easy to use it in other languages later.

<strong>interacting with page elements</strong>

Now that we've found the "Search Terms" form we can interact with it. First we want to make sure that the form is empty:

{% highlight python %}
browser.find_element_by_id('terms').clear()
{% endhighlight %}

Now we can write on the form. Here we are interested in all occurrences of the word "balloon" in the news today. We start by writing "balloon" on the form:

{% highlight python %}
browser.find_element_by_id('terms').send_keys('balloon')
{% endhighlight %}

Next we need to specify the date. There is a "Specify Date" drop-down menu. Let us locate it. As usual we start by right-clicking the element and selecting "Inspect Element". That gives us the following HTML code:

{% highlight html %}
<select class="input" id="dateSelector1" style="vertical-align: top;" name="dateSelector1">
  <option value="">All available dates</option>
  <option value="0:DY">Today</option>
  <option value="is">Date is…</option>
  <option value="before">Date is before…</option>
  <option value="after">Date is after…</option>
  <option value="from">Date is between…</option>
  <option value="1:WK">Previous week</option>
  <option value="1:MO">Previous month</option>
  <option value="3:MO">Previous 3 months</option>
  <option value="6:MO">Previous 6 months</option>
  <option value="1:YR">Previous year</option>
  <option value="2:YR">Previous 2 years</option>
  <option value="5:YR">Previous 5 years</option>
  <option value="previous">Previous…</option></select>
{% endhighlight %}

We can see the element's name and id but here we will use neither. This is a drop-down menu and we will need to select one of its options ("All available dates", "Today", etc), so here we will use the element's xpath. How do you get it? We are using Chrome here, so this is really simple: we just right-click the blue-highlighted line that corresponds to the element's HTML code and select "Copy XPath". Like this:

[![](http://i.imgur.com/cUIAYCI.jpg)](http://imgur.com/cUIAYCI)

That gives us the following xpath:

{% highlight html %}
//*[@id="dateSelector1"]
{% endhighlight %}

Now, as usual, scroll up from the blue-highlighted line until you find out which frame contains the element. Here that is the same frame of "Search Terms" (i.e., "mainFrame"), so we are already there, no need to move.

If all we wanted were to locate the element, we would do this:

{% highlight python %}
browser.find_element_by_xpath('//*[@id="dateSelector1"]')
{% endhighlight %}

But we want to open that drop-down menu and select "Today". So we do this instead:

{% highlight python %}
browser.find_element_by_xpath('//*[@id="dateSelector1"]/option[contains(text(), "Today")]').click()
{% endhighlight %}

Now we've entered our search term (balloon) and selected our date (today). Next we need to select our news sources. That's another drop-down menu, a bit further down the page. You know the drill: right-click the element, retrieve relevant attributes, scroll up to find out the frame. There isn't anything new to learn here (and we haven't left "mainFrame" yet), so I'll just give you the code (let's say we want to select all news sources in English):

{% highlight python %}
browser.find_element_by_xpath('//*[@id="byType"]/option[text()="All News (English)"]').click()
{% endhighlight %}

Finally, we need to click the "Search" button (next to the "Search Terms" form) to submit the search. Same drill: right-click element, get attributes, scroll up to find frame. Except that here there is no id or name:

{% highlight html %}
<input type="submit" value="Search" />
{% endhighlight %}

So we need to use xpath again, even though this is not a drop-down menu:

{% highlight python %}
browser.find_element_by_xpath('//*[@id="searchForm"]/fieldset/ol/li[2]/span/span/input').click()
{% endhighlight %}

Now that is one ugly-looking xpath. Our code will look better if we use the element's CSS selector instead:

{% highlight python %}
browser.find_element_by_css_selector('input[type=\"submit\"]').click()
{% endhighlight %}

I don't know of any "copy-and-paste" way to get an element's CSS selector, but if you stare at the line above long enough you can see how it derives from the element's HTML code.

That's it. You should now see Chrome leaving the search page and opening the results page.

There is a lot more to cover, but that will have to wait.
