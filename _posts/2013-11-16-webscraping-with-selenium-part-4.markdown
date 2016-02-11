---
comments: true
layout: post
title: webscraping with Selenium - part 4
---

I've assumed that you know a bit of programming, so you are probably familiar with loops and conditional expressions. I won't cover these (or any) general programming concepts, but I want to discuss two specific points. The first one is the importance of pacing your bot. The second one is how to iterate over searches on LexisNexis Academic. This second point is really about LexisNexis, not about webscraping in general, so you can safely skip it if that's not the site you want to webscrape.

<strong>the importance of pacing</strong>

Your computer can fetch online content much faster than you can, so it's tempting to just release the beast (i.e., your bot) into the wild and let it move full speed ahead. But that's a dead giveaway. You want your bot to pass for a human but if it moves at blazing-fast speeds that may set off all kinds of alarms with the administrators of the website (or with the bots they've built to do detect enemy bots). 

Hence you need to pace things. To do that just insert a `time.sleep(seconds)` statement between each iteration of the loop. Do a few searches manually first, see how long it takes, and use that information to set `seconds` in a way that slows your bot down to human speed.

Better yet: make `seconds` partially random. Something like this:

{% highlight python %}
import random

seconds = 5 + (random.random() * 5)
time.sleep(seconds)
{% endhighlight %}

`random.random()` will generate a random number between 0 and 1. So we are randomizing the delay between searches, which will vary between 5 and 10 seconds. That looks a lot more like human activity than a uniform delay. Try doing 100 searches with exactly 5 seconds between them. You can't. And if you can't do it then you don't want your bot to do it.

"Then why would I want to webscrape in the first place? If the bot can't go faster than I can then what's the point? I could simply manually fetch all the content I want." You could and you should, if that's at all feasible. Building a webscraping bot can take a couple of weeks, depending on the complexity of the website and on whether you have done this before. If fetching everything manually would take only a couple of minutes then there is little reason to do it programmatically.

Webscraping is for when fetching everything manually would take days or weeks or months. But even then you won't necessarily be done any faster. It may still take weeks or months or years for your bot to do all the work (well, hopefully not years). The key point is: webscraping is not about finishing faster, it's about freeing you to work on other, more interesting, tasks. While your bot is hard at work on LexisNexis or Factiva or any other site you are free to work on other parts of your dissertation, finish a conference paper, or binge-watch House of Cards on Netflix.

Also, fetching online content manually is error-prone. If you are doing it programmatically everything is transparent: you have the code, hence you know exactly what searches were performed. You can also log any errors, as we saw in part 3, so if something went wrong you will know all about it: day, hour, search expression, button clicked, etc. 

But if you're doing things manually how can you be sure that you did search for Congo Brazzaville and not for Congo Kinshasa instead? Imagine how tired and bored you will be by day #10. Do you really trust yourself not to make any typos? Or not to skip a search? You can hire undergrads to do the work, but if _you_ can can make mistakes while doing it then imagine people who have no stake whatsoever in your research results.

So, even if your bot doesn't go any faster than you would you will still be better off with it.

All that said, in part 5 (coming soon) we will see that you can actually make things go faster - if you have multiple bots. But that's dangerous in a number of ways you need to know about all the dangers first. So hang in there.

<strong>looping over searches on LexisNexis Academic</strong>

Back in part 1 we submitted a search on LexisNexis Academic. We searched for all occurrences of the word "balloon" in the news that day. In part 2 we went to the results page and saw that there were 121 results. We then wrote some code to retrieve those 121 results.

That was all fine and dandy for introductory purposes but the thing is, that code only works when the number of results is between 1 and 500. If there are 0 results we don't get the results page, we get this page instead:

[![](http://i.imgur.com/b7srGv0.jpg)](http://imgur.com/b7srGv0)

Selenium will look for the 'fr_resultsNav...' frame (remember that?), won't find it and will throw a `NoSuchElementException`.

Conversely, if there are over 3000 results we get this page instead:

[![](http://i.imgur.com/73x5lJt.jpg)](http://imgur.com/73x5lJt)

Same as before: Selenium will look for the 'fr_resultsNav...' frame, won't find it  and will throw a `NoSuchElementException`.

Finally, if the number of results is between 501 and 3000 the code from part 2 will work fine up to the point where  the "Download" or "Send" button is clicked (according to whether you are downloading the results or having LexisNexis email them to you). Then LexisNexis will give you an error message.

[![](http://i.imgur.com/n1ay2XS.jpg)](http://imgur.com/n1ay2XS)

Yep, we can only retrieve 500 results at a time. The code from part 2 tries to download/email "All Documents". But here we have 587 results, so we can't do that.

You can see where this is going: you will need to branch your loop in order to account for those different scenarios.

Selenium-wise there is nothing new here so I won't give you all the code, just pieces of it.

_Scenario #1: no results_

We need to locate the "No Documents Found" message that we get when there are no results. You already know how to find page elements (see part 1 if you don't). But we can't simply use `browser.find_element_by_`. If we do and we are _not_ on the "no results" page Selenium will fail to find the "No Documents Found" message and the code will crash. Hence we need to encapsulate `browser.find_element_by_` inside a `try/except` statement. If the "No Documents Found" element is found then we click "Edit Search" (top of the page) and move on to the next search. Otherwise we have one or more results and hence we need to move on to the results page.

Here's some pseudocode for that (say we know the id of the element).

{% highlight python %}
try:
    # element_id = id of "No Documents Found" element
    browser.find_element_by_id(id)
    # click "Edit Search"
    # move on to next search
except NoSuchElementException:
    # move on to the results page
{% endhighlight %}

This works. It's not the most elegant solution though. Not hitting the "no results" page is not exactly an error. So it feels weird to treat it as such.

Selenium doesn't have a "check if element exists" method, but we can emulate one. Something like this:

{% highlight python %}
def exists_by_id(id):
    try:
        browser.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True
{% endhighlight %}
(I stole this code from [here](http://stackoverflow.com/a/12150013/2453555).)

I know, we didn't get rid of the `try/except` statement. But at least it is now contained inside a function and we don't have to see it every time we need to check for some element's existence based on its id.

You can write similar functions for other identifiers (name, xpath, etc). You can also write a more general function where you pass the identifier as an argument. Whatever suits your stylistic preferences.

You may want to log any searches that yield no results.

_Scenario #2: more than 3000 results_

This is similar to "no results" scenario, with only two differences. First, we need to look for the "More than 3000 Results" message (rather than the "No Documents Found" message); as before, we need to look for that message in a "safe" way, with a `try/except` statement or a user-defined function. Second, we have the option to go back and edit the search or proceed to the results page. 

We can choose the latter by clicking the "Retrieve Results" button. But caution: when there are more than 3000 results the results page will only give us 1000 results. I don't know what criteria LexisNexis uses to select those 1000 results (I asked them but they never bothered to reply my email). Depending on what you intend to do later you may want to consider issues of comparability and selection bias.

_Scenario #3: 1-3000 results_

If we are neither on the "no results" page nor on the "3000+ results" page then our first step is to retrieve the total number of results. 

That number is contained in the `totalDocsInResult` object, as attribute "value". Here is the object's HTML code:

{% highlight html %}
<input type="hidden" name="totalDocsInResult" value="587">
{% endhighlight %}

`totalDocsInResult`, in turn, is contained inside the `fr_resultsNav...` frame that we already saw in part 2, which in turn is inside 'mainFrame'. We already know how to move into `fr_resultsNav...` (see part 2). Once we are there extracting the total number of results is straightforward.

{% highlight python %}
total = int(browser.find_element_by_name('totalDocsInResult').get_attribute('value'))
{% endhighlight %}

(`totalDocsInResult` stores the number as a string, so we need to use `int()` to convert it to a number.)

If we have between 1 and 500 results nothing changes and we can use the code from part 2. But if we have between 501 and 3000 results that code won't work, since we can only retrieve 500 results at a time. We need to iterate over batches of 500 results if we have 501-3000 results. Here is some starter code.

{% highlight python %}
if total > 500:
    initial = 1
    final = 500
    batch = 0
    while final <= total and final >= initial:
        batch += 1
        browser.find_element_by_css_selector('img[alt=\"Email Documents\"]').click()
        browser.switch_to_default_content()
        browser.switch_to_window(browser.window_handles[1])
        browser.find_element_by_xpath('//select[@id="sendAs"]/option[text()="Attachment"]').click()
        browser.find_element_by_xpath('//select[@id="delFmt"]/option[text()="Text"]').click()
        browser.find_element_by_name('emailTo').clear()
        browser.find_element_by_name('emailTo').send_keys(email)						
        browser.find_element_by_id('emailNote').clear()
        browser.find_element_by_id('emailNote').send_keys('balloon')
        browser.find_element_by_id('sel').click()
        browser.find_element_by_id('rangetextbox').clear()
        browser.find_element_by_id('rangetextbox').send_keys('{}-{}'.format(initial, final))
        browser.find_element_by_css_selector('img[alt=\"Send\"]').click()
        try:
            element = WebDriverWait(browser, 120).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[alt=\"Close Window\"]')))
        except TimeoutException:
            log_errors.write('oops, TimeoutException when searching for balloon' + '\n')
            time.sleep(30)
            browser.close()
        initial += 500
        if final + 500 > total:
            final = total
        else:
            final += 500
        backwindow = browser.window_handles[0]
        browser.switch_to_window(backwindow)
        browser.switch_to_default_content()
        browser.switch_to_frame('mainFrame')
        framelist = browser.find_elements_by_xpath('//frame[contains(@name, 'fr_resultsNav')]')
        framename = framelist[0].get_attribute('name')
        browser.switch_to_frame(framename)
{% endhighlight %}

Lines 1-5 create the necessary accumulators and start the loop. Lines 16-18 fill out the "Select Items" form, which we didn't need in part 2 (we had fewer than 500 results, so just selected "All Documents"). Line 19 clicks the "Send" button. 

As before, once we click "Send" LexisNexis will shove the results into a text file and email it. Generating that file may take a while. The more so since we are now selecting 500 results, which is a lot. It may take a whole minute or so before the "Close Window" button finally appears on the pop-up. 

That's why we need the explicit wait you see in lines 20-25 (see part 3 if this is new to you). If the "Close Window" button takes over two minutes to appear we close the pop-up by brute force (and we hope that the file with the results was generated and sent correctly).

Lines 26-30 update the accumulators and lines 31-37 take us back to the results page.

Naturally this entire loop will be inside the big loop that iterates over your searches. I won't give you any code for that outer loop, but really it's simpler than the inner loop above.

Here I only used an explicit wait for the "Close Window" button but of course you will want to sprinkle explicit waits whenever you feel the need (i.e., whenever your code crashes while trying to locate an element or interact with it). Review part 3 if needed.

That's about it for now. On the next post we will cover headless browsing and parallel webscraping.

([Part 5](http://thiagomarzagao.com/2013/11/17/webscraping-with-selenium-part-5/))