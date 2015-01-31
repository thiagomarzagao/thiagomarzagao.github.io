---
comments: true
layout: post
title: webscraping with Selenium - part 3
---

In part 2 we learned how to handle dynamic names and how to download content with Selenium. Here we will learn how to make our code robust to network flukes.

<strong>handling errors</strong>

When you run a regression multiple times the result is always be the same, provided that the data and code you are using are the same. You run it a million times and there it is, same result. In other words, the result is deterministic.

With webscraping, however, the result is probabilistic. Sometimes a page element doesn't load properly. Sometimes the servers are too busy to respond to a click. Sometimes your own internet connection flickers for a millisecond. And so on.

In LexisNexis, for instance, sometimes you get this:

[![](http://i.imgur.com/wCRHdgJ.jpg)](http://imgur.com/wCRHdgJ)

In these cases Selenium will fail to find the elements you want and will crash. Selenium will throw out error messages like `NoSuchElementException` or `NoSuchFrameException`. If you've tried the code from parts 1 and 2 you may have encountered these errors already. It's not that the code is wrong, it's just that it is incomplete; we haven't prepared it for network flukes. Let's do it now.

One thing we can do is ensure that Selenium waits for a few seconds before it gives up on finding elements. There are different ways to do that. First there is the implicit wait statement:

{% highlight python %}
browser.implicitly_wait(30)
{% endhighlight %}

This statement makes Selenium wait up to 30 seconds before throwing an exception. You set the time limit once in your code and it is valid for the entire session.

Alternatively, you can set individual wait parameters for each action. To do that we first need to import a bunch of other stuff from the Selenium bindings:

{% highlight python %}
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException
{% endhighlight %}

Now suppose that we want to wait for up to two minutes before we declare an element "missing". Let's say that the element is a button and that we know its CSS selector. We can do this:

{% highlight python %}
some_object = WebDriverWait(browser, 120).until(EC.element_to_be_located((By.CSS_SELECTOR, 'img[alt=\"Some Button\"]')))
{% endhighlight %}

Selenium will look for the element every 500 milliseconds and, as soon as the element is found, the wait is over. If 120 seconds elapse and the element hasn't been found, Selenium throws a `TimeoutException`.

You need to decide what to do about the `TimeoutException`. Do you re-try a couple of times? Do you go back to the search page and move on to the next search? That of course depends on your particular research needs. But whatever path you choose you want your code to handle that exception gracefully. In Python that is done with `try/except` statements, like this:

{% highlight python %}
try:
    some_object = WebDriverWait(browser, 120).until(EC.element_to_be_located((By.CSS_SELECTOR, 'img[alt=\"Some Button\"]')))
except TimeoutException:
    # do something (retry, move on, exit, curse your internet provider, etc)
{% endhighlight %}

That way your code won't crash when Selenium throws a `TimeoutException`. It will do whatever is inside the `except` statement instead.

Here we used the `element_to_be_located` condition, but that is not always what we need. Sometimes the element is located but cannot be interacted with (yet). Selenium offers wait conditions for several different possibilites. For instance, sometimes the element is located but Selenium crashes and the error message says that the element is not clickable. In that case we can do something like this:

{% highlight python %}
try:
    some_object = WebDriverWait(browser, 120).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[alt=\"Some Button\"]')))
except TimeoutException:
    # do something
{% endhighlight %}

The full gamut of wait conditions is [here](http://selenium.googlecode.com/svn/trunk/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html).

Deciding what elements to (explicitly) wait for, with what conditions, and for how long is a trial-and-error process. Run your code without any waits first and see where it crashes. Add a wait condition for the problematic element, encapsulate the wait condition within a `try/except` statement, and run the code again. Repeat until your code doesn't crash anymore.

This is often a frustrating process and you'll need patience. You think that you've covered all the possibilities and your code runs for an entire week and you are all happy and celebratory and then on day #8 the damn thing crashes. The servers went down for a millisecond or your Netflix streaming clogged your internet connection or whatnot. It happens.

It's always a good idea to log errors. You can create a log file in the beginning of your code, like this:

{% highlight python %}
path_to_log = '/Users/yourname/Desktop/'
log_errors = open(path_to_log + 'log_errors.txt', mode = 'w')
{% endhighlight %}

And then add an entry to that file every time you get a `TimeoutException`:

{% highlight python %}
try:
    some_object = WebDriverWait(browser, 120).until(EC.element_to_be_located((By.CSS_SELECTOR, 'img[alt=\"Some Button\"]')))
except TimeoutException:
    log_errors.write('couldnt locate button XYZ when searching for "balloon"' + '\n')
    # do something
{% endhighlight %}

Once your code has finished running you can inspect the log file and see what searches you need to re-do.
