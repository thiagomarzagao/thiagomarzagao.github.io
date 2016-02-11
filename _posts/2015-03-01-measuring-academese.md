---
comments: true
layout: post
title: measuring academese
---

We all know that [academic writing stinks](http://chronicle.com/article/Why-Academics-Writing-Stinks/148989/), but exactly how bad is it? And in what disciplines does academic writing stink the most? To answer these questions I scraped 174,527 academic articles, came up with a few indicators of "academese" and compared these indicators across disciplines.

**our data source**

I scraped those articles from [SciELO](http://www.scielo.org/php/index.php). In case you've never heard of SciELO, it's like [JSTOR](https://www.google.com.br/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0CB0QFjAA&url=http%3A%2F%2Fwww.jstor.org%2F&ei=rujxVI_iMpaKsQSOnoH4Cw&usg=AFQjCNEXYivnJOqb_qrQBhcHcX8DSH0SAQ&bvm=bv.87269000,d.aWw), but focused on Latin American journals. I would rather have scraped JSTOR, but it's gated. I could scrape it using my [OSU](https://www.google.com.br/search?q=osu&oq=osu&aqs=chrome..69i57j69i60j69i65l3j69i60.1350j0j7&sourceid=chrome&es_sm=91&ie=UTF-8#q=ohio+state) credentials, but the [Aaron Swartz](http://en.wikipedia.org/wiki/Aaron_Swartz) brouhaha is not an encouraging precedent. Also, JSTOR articles are usually in PDF, which sucks for text mining (especially when the PDF is the scan of a document, which is often the case in JSTOR). SciELO, by contrast, is ungated (it doesn't even have a "terms of use" page, so I can't possibly be breaking any rules) and its articles are in HTML, which is much easier to parse than PDF.

Most articles on SciELO are in Portuguese or Spanish but that's not a problem here. The flaws of academic writing - cluttered sentences, meaningless words, plenty of jargon - are not language-specific. And thanks to the Normands the mumbo jumbo barely changes from one language to another: in English you problematize the discursive paradigm and in Portuguese *você problematiza o paradigma discursivo*.

**summary statistics**

The 174,527 articles I scraped are all the articles in Portuguese from all the 281 active journals on SciELO. Here's how they are distributed:

<iframe src="/assets/areas.html" width="800" height="400" frameborder="0" scrolling="no"></iframe>

We'll look into specific disciplines in a minute.

(SciELO doesn't categorize its journals, so the categorizations above are my own, partly based on [Latindex](http://www.latindex.unam.mx/)'s. In case you are curious, [here](https://gist.github.com/thiagomarzagao/322c9d6032ebee5697b5) are the journal ISSN codes and respective areas.)

**academese and how to measure it**

> ...the secret of good writing is to strip every sentence to its cleanest components. Every word that serves no function, every long word that could be a short word, every adverb that carries the same meaning that's already in the verb, every passive construction that leaves the reader unsure of who is doing what - these are the thousand and one adulterants that weaken the strength of a sentence. And they usually occur in proportion to education and rank. (William Zinsser, [On Writing Well](http://www.amazon.com/Writing-Well-30th-Anniversary-Edition/dp/0060891548).)

As we see, academese is not a particular type of bad writing. The same set of flaws that we've been calling academese could very well be called journalese or bureaucratese. The specific jargon may change (academics *critique*, bureaucrats *impact*) but the underlying sins are the same: clutter and vagueness.

Now that we know what bad writing is we can measure it. Here are my indicators:

- Word length.
- Sentence length.
- Adverbs/total number of words. To identify adverbs I use the 1,000 most frequent adverbs in the [Portuguese Corpus](http://www.corpusdoportugues.org/).
- Gerunds/total number of words. I count as a gerund any word that ends in 'ndo', which is how gerunds end in Portuguese - as in *fazendo* (doing), *escrevendo* (writing), etc.
- Inane words/total number of words. I don't have an exhaustive list of inane words. Instead I selected any words that match one of the following [regular expressions]((http://en.wikipedia.org/wiki/Regular_expression)):
    - `'^problematiz.*'`: *problematizar* (to problematize), *problematização* (problematization), etc.
    - `'^paradigma.*'`: *paradigma* (paradigme), *paradigmático* (paradigmatic), etc.
    - `'^discursiv.*'`: *discursivo* (discursive), *discursividade* (discursivity), etc.
    - `'^dial\u00E9tic.*'`: *dialética*, *dialético* (both mean dialectic), etc.
    - `'^critic.*'` and `'^cr\u00EDtic.*'`: *criticar* (to criticize), *crítico* (critical, critic), *criticado* (criticized), etc. You may have qualms about this but think: are people supposed to do anything *a-critically* in academia? If not then *critical* is inane unless we're talking about a specific disagreement (as in "Hayek criticized Keynes' monetary theory"). Elsewhere - "critical theory", "a critical look at", etc - *critical* is pointless.

I picked these words because they are not specific to any disciplines. Sociologists and physicists alike can talk about paradigmes, problematize phenomena, or take a critical look at theories and experiments. Sociologists and physicists may differ in how often they use such inane words (that's what I want to measure) but they both have the same opportunities to use them.

I considered enriching my list of inane words with words from Sokal's [hoax](http://www.physics.nyu.edu/sokal/transgress_v2/transgress_v2_singlefile.html) and from the [Bad Writing Contest](http://denisdutton.com/bad_writing.htm). But that might stack the deck against the humanities. Physicists probably don't have many chances to write *entelechy*, *otherness*, or *essentiality*.

I'd rather use a machine learning approach but I couldn't find a corpora of academic articles pre-labeled as academese/not academese (let alone one such corpora that happens to be in Portuguese). Hence what's left is this sort of "dictionary" approach, which is much weaker - I'm certainly missing A LOT of relevant features (and possibly using some irrelevant ones). But it'll have to do for now.

**so, who stinks the most?**

Here's the ratio inane words / total number of words:

<iframe src="/assets/inane.html" width="800" height="175" frameborder="0" scrolling="no"></iframe>

Adverbs / total number of words:

<iframe src="/assets/adverbs.html" width="800" height="175" frameborder="0" scrolling="no"></iframe>

Gerunds / total number of words:

<iframe src="/assets/gerunds.html" width="800" height="175" frameborder="0" scrolling="no"></iframe>

Average sentence length:

<iframe src="/assets/sentenceLength.html" width="800" height="175" frameborder="0" scrolling="no"></iframe>

Average word length:

<iframe src="/assets/wordLength.html" width="800" height="175" frameborder="0" scrolling="no"></iframe>

Clearly it's in the humanities and social sciences that academese really thrives. Not exactly a shocking finding, but it's nice to finally have some numbers. I didn't expect the difference in inane words usage to be so large. Conversely, I expected word length to vary a lot more (maybe scientific names are inflating word size in the hard sciences?).

**zooming in**

Let's zoom in on some of the humanities and social sciences. Here's our articles:

<iframe src="/assets/disciplines.html" width="800" height="500" frameborder="0" scrolling="no"></iframe>

Now let's see how these different disciplines compare. Here's the ratio inane words / total number of words:

<iframe src="/assets/inane2.html" width="800" height="275" frameborder="0" scrolling="no"></iframe>

Adverbs / total number of words:

<iframe src="/assets/adverbs2.html" width="800" height="275" frameborder="0" scrolling="no"></iframe>

Gerunds / total number of words:

<iframe src="/assets/gerunds2.html" width="800" height="275" frameborder="0" scrolling="no"></iframe>

Average sentence length:

<iframe src="/assets/sentenceLength2.html" width="800" height="275" frameborder="0" scrolling="no"></iframe>

Average word length:

<iframe src="/assets/wordLength2.html" width="800" height="275" frameborder="0" scrolling="no"></iframe>

Well, these are some disappointing data. I expected big differences - especially between pairs like economics and anthropology, or business and history. Turns out I was wrong. Sadly, there isn't a clear "worst offender" for us to shame. Philosophy wins (well, loses) when it comes to poor word choices, but not by much, and philosophers don't use longer sentences or words than the other social scientists.

**what's next**

This analysis is not language-specific - what makes bad writing bad is the same set of flaws in English and in Portuguese. But perhaps this analysis is culture-specific? For instance, what passes for economics in Brazil is much different than what we find on the American Economic Review - there is a lot more "problematization of paradigms" in the tropics, so to speak. So I wonder how things would change if I used American articles instead. I'm not going to scrape any gated databases, lest I get in legal trouble. But maybe Google Scholar searches might contain enough ungated results? Or maybe there is some (large enough) ungated database that I don't know of?

**the gory details**

Here's the code I used to scrape SciELO, in case it may be useful to you. (Please, [be considerate](http://lethain.com/an-introduction-to-compassionate-screenscraping/). SciELO is super nice to us scrapers: it's ungated, there are no captchas, everything is in plain HTML, and - crucially - they don't prohibit scraping. So don't overparallelize or otherwise disrupt their servers.)

{% highlight python %}
import os
import re
import requests
from bs4 import BeautifulSoup

# get URL of each journal (active journals only)
startURL = 'http://www.scielo.br/scielo.php?script=sci_subject&lng=pt&nrm=iso'
session = requests.Session()
startHTML = session.get(startURL).text
soup = BeautifulSoup(startHTML)
regex = re.compile(soup.find_all('p')[4].text) # regex to filter out non-active journals
sections = soup.find_all(text = regex)
journalURLs = []
for i in range(len(sections)):
    newSection = sections[i].next_element.find_all('a')
    newJournalURLs = [URL.get('href') for URL in newSection]
    journalURLs += newJournalURLs
basepath = '/Users/thiagomarzagao/Desktop/articles/' # change as needed

# go to each journal
for i, journalURL in enumerate(journalURLs):
    print 'journal num:', i + 1, 'de', len(journalURLs)
    k = 1
    IDstart = journalURL.index('pid=')
    IDend = journalURL.index('&lng')
    journalID = journalURL[IDstart+4:IDend]
    print 'journal id:', journalID    
    journalPath = basepath + journalID + '/'
    if os.path.exists(journalPath):
        continue
    else:
        os.makedirs(journalPath)
    journalStartHTML = session.get(journalURL.replace('serial', 'issues')).text
    journalSoup = BeautifulSoup(journalStartHTML)

    # go to each issue
    issuesURLs = [URL.get('href') for URL in journalSoup.find_all('a')[10:-3]][:-2]
    for n, issueURL in enumerate(issuesURLs):
        print 'issue num:', n + 1, 'de', len(issuesURLs)
        if issueURL:
            if 'pid=' in issueURL:
                issueStartHTML = session.get(issueURL).text
                issueSoup = BeautifulSoup(issueStartHTML)
                articlesURLs = [URL.get('href') for URL in issueSoup.find_all('a', text = u'texto em  Portugu\u00EAs')]
                if len(articlesURLs) > 0:

                    # go to each article and scrape it
                    for articleURL in articlesURLs:
                        articleHTML = session.get(articleURL).text
                        articleSoup = BeautifulSoup(articleHTML)
                        articleTextList = [p.text for p in articleSoup.find_all('p')]
                        articleText = ''
                        for piece in articleTextList:
                            articleText += piece

                        # save article to disk
                        with open(journalPath + str(k) + '.txt', mode = 'wb') as fbuffer:
                            fbuffer.write(articleText.encode('utf8'))
                        k += 1
{% endhighlight %}

The code above will yield a little garbage: a few articles not in Portuguese and some texts that are not articles (copyright notices mostly). Not enough garbage to be worth fixing though.

To parse the sentences I used the following regular expression, which I stole from [here](http://stackoverflow.com/questions/5553410/regular-expression-match-a-sentence).

{% highlight python %}
regex = re.compile("[^.!?\\s]" +
                   "[^.!?]*" +
                   "(?:" +
                   "  [.!?]" +
                   "  (?!['\"]?\\s|$)" +
                   "  [^.!?]*" +
                   ")*" +
                   "[.!?]?" +
                   "['\"]?" +
                   "(?=\\s|$)", 
                   re.MULTILINE)
{% endhighlight %}

To make the pie charts I used [d3pie](http://d3pie.org/), which is amazing tool: you make the charts interactively and d3pie generates the code for you. (That sort of defeats the purpose of these posts, which is to help me practice [D3](http://d3js.org/), but it was just so quick and easy that I couldn't resist.) To make the bar charts I just used plain D3. Here's the code for the first bar chart (the code is almost the same for the others):

{% highlight html linenos %}
<!DOCTYPE html>
<meta charset="utf-8">
<style>

.axis path, .axis line {
    fill: none;
    stroke: black;
}

.axis text {
    font-family: sans-serif;
    font-size: 16px;
}

#tooltip {
    position: absolute;
    width: auto;
    height: auto;
    padding: 10px;
    background-color: white;
    -webkit-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
    -moz-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
    box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
    pointer-events: none;
}

#tooltip.hidden {
    display: none;
}

#tooltip p {
    margin: 0;
    font-family: sans-serif;
    font-size: 16px;
    line-height: 20px;
}

</style>
<body>

<div id="tooltip" class="hidden">
    <p><span id="value">100</span>
    </p>
</div>

<script src="d3/d3.min.js"></script>
<script>

var margins = {
    top: 12,
    left: 150,
    right: 24,
    bottom: 24
},
legendPanel = {
    width: 0
},
width = 500 - margins.left - margins.right - legendPanel.width + 150,
    height = 136 - margins.top - margins.bottom,
    dataset = [{
        data: [{
            month: 'humanities & social',
            count: 0.00080
        }, {
            month: 'biological & earth',
            count: 0.00012
        }, {
            month: 'exact',
            count: 0.00017
        }],
        name: ''
    }

    ],
    series = dataset.map(function (d) {
        return d.name;
    }),
    dataset = dataset.map(function (d) {
        return d.data.map(function (o, i) {
            // Structure it so that your numeric
            // axis (the stacked amount) is y
            return {
                y: o.count,
                x: o.month
            };
        });
    }),
    stack = d3.layout.stack();

stack(dataset);

var dataset = dataset.map(function (group) {
    return group.map(function (d) {
        // Invert the x and y values, and y0 becomes x0
        return {
            x: d.y,
            y: d.x,
            x0: d.y0
        };
    });
}),
    svg = d3.select('body')
        .append('svg')
        .attr('width', width + margins.left + margins.right + legendPanel.width)
        .attr('height', height + margins.top + margins.bottom)
        .append('g')
        .attr('transform', 'translate(' + margins.left + ',' + margins.top + ')'),
    xMax = d3.max(dataset, function (group) {
        return d3.max(group, function (d) {
            return d.x + d.x0;
        });
    }),
    xScale = d3.scale.linear()
        .domain([0, xMax])
        .range([0, width]),
    months = dataset[0].map(function (d) {
        return d.y;
    }),
    yScale = d3.scale.ordinal()
        .domain(months)
        .rangeRoundBands([0, 100], .1),
    xAxis = d3.svg.axis()
        .ticks(5)
        .scale(xScale)
        .orient('bottom'),
    yAxis = d3.svg.axis()
        .scale(yScale)
        .orient('left'),
    colours = d3.scale.category10(),
    groups = svg.selectAll('g')
        .data(dataset)
        .enter()
        .append('g')
        .style('fill', function (d, i) {
        return colours(i);
    }),
    rects = groups.selectAll('rect')
        .data(function (d) {
        return d;
    })
        .enter()
        .append('rect')
        .attr('x', function (d) {
        return xScale(d.x0);
    })
        .attr('y', function (d, i) {
        return yScale(d.y);
    })
        .attr('height', function (d) {
        return yScale.rangeBand();
    })
        .attr('width', function (d) {
        return xScale(d.x);
    })
        .on('mouseover', function (d) {
        var xPos = parseFloat(d3.select(this).attr('x')) / 2 + width / 2;
        var yPos = parseFloat(d3.select(this).attr('y')) + yScale.rangeBand() / 2;

        d3.select('#tooltip')
            .style('left', xPos + 'px')
            .style('top', yPos + 'px')
            .select('#value')
            .text(d.x);

        d3.select('#tooltip').classed('hidden', false);
    })
        .on('mouseout', function () {
        d3.select('#tooltip').classed('hidden', true);
    })

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);

svg.append('g')
    .attr('class', 'axis')
    .call(yAxis);

series.forEach(function (s, i) {
    svg.append('text')
        .attr('fill', 'white')
        .attr('x', width + margins.left + 8)
        .attr('y', i * 24 + 24)
        .text(s);
    svg.append('rect')
        .attr('fill', colours(i))
        .attr('width', 60)
        .attr('height', 20)
        .attr('x', width + margins.left + 90)
        .attr('y', i * 24 + 6);
});

</script>
</body>
{% endhighlight %}

This is it!