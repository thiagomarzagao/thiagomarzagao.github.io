---
comments: true
layout: post
title: finding books to read
---

Despite all the hype about AI, product recommendations still suck. Amazon offers me the exact same Bose headphones I bought last month, plus two hundred close substitutes. Spotify thinks that because I enjoy Eurodance from the 1990s I will also enjoy Brazilian music from the 1990s. Netflix thinks that because I enjoy *Black Mirror* I will also enjoy *Dear White People* - and that's despite Netflix knowing that I'm a fan of *Rick & Morty*, *South Park*, and any show that has Ricky Gervais. Goodreads thinks that because I enjoyed *Ready Player One* I will also enjoy *Spell or High Water* even though I've already read *Spell or High Water* and rated it only one star on Goodreads itself. No wonder there is zero peer-reviewed evidence that Cambridge Analytica swayed even a single voter in 2016. The singularity is nowhere near.

I could write to each of those companies or annoy them on Twitter or whatnot. But I believe in the DIY ethic.

<a href="https://twitter.com/balajis/status/753773388452073472"><img src="http://i.imgur.com/bSSLQNn.png"></a>

I chose to start with [Goodreads](https://www.goodreads.com/). It has by far the most egregious recommender system. And you hear people talk about their favorite TV shows or self-tracking wristbands all the time but you don't always get to hear people talk about their favorite books.

**"do the simple thing first"**

I used something called *user-based collaborative filtering*, which is fancy language for "find other people who like the sort of stuff you like and then check what else they also like."

<img src="https://i.imgur.com/dLLfttR.jpg">

There are lots of ways to do user-based collaborative filtering. Some algorithms only require grade school math while others rely on deep learning. (Aggarwal's [Recommender Systems](https://www.amazon.com/Recommender-Systems-Textbook-Charu-Aggarwal-ebook/dp/B01DK3GZDY/) is by far the best textbook on the subject that I know of, in case you're interested.) Here I used something that only requires grade school math and can't even be called an "algorithm": cosine similarity.

But before I talk about cosine similarity let me talk about the data we need to collect in order to use it.

**scraping**

You start by collecting, for every item you ever rated, all other ratings it has received. And you also collect the identity (name or user ID) of all the other raters - all the people who have rated items in common with you. So I had to collect, for each book I ever rated on Goodreads, all other ratings that book received on Goodreads, along with the user IDs of the other raters.

Unfortunately, Goodreads doesn't let us see *all* the ratings each book has received. Goodreads lets us see the full distribution of ratings: forty thousand 5-star ratings, twenty thousand 4-star ratings, and so on (see below). But it doesn't let us see all the ratings themselves. And if I can't see a rating I can't know whose rating it is, so for our purposes here it might as well not exist.

<a href ="https://www.goodreads.com/book/show/1760630.Self_Reliance"><img src="https://i.imgur.com/UqXIdO6.png"></a>

How many ratings does Goodreads let us see? If you visit a book's page - say, [Ender's Game](https://www.goodreads.com/book/show/375802.Ender_s_Game) page - you immediately see up to 30 ratings (fewer if it's an obscure book that not even 30 people have bothered to rate). If the book has more than 30 ratings you can click "next" on the bottom of the page and that shows you 30 more ratings. You can keep clicking "next" until you get to page ten, which means you can get up to 300 ratings in total. That's regardless of the book's popularity: it can be *Pride and Prejudice*, which has 2.3 million ratings, and you still won't be able to see beyond page ten.

<img src="https://i.imgur.com/wEI5NzD.png">

Now, we can bypass that limit - to a point. We can filter the contents and ask to see just 1-star ratings or just 2-star ratings and so on. And each time we will get back up to ten pages (of 1-star ratings or 2-star ratings or whatever else we chose). Goodreads ratings go from 1 to 5 stars, integers only, so in practice this filtering lets us multiply five-fold the total number of ratings we can collect for each book: we increase it from 300 to 1500.

<img src="https://i.imgur.com/l1aRzxv.png">

We can even go beyond 1500. See the "Sort" button in the above picture? We can sort the ratings from older to newer or from newer to older. Either way we still get back up to ten pages. So we can get 1500 ratings sorted from older to newer and then get 1500 ratings sorted from newer to older. That way we end up with 3000 ratings (some - or all - of which will be duplicates when the book is not popular enough to have received more than 3000 ratings in total).

I didn't do the sorting thing though. It only occurred to me after I had done everything and I'm in no mood to go back and redo everything. So what I have is only up to 1500 ratings per book. Sorry, reviewer #2.

Alrigh then, enough talk. Here is the Python code I wrote to get all the ratings I ever gave on Goodreads. I used Selenium and Chrome. If you're new to scraping then here's a [tutorial](/resources#selenium). You don't need to be logged in to scrape Goodreads (though that reduces the size of the data a little: some Goodreads users choose to make their profiles available only to people who are logged in).

{% highlight python %}
import time
import pickle
from selenium import webdriver
from bs4 import BeautifulSoup

# initialize browser
path_to_executable = '/path/to/chromedriver'
browser = webdriver.Chrome(path_to_executable)

# get my own reviews
my_url = 'https://www.goodreads.com/review/list/123456789-your-user-id-here?print=true'
browser.get(my_url)
time.sleep(5)
source = browser.page_source
soup = BeautifulSoup(source, 'lxml')

# get total number of pages
pagination_div = soup.find('div', {'id': 'reviewPagination'})
page_links = pagination_div.find_all('a')
last_page = page_links[-2] # page_links[-1] is "next >>"
total_pages = int(last_page.text)
print('total_pages:', total_pages)

my_reviews = {}
for page in range(1, total_pages + 1):

    # get page and extract table that contains the reviews
    new_page = my_url + '&page=' + str(page)
    browser.get(new_page)
    time.sleep(5)
    source = browser.page_source
    soup = BeautifulSoup(source, 'lxml')
    table = soup.find('table', {'id': 'books'})
    rows = table.find_all('tr', class_ = 'bookalike review')

    # for each review get book title, link, and my rating
    for i, row in enumerate(rows):
        title_column = row.find('td', class_ = 'field title')
        title = title_column.find('a').text
        href = title_column.find('a')['href']
        rating_column = row.find('td', class_ = 'field rating')
        rating_div = rating_column.find('div', class_ = 'value')
        rating_span = rating_div.find('span', class_ = 'staticStars')
        if rating_span.has_attr('title'):
            my_rating = rating_span['title']
            my_reviews[str(page) + '_' + str(i)] = (title, href, my_rating)

with open('my_reviews.pkl', mode = 'wb') as f:
    pickle.dump(my_reviews, f)
{% endhighlight %}

And here is the code I wrote to scrape all the ratings of every book I've ever rated. Now, this code takes a while to run - it's getting every rating of every book I ever read -, so I used Chrome in [headless mode](https://developers.google.com/web/updates/2017/04/headless-chrome).

{% highlight python %}
import time
import pickle
from selenium import webdriver
from bs4 import BeautifulSoup

# load my own reviews
with open('my_reviews.pkl', mode = 'rb') as f:
    my_reviews = pickle.load(f)

# get book URLs
book_endpoints = [e[1] for e in my_reviews.values()]

# initialize browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('log-level=3')
chrome_options.add_experimental_option('prefs', {'profile.default_content_setting_values.automatic_downloads': 1})
executable_path = '/path/to/chromedriver'
browser = webdriver.Chrome(executable_path = executable_path, chrome_options = chrome_options)

# get book reviews
all_reviews = {}
for i, book_endpoint in enumerate(book_endpoints):
    print(' ')
    print(i, book_endpoint)

    # get book id
    if '.' in book_endpoint:
        book_id = int(book_endpoint[11:book_endpoint.index('.')])
    elif '-' in book_endpoint:
        book_id = int(book_endpoint[11:book_endpoint.index('-')])
    else:
        book_id = book_endpoint[11:]

    # create empty list to store book's reviews
    all_reviews[book_id] = []

    source = ''

    # iterate through all possible ratings (1-5)
    for rating in range(1, 6):
        print('rating:', rating)

        # get source code of book's first page and soupify it
        browser.get('https://www.goodreads.com' + book_endpoint + '?rating=' + str(rating))
        time.sleep(5)
        source = browser.page_source
        soup = BeautifulSoup(source, 'lxml')

        page = 1
        while True:

            # get divs that contain the reviews
            reviews = soup.find_all('div', class_ = 'review')

            for review in reviews:

                # get endoint of reviewer's URL
                reviewer = review.find('a', class_ = 'user')['href']

                # get text
                text_div = review.find('div', class_ = 'reviewText stacked')
                if text_div:
                    text = text_div.find('span', class_ = 'readable').text
                else:
                    text = None

                # store review
                all_reviews[book_id].append((reviewer, rating, text))

            print('page:', page, 'book reviews:', len(set(all_reviews[book_id])))

            # go to next page
            if '<a class="next_page"' in source:
                try:
                    element = browser.find_element_by_partial_link_text('next ')
                    browser.execute_script("arguments[0].click();", element)
                    while browser.page_source == source:
                        time.sleep(1)
                    source = browser.page_source
                    soup = BeautifulSoup(source, 'lxml')
                    page += 1
                except:
                    print('"next" present but couldnt click it')
                    break
            else:
                print('no "next" element')
                break

with open('raters.pkl', mode = 'wb') as f:
    pickle.dump(all_reviews, f)
{% endhighlight %}

On Goodreads you can give a star-based rating, as we've discussed, but you can also write a review about the book. The code above gets these reviews too. I won't use them here, but I may in a future blog post (it might be fun to inspect the adjectives most frequently associated with each book).

**les data**

In total I got 292,043 ratings from 197,548 different Goodreads users. That's all from 357 books, which is the number of books I had rated by the time I did this. That's all the data I need to find people who like the same sort of stuff I like.

In fact, that's actually *more* data than I need. I have to discard everyone with whom I have only *one* book in common (more about that in a minute). After doing that I'm left with 43,825 raters and the following distribution:

<img src="https://i.imgur.com/gAg7oti.png">

As you see, the vast majority of these users have only a couple of books in common with me: they are concentrated in the 2-10 range of the X axis. Only a few users have rated more than 10 books in common with me. The maximum is 68 books. That's <a href="https://www.goodreads.com/user/show/1413439-stephen">Stephen</a>.

Turns out Stephen and I have a similar sci-fi taste. We're both into the classics - Heinlein, Bradbury, Asimov - and into more recent authors like Neal Stephenson, Charles Stross, and Ted Chiang. We're both also into economic and moral philosophy: Friedman, Hayek, Emerson, Nietzsche.

But no, I can't just go after the books Stephen has read and I haven't. Life is not so simple. His interests are far more diverse than mine: he's into horror, fantasy, comics, crime, and dozens of other genres, whereas I can go a whole year reading nothing but sci-fi. I've only read 2% of the books he's read, but he's read 24% of the books I've read. So it's not like Stephen and I are "book twins", it's just that Stephen reads *a lot*, so inevitably he will look like many people's "book twin" at first glance.

Not to mention that our ratings don't necessarily coincide. For instance, Stephen is much more indulgent with slow-paced novels than I am. He 4-starred Olaf Stapledon's *Last and First Men* and C.J. Cherryh's *Downbelow Station*, both of which I abandoned after just a few chapters. I like books that hook you from the very first paragraph.

> The moon blew up without warning and for no apparent reason. (Seveneves, Neal Stephenson)

> I did two things on my seventy-fifth birthday. I visited my wife's grave. Then I joined the army. (Old Man's War, John Scalzi)

> Lolita, light of my life, fire of my loins. (Lolita, Vladimir Nabokov)

There are other complications but I'm getting ahead of myself. For now I just want to find *potentially* similar people, not evaluate each of them. Stephen is a potential *neighbor* - to use the jargon of user-based collaborative filtering -, but we won't know for sure until much later. Keep reading.

There's one complication I need to mention right now though. When I check Stephen's profile on Goodreads I can see that we actually have rated 93 books in common, not 68. My dataset is lying to me. Why? Well, remember how I only got up to 1500 ratings for each book because Goodreads doesn't let us see all the ratings? Turns out that for 25 of those 93 books Stephen's ratings were not in the (up to) 1500 ratings I scraped for each book. Hence those 25 ratings didn't make it into the dataset.

I could fix that by scraping each rater's profile and checking all the books we *actually* have in common. But with 43,825 raters that would take forever. I could parallelize the scraping - have, say, 43k bots scrape ~1k raters each. But Goodreads would surely understand that as an attack and block my IP address. I could get around that by using proxies or remote servers but that's a lot more effort than I'm willing to put into this. Sorry again, reviewer #2.

Alright, time to go back to the question I left hanging before: why did I have to drop users with only one book in common with me? To answer that I need to (finally) explain cosine similarity. 

**cosine similarity**

Say we arrange the scraped data in a matrix where each column represents a book, each row represents a user, and each cell represents how many stars that user rated that book. Here I have 43,825 users and 357 books, so that's a 43,825 by 357 matrix.

(Most users won't have rated most books, so most of the cells are `NULL` or `None` or whatever null-like representation you prefer. It can't be zero though - that would later be interpreted as a rating of zero stars -, so this isn't really a sparse matrix, it's something else. I don't know that it has a specific name.)

Now suppose I pluck two arbitrary (row) vectors from that matrix and, in these vectors, I keep only the columns corresponding to books that *both* users have rated (i.e., I drop all columns corresponding to books that only one or neither user has rated). If you project the resulting two vectors onto an Euclidian space there will be an angle between them. 

<img src="https://i.imgur.com/7X7xrsZ.png"> Here's the thing: *the cosine of that angle is a measure of how similar the two vectors are*. Ta-da. Now you know what cosine similarity means.

<iframe src="https://giphy.com/embed/OK27wINdQS5YQ" width="480" height="338" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
<br>

A concrete example might help.

Let's pluck two users from our matrix: myself and someone else. Say, [Geneva](https://www.goodreads.com/user/show/10228399-geneva). We have rated a total of five books in common according to the dataset. Here are our ratings for those five books:

| book | Geneva | Thiago |
| <a href="https://www.goodreads.com/book/show/16690">The Moon is a Harsh Mistress</a> | 4 | 2 |
| <a href="https://www.goodreads.com/book/show/22328">Neuromancer</a> | 3 | 3|
| <a href="https://www.goodreads.com/book/show/830">Snow Crash</a> | 4 | 5 |
| <a href="https://www.goodreads.com/book/show/509784">The End of Eternity</a> | 4 | 5 |
| <a href="https://www.goodreads.com/book/show/13330370">The Last Policeman</a> | 4 | 5 |

These are our two vectors then: [4, 3, 4, 4, 4] (Genevas' ratings) and [2, 3, 5, 5, 5] (my ratings).

The first step here is to compute the *Euclidean norm* of each vector. It's not hard: for each vector you square every element, you sum up all these squares, then you take the square root of that sum. So for Geneva's vector the norm is \\(\sqrt{4^2 + 3^2 + 4^2 + 4^2 + 4^2}\approx 8.54\\). For my own vector the norm is \\(\sqrt{2^2 + 3^2 + 5^2 + 5^2 + 5^2}\approx 9.38\\).

Next we divide each vector's element by the vector's norm. Hence Geneva's vector becomes \\([\frac{4}{8.54}, \frac{3}{8.54}, \frac{4}{8.54}, \frac{4}{8.54}, \frac{4}{8.54}]\\) = [0.46, 0.35, 0.46, 0.46, 0.46] and mine becomes \\([\frac{2}{9.38}, \frac{3}{9.38}, \frac{5}{9.38}, \frac{5}{9.38}, \frac{5}{9.38}]\\) = [0.21, 0.31, 0.53, 0.53, 0.53].

Finally, the cosine itself. It's just the dot product of those two vectors: 0.46(0.21) + 0.35(0.31) + 0.46(0.53) + 0.46(0.53) + 0.46(0.53) = 0.09 + 0.10 + 0.24 + 0.24 + 0.24 \\(\approx\\) 0.93.

How similar are the two vectors if the cosine of their angle is 0.93? They are about as similar as they can be: for any two vectors of our Goodreads matrix the cosine will be in the 0-1 range. The closer to 0, the more different the two vectors are. The closer to 1, the more similar.

(Before the math police come after me: "in abstract" a cosine can vary from -1 to +1. But in our Goodreads matrix we only have nonnegative values; Goodreads doesn't let you rate a book negative stars. So here the cosine between any of our two vectors has to be in the 0 to +1 range.)

*If I compute the cosine between my own vector and every other vector in our matrix then I'll know which users are most similar to me, book-wise.*

Perhaps now you can see why I dropped users who only had one book in common with me. An angle cannot exist between two points, only between two vectors. And I need at least two points to form one vector.

Note that I have only considered the five books that Geneva and I have both rated. We can't compute the cosine between two vectors that are not the same size. If I add a sixth book that'll be a book that either only Geneva has rated or only I have rated or neither of us has rated. We'd have one vector with six elements and one vector with five elements (no, we can't input zero or any other value to fill the gap). That wouldn't work.

Another thing to keep in mind is that, as I explained before, I only got up to 1500 ratings for each book, so the number of books I have in common with each of the other Goodreads users is actually higher than what's in the dataset. I checked Geneva's profile and it turns out that we share 21 books, not five. So by computing the cosines between my ratings and everyone else's ratings I get a *rough idea* about who my closest neighbors *probably* are; I don't get a precise, 100% accurate ranking of my closest neighbors.

**too many book twins**

So I sat down and computed the cosine similarity between me and every other person on my Goodreads dataset. (Well, actually I sat down and wrote code to do that for me.)

Turns out there are lots of people for whom cosine=1, the maximum possible value. But no, I don't have lots of book twins out there. The problem is: a cosine of 1 is pretty common when the two vectors are short.

Take user [Ajay](https://www.goodreads.com/user/show/9530007-ajay), for instance. We have two books in common: *How to Lie with Statistics* and *Skin in the Game*. He rated both 5 stars. I rated both 3 stars. If you do the math you'll find a cosine of 1. Or take [Derek](https://www.goodreads.com/user/show/5982358-derek-bridge). We also have two books in common: *The Signal and the Noise* and *Neuromancer*. He rated them 3 and 2 stars respectively. I rated them 4 and 3 stars respectively. Cosine is also 1.

Let's put this in perspective. Remember Stephen? Our cosine similarity is 0.93. Now that's a guy with whom I share 68 books. Should Ajay and Derek rank higher than Stephen on my similarity ranking? I don't think so. I'd much rather read a book suggested by Stephen than a book suggested by Ajay or Derek.

Alright then, should I drop everyone with fewer than, say, ten books in common with me? Nope. Not all books are equally important. The two books I share with Ajay and the two books I share with Derek are all pretty popular. Lots of people have read them, most of which are certainly not in my tribe. Now what if I had only two books in common with someone but those two books were, say, David Wingrove's *[The Middle Kingdom](https://www.goodreads.com/book/show/296382.The_Middle_Kingdom)* and John Ringo's *[Live Free or Die](https://www.goodreads.com/book/show/6713634-live-free-or-die)*?

<img src="https://i.imgur.com/Fk35oiw.png">

That would be a different story. Those two books are excellent but little known. *The Middle Kingdom*, published in 1989 - back when China's GDP was 3.8% of what it is today -, shows a future where history has been rewritten and schoolchildren learn that the Chinese have been ruling the world since general Ban Chao (an [actual person](https://en.wikipedia.org/wiki/Ban_Chao)) destroyed the Roman Empire in the first century AD. *The Middle Kingdom* makes *Lord of the Rings* and *Game of Thrones* seem juvenile and unimaginative. And yet it has only 1.3k ratings on Goodreads. *Live Free or Die*, in turn, is about a guy named Tyler Vernon. Earth has been conquered by an alien race - the Horvath. Tyler sells maple syrup to other alien races (it works as a mixture of cocaine and aphrodisiac for them). He then uses the money to buy alien military technology and fight back against the Horvath. It's great, unapologetic, libertarian sci-fi - government fails to fight off hostile aliens, private sector steps up; it's Robert Heinlein meets Ayn Rand. And yet only 7.3k brave souls have rated it on Goodreads.

My point is: if I only have two books in common with you and these two books are *The Middle Kingdom* and *Live Free or Die* then I definitely want to hear your book recommendations. Those two books are too good and too obscure. Reading them certifies you as the sort of weirdo I want to get book recommendations from. That's why I can't simply drop people with whom I have only two or three books in common. They may be the right books.

We can think about it from a probabilistic perspective. The fact you've read *The Middle Kingdom* and *Live Free or Die* tells me more about you than the fact that you've read, say, *Ender's Game*. Don't get me wrong, I love *Ender's Game* - it's on my top 5 list of all-time favorites. But nearly a million people have rated *Ender's Game* on Goodreads. The more popular the book, the more diverse its readers. Surely there are Ender's Game readers who enjoy boring novels like *Anne of Green Gables* or *The Handmaid's Tale*. You telling me that you've read *Ender's Game* doesn't tell me much about what type of reader you are. Same with *Ready Player One*, *Snow Crash*, and *World War Z*: excellent books, but so popular that they attract all sorts of people, including lots of people I absolutately *don't* want to get book recommendations from. In probabilistic terms, P(good recommendations\|has read The Middle Kingdom) > P(good recommendations\|has read World War Z).

What to do then?

**measuring how weird you are**

The solution is to use something called Inverse User Frequency (IUF). Here is how it works. Goodreads has ~65 million users. *To Kill a Mockingbird* has been rated by 3.6 million users. So its IUF is log(65/3.6) \\(\approx\\) 2.8. *The Middle Kingdom*, on the other hand, has been rated by only 1.3k users. So its UDF is log(65/0.0013) \\(\approx\\) 10.8. So, *The Middle Kingdom* is almost four times weirder than *To Kill a Mockingbird* (without taking the log the differences would be too extreme; we want to take the book's popularity into account but not too much). (If you're familiar with natural language processing you will notice this is similar to Inverse Document Frequency.)

So instead of computing raw cosine similarities we are going to compute *weighted* cosine similarities, with each rating being weighted by the IUF of the corresponding book.

To give a concrete example, let's go back to Geneva. Here are the IUFs of the books we have in common.

| book | raters | IUF |
| The Moon is a Harsh Mistress | 91k | 6.5 |
| Neuromancer | 216k | 5.7 | 
| Snow Crash | 200k | 5.7 |
| The End of Eternity | 34k | 7.5 |
| The Last Policeman | 20k | 8 |

Now that we have the IUFs we incorporate them in the cosine computation.

$$ \dfrac{0.09(6.5) + 0.10(5.7) + 0.24(5.7) + 0.24(7.5) + 0.24(8.0)}{6.5 + 5.7 + 5.7 + 7.5 + 8.0}\\
\approx 0.15$$

That's more like it. The books I have in common with Geneva are pretty popular and that's reflected in our similarity going down from 0.93 to 0.15. Good. Now, the decrease is not as drastic as it seems. Weighting by IUF makes all cosine similarities smaller. Let's go back to the hypothetical example of someone with whom I share two books and they are *The Middle Kingdom* and *Live Free or Die*. If that other person has rated both 4 and I have rated both 5 then our raw cosine similarity is 1 but our weighted cosine similarity is only 0.5.

**still doesn't quite feel like my tribe...**

<a href="https://twitter.com/balajis/status/753773388452073472"><img src="https://i.imgur.com/3dv9TzW.jpg"></a>

I adjusted the cosine similarities to account for the IUF, looked into the people with the highest similarity scores and... things were still a bit odd. When I looked into the top 10 folks and the books they've rated - and what their ratings were - I just couldn't quite picture myself taking book recommendations from them in real life (like, if I had met them at a café). I know, this is super wishy-washy, but I'm sure you get the idea.

Turns out I had neglected to take into consideration that some people are just more generous and forgiving than others. Some people have a mean rating of 4.5 while others have a mean rating of 2.5. So we need to *mean-center* people's ratings before we compute the similarity scores. As in: if your mean rating is 2.5 and you rated *Snow Crash* 4 stars then I'll actually consider it 1.5 stars when computing our cosine similarity.

So, I redid everything but mean-centering the ratings.

**did it work?**

Well, we can't answer that question just yet. First we need to answer another question: how do we know how good (or bad) the results are?

Turns out there is a simple metric for that. I can use the similarities I generated to "predict" my own ratings for books I have already rated, then compare the predicted ratings to my actual ratings.

Say I take Stephen and Geneva, which we've encountered before. Stephen rated Neal Stephenson's *Snow Crash* five stars. Geneva rated it four stars. My similarity with Stephen is 0.93. My similarity with Geneva is 0.15. So if I wanted to use only Stephen and Geneva to produce a prediction, I could make it $$\dfrac{5(0.93) + 4 (0.15)}{0.93 + 0.15} = 4.86$$. In other words, I could use a weighted average of Stephen's and Geneva's ratings to "predict" what my own rating of *Snow Crash* would be (the weights being our respective similarities). My actual rating of *Snow Crash* is five stars, which is pretty close to 4.86. 

I can do this operation for all books I ever rated. And then I can check how close my predicted ratings and my actual ratings are. How can we measure that? Hhmm, if only there was a way to compare the similarity of two vectors... Oh wait, there is: cosine similarity. So I use cosine similarity twice: first to compute user-user similarities, then to assess the quality of the predictions those similarities produce. What a handy tool.

Now, here I don't want to use all Goodreads users I scraped. The whole point of this exercise is to find my tribe, i.e., the people whose literary tastes are most similar to mine. That's the folks I want to get book recommendations from. So I have to define a threshold - say, my top 100 or my top 10000 most similar users. And then I predict the ratings for the books I have rated in common with these top *k* people - my top *k* "neighbors", as textbooks refer to them.

There is a trade off in choosing *k*. The higher the *k* the more neighbors you have to get predictions from, so the more books you have predictions for. But the higher the *k* the more you get predictions from neighbors who are not so close to you. Here I tried a bunch of different values for *k* and it turns out that *k*=1000 seemed like a good compromise.

Now we're ready to the answer the original question: how good are the results? Turns out the cosine similarity between my predicted ratings and my actual ratings, using my top 1000 neighbors, is 0.91 (after adding back the mean, which we removed before - remember?). Since cosines vary from 0 to 1, that seems pretty good. Looks like I've finally found my tribe.

<img src="https://i.imgur.com/2Mv5KWJ.jpg">

**so what?**

Ok, so how do we generate book recommendations? Well, I just "predicted" what my ratings would be for books I have already rated. That's how I assessed the quality of the similarities. (That's how we assess any predictive model: we "predict" things that have already happened, then check how right or wrong those "predictions" are.) 
Now, to get actual book recommendations I simply predict what my ratings will be for books I have *not* rated and I pick the books which I'm predicted to rate highly. So this time I will *predict* without quotes: what I'm predicting hasn't happened yet.

I went back to my top 1000 neighbors and scraped their ratings for every book they have ever rated (and that I never did). Then I predicted what my own rating would be for each one of those books.

That resulted in a ranking of 29,335 books. Here are the top 12:

- Jim Butcher's [Storm Front](https://www.goodreads.com/book/show/47212.Storm_Front). This is the first of a series of books, several of which were in the top 100. I had never heard of it before. I'm not really into the fantasy genre, but I guess I'll give it a try.

- Brandon Sanderson's [The Way of Kings](https://www.goodreads.com/book/show/7235533-the-way-of-kings). Another first book of a fantasy series I had never heard of.

- Carl Sagan's [Cosmos](https://www.goodreads.com/book/show/55030.Cosmos). I've seen the Neil deGrasse Tyson show and I loved it, so I'm surely going to read this.

- Brian Vaughan and Fiona Staples' [Saga](https://www.goodreads.com/book/show/15704307-saga-vol-1). I've never read a graphic novel before and I never thought I would, but I guess there is a first time for everything.

- Terry Pratchett's [The Color of Magic](https://www.goodreads.com/book/show/34497.The_Color_of_Magic). Yet more fantasy. This one I had seen around but the book description hadn't appealed to me.

- Mario Puzo's [The Godfather](https://www.goodreads.com/book/show/22034.The_Godfather). Ok, this probably should have been in my want-to-read shelf already.

- Yuval Harari's [Sapiens](https://www.goodreads.com/book/show/23692271-sapiens). At one point I had this book in my want-to-read shelf but then I read Harari's other book, [Homo Deus](https://www.goodreads.com/book/show/31138556-homo-deus), and I didn't really enjoy it, so I gave up on Sapiens. I guess I'll put it back there now.

- Brandon Sanderson's [The Final Empire](https://www.goodreads.com/book/show/68428.The_Final_Empire). Yet more fantasy I had never heard of.

- David Weber's [On Basilisk Station](https://www.goodreads.com/book/show/35921.On_Basilisk_Station). Now, that's what I'm talking about! Finally some sci-fi in my recommendations. This is probably the one I'll read first.

- Patrick Rothfuss' [The Name of the Wind](https://www.goodreads.com/book/show/186074.The_Name_of_the_Wind). More. Freaking. Fantasy. This one I had seen around before but the title is so uninspiring that I never even bothered to read the book's description.

- Dostoyevsky's [The Brothers Karamazov](https://www.goodreads.com/book/show/4934.The_Brothers_Karamazov). Not sure what to do about this one. I endured Tolstoy's *Anna Karenina* and *War and Peace* and from what I've heard Dostoyevsky is similarly soporific. I may not have the fortitude to go through this one.

- J.J. Benítez' [Jerusalén](https://www.goodreads.com/book/show/66632.Jerusal_n). This one I read before - some 25 years ago, as a kid. (But I rated a different edition on Goodreads, so it ended up on my recommendations here.) This was the first book about time travel I ever read and I absolutely loved it. Now, my thirteen-year-old self was not a particularly discriminating reader. So I think I'll pass. I don't want to ruin the good memories I have of it.

And voilà, I have built and used my own book recommender system.

These results are less exciting than I expected. I don't understand all the fantasy books. I've read a fantasy novel here and there but I've read all of Asimov's Robot, Empire, and Foundation novels, most Neal Stephenson books, a lot of Robert Heinlein and John Scalzi - so why the heck is there only *one* sci-fi book in my top 12 recommendations?

I guess some of the oddities may be due to my including non-fiction books when computing the cosine similarities. The fact that you and I have both read Daron Acemoglu's *Economic origins of dictatorship and democracy* and William Greene's *Econometric analysis* and Luciano Ramalho's *Fluent Python* may result in a high similarity score but that doesn't mean we like the same stuff when it comes to fiction. Dropping non-fiction books might improve the results. That would require going through each of my books and flagging them as either fiction and non-fiction, then redoing everythig I've done here, so I'm not doing it. You and I will just have to live with that, reviewer #2.

But there is a lot more room for improvement here - it's not just about dropping non-fiction books. Let's talk about some possibilities.

**what next?**

If you're building a recommender system on top of cosine similarity or some other such metric the way to go about it is to tweak the similarity formula in all sorts of ways - give more weight to this or that, etc -, check how good or bad the resulting predictions are in each case, then pick the formula that yields the best predictions. I did a little tweaking here (IUF, mean-centering), but if you're serious about it you should try a lot more.

Besides, there are other ways to build recommender systems that don't rely on hard-coded similarity formulas. For instance, we could use linear regression to *learn* the weight each neighbor should have. We'd still end up with a weighted average for the predictions, but the weights would have been learned from the data.

Alternatively we could use algorithms like random forest, support vector machine, or neural network. These algorithms have one big advantage over a linear regression: they learn weird relationships between the variables you have. It could be, for instance, that I'm unlikely to enjoy books that are recommended by both Stephen and Geneva but likely to enjoy books that are recommended only by Geneva and not by Stephen or vice-versa. Or that I'm super likely to enjoy a book recommended by Peter only if his rating is exactly five stars and all other ratings are exactly one star. Linear regression won't capture any of that unless you know beforehand what these oddities are and model them explicitly. But random forest, SVM, and neural networks can learn those oddities from the data and incorporate them into their predictions. The drawback is that if you don't have a lot of data these algorithms can easily mistake noise for signal and incorrectly pick up idiosyncrasies.

You could also use clustering algorithms, like k-means or DBSCAN. They work by grouping (clustering) samples (in our case, those would be Goodreads users) together according to their similarities.

Now, using linear regression, random forest, SVM, neural network, or clustering requires overcoming a problem: missing data. Here my top 1000 neighbors don't have a single book that they all have rated in common. There are too many missing data points to run a regression or do anything of the kind. So before doing any of that you'll need to either impute the missing data points or use matrix factorization to reduce the dimensionality of your dataset. The exception is k-means, which is relatively straightforward to adapt for use with massive missing data (see the Aggarwal book I mentioned before, chapter 12).

An alternatively that bypasses the missing data issue entirely is to model the data as a big *graph*, which is just fancy data science jargon for a *network*, like Facebook or Twitter: you have nodes (people and pages) and links between them (A follows B, A is friends with B, etc). Here we could model each Goodreads user as a node and each rating that two users have in common as a link between them. Then we could use a class of algorithms known as *community detection algorithms* to find what the "cliques" are.

Here I was just building a recommender system for myself, for the fun of it, so I'm not going to do any of that. But if you're doing something serious with it then you probably should try at least some of these alternatives and see which one yields the best predictions.

---

This is it. Happy reading!

> Outside of a dog, a book is man's best friend. Inside of a dog it's too dark to read. (Groucho Marx)
