---
comments: true
layout: post
title: personal pronouns in Brazilian Portuguese
---

While English doesn't have a singular *you* (unless you count *thou*), Portuguese has two: *tu* and *você*, with *tu* being preferred in some regions and *você* being preferred in others. A while ago an American friend who is learning Portuguese asked me where exactly people used one form or the other and, despite Portuguese being my first language, I couldn't give her a proper answer. So, to atone for my unhelpfulness (and because I needed an excuse to start playing with [D3](http://d3js.org/)) I scraped 680,045 geolocated tweets from Brazil and made the map below, where the higher the *tu*/*você* ratio the "redder" the state and the lower the *tu*/*você* ratio the "bluer" the state. Hover the mouse on the map to see the state names and respective ratios and number of tweets.

<iframe src="/assets/map1.html" width="800" height="700" frameborder="0" scrolling="no"></iframe>

As we see, all states prefer *você* over *tu* - not a single state has a *tu*/*você* ratio higher than 1. And that preference is strong: in all states but one *você* is at least twice as popular as *tu* (i.e., the ratios are no higher than 0.5). The exception is Rio Grande do Sul (the purple, southernmost state), where the contest is close, with a *tu*/*você* ratio of 0.88. Which fits the popular perception of *gaúchos* (as natives from Rio Grande do Sul are often called) having a culture that is heavily influenced by the surrounding Spanish-speaking countries (*tu* is singular *you* in Spanish as well).

Other than in Rio Grande do Sul *tu* is most popular in Santa Catarina (*tu*/*você* ratio of 0.47), Maranhão (0.42), Amapá (0.35), Pará (0.30), and Roraima (0.30). Santa Catarina is in the South (it borders Rio Grande do Sul) while the other four states are in the North and Northeast. *Você*, on the other hand, is most popular in Sergipe (0.05), Minas Gerais (0.06), Goiás (0.06), Mato Grosso do Sul (0.08), Mato Grosso (0.08), São Paulo (0.08), and Espírito Santo (0.09) - basically the entire Southeast and Midwest regions.

I got curious to know how exactly people use *tu*. You see, conjugation is a tricky business in Romance languages. In English I go, you go, he/she/it goes, we go, you go, they go - the verb almost never changes. But in Portuguese *eu vou* (I go), *tu vais* ("singular you" go), *você vai* ("singular you" go), *ele/ela vai* (he/she/it goes), *nós vamos* (we go), *vós ides* ("y'all" go), *vocês vão* ("y'all" go), *eles/elas vão* (they go). The verb almost always changes. And as this example shows, *tu* and *você* call for different verb inflections: *tu* **_vais_** but *você* **_vai_**.

Or so Portuguese grammar dictates. But grammar rules are one thing and what people actually say are another. At least where I'm currently living (Brasília), when people use *tu* they often conjugate it as *você*: *tu vai* instead of *tu vais*; *tu foi* ("singular you" went) instead of *tu foste*; and so on. So, when people use *tu* do they conjugate it correctly?

Turns out they don't. Out of the 680,045 tweets I scraped *tu vai* appears in 6,559 of them while *tu vais* appears in a mere 77 - too few to even allow state-wise comparisons.

Which is probably ok. By merging the conjugation rules of *tu* and *você* we simplify Portuguese grammar. Old English conjugation was hard: *ic hæbbe* (I have), *þū hæfst* (thou hast), *hē/hit/hēo hæfð* (he/it/she has), *wē/gē/hīe habbaþ* (we/"y'all"/they have) - and that's just the nominative case; there were also the accusative, dative, and genitive cases, each calling for different verb inflections. But over the centuries English grammar got simplified and now conjugation is pretty straightforward - and I don't see anyone complaining about that. Portuguese still needs to undergo a similar process. The less school time we spend learning arbitrary verb inflections the more time we can spend learning useful stuff.

In case this discussion has awaken your inner etymologist you may like to know that *tu* and *thou* are cognate - they both come from the same Proto-Indo-European word. And both have declined for the same reason: people were looking for less intimate ways to refer to one another. The English solution was to imitate the French by using the plural pronoun (*you*). The Portuguese solution was to imitate the Spanish by using Your Mercy - *Vuestra Merced* in Spanish, *Vossa Mercê* in Portuguese. *Vossa Mercê* is a bit cumbersome to say, so eventually people slurred it into *você* (just like Spanish speakers eventually slurred *Vuestra Merced* into *usted*).

(Btw, if you are into etymology you should check Kevin Stroud's [The History of English Podcast](http://historyofenglishpodcast.com/). It's amazing to the point where I don't even mind being stuck in traffic anymore.)

It would be interesting to know how usage of *tu* and *você* varies in other Portuguese-speaking countries, but only Brazil has a population big enough to yield 600k geolocated tweets each containing *tu* and/or *você* in under a week. It would also be interesting to know how *tu* and *você* usage has varied over time - in particular, when exactly *você* overtook *tu* as the most popular choice. But there was no Twitter before the 21st century (and Google Books N-Gram Viewer doesn't have a Portuguese corpus).

Some caveats are in order. First, there may be intra-state variation. But for most cities there are too few tweets and I'd rather not say anything about how the people from this or that city speak based on only a handful of tweets. So, state capitals and other large cities are overrepresented here. Second, you need internet access and a device of sorts (a cell phone at least) in order to tweet, so the really poor are excluded from this analysis. There is some [evidence](https://repositorio.ufba.br/ri/bitstream/ri/8422/1/Viviane%20Gomes%20de%20Deus.pdf) that usage of *tu* declines with income, so I'm probably underestimating *tu* usage here. Third, people don't necessarily tweet the same way they speak. For instance, perhaps the people of Rio Grande do Sul write *tu* more often than they speak it.
 
If you want the gory details, I used Twitter's [sample stream](https://dev.twitter.com/streaming/reference/get/statuses/sample), which is a continuous stream of a small random sample of all tweets, in JSON format. Programming-wise I used Python's [Tweepy](http://www.tweepy.org/). Here's my code (minus access key, token secret, etc; you can create your own Twitter-scraping credentials [here](https://apps.twitter.com/)):

{% highlight python %}
import tweepy
 
consumer_key = "YourConsumerKey"
consumer_secret = "YourConsumerSecret"
access_token = "YourAccessToken"
access_token_secret = "YourTokenSecret"
 
class listener(tweepy.streaming.StreamListener):
    def on_data(self, data):
        print data
        return True
        
    def on_error(self, status):
        print status
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
 
while True:
    try:
        twitterStream = tweepy.Stream(auth, listener())
        twitterStream.filter(track = [u"voc\u00EA", 
                                      u"voce",
                                      u"vc",
                                      u"tu"])
    except:
        continue
{% endhighlight %}

This code will simply scrape the tweets and show them on your screen but won't save them. To save, you need to point the stdout to some output file, as in: `python scrapeTwitter.py > output.csv`.

As you can see from the code, I limited my scraping to posts containing *tu*, *você*, *voce*, or *vc* (a common shorthand for *você* in Portuguese). The Twitter API [doesn't care about case](https://dev.twitter.com/streaming/overview/request-parameters#track), so that also yielded *Tu*, *TU*, *vC*, etc.

I also used Python to parse the tweets:

{% highlight python %}
import os
import re
import json
import pandas as pd

# folder containing the files of scraped tweets; change as needed
path = '/Users/thiagomarzagao/Desktop/tweets/' 

# regex to remove some non-standard characters
vanilla = u'[^\u0041-\u005A \
              \u0061-\u007A \
              \u00C0-\u00D6 \
              \u00D8-\u00F6 \
              \u00F8-\u00FF \
              \u0100-\u017F \
              \u0020]'
regex = re.compile(vanilla)

# spelling variations of 'voce'
voces = set([u'voce', u'voc\u00EA', u'vc'])

# parse everything
tweets = []
f = 0
n = 0
for fname in os.listdir(path):
    if '.json' in fname:
        f += 1
        with open(path + fname, mode = 'rb') as fbuffer:
            for record in fbuffer:
                try:
                    if len(record) > 1:
                        jsondata = json.loads(record)
                        if 'place' in jsondata:
                            if jsondata['place']:
                                if jsondata['place']['country_code'] == 'BR':
                                    if jsondata['place']['place_type'] == 'city':
                                        n += 1
                                        print 'f:', f, fname
                                        print 'n:', n
                                        lowercased = jsondata['text'].lower()
                                        cleaned = regex.sub(' ', lowercased)
                                        splitted = cleaned.split()
                                        tu = False
                                        voce = False
                                        tuvais = False
                                        tuvai = False
                                        if 'tu' in splitted:
                                            tu = True
                                        for v in voces:
                                            if v in splitted:
                                                voce = True
                                        if 'tu vais' in cleaned:
                                            tuvais = True
                                        if 'tu vai ' in cleaned:
                                            tuvai = True
                                        location = jsondata['place']['full_name']
                                        comma = location.index(',')
                                        city = location[:comma].encode('utf8')
                                        state = location[comma + 2:].encode('utf8')
                                        if state == 'Brasil':
                                            state = city
                                        if state == 'Brazil':
                                            state = city
                                        tweet = (tu, voce, tuvais, tuvai, city, state)
                                        tweets.append(tweet)
                                        print cleaned.encode('utf8')
                except:
                    continue
                    
df = pd.DataFrame(tweets)
colnames = ['tu', 'voce', 'tuvais', 'tuvai', 'city', 'state']
df.to_csv('/Users/thiagomarzagao/Desktop/tweets.csv', # destination of tabulated data; change as needed
          index = False, 
          header = colnames)
{% endhighlight %}

(You may want to comment out line 67 - `print cleaned.encode('utf8')`. Otherwise every tweet you scraped will show on your screen as it is parsed. That can make you lose faith in mankind.)

To make the choropleth (the fancy word for a map whose colors vary according to data) I initially considered [plotly](https://plot.ly/), but as it turns out they don't handle maps natively and I didn't like the [workarounds](http://nbviewer.ipython.org/github/etpinard/plotly-misc-nbs/blob/etienne/plotly-maps.ipynb) I found. So I turned to [D3](http://d3js.org/). It's not very intuitive, especially if you're used to making your plots in R, Matlab, or Stata. You have to juggle three languages - JavaScript, HTML, and CSS - to get your plot to work and that can be confusing in the beginning. But it got the job done. The map itself was originally in shapefile format and I used Carolina Bigonha's [br-atlas](https://github.com/carolinabigonha/br-atlas) to convert it to [Topojson](https://github.com/mbostock/topojson) format.

Below is the code I used to produce the choropleth. Here I only have 27 observations, so I didn't mind hardcoding the data for each of them. But if you have more observations (say, counties) you probably want to automate the process by having a function map *tu*/*você* ratios to the RGB color spectrum.

{% highlight html %}
<!DOCTYPE html>
<meta charset="utf-8">
<style>

.uf:hover {fill-opacity: 0.5;}

.uf.MS {fill: rgb(19,0,235);}
.uf.SC {fill: rgb(81,0,173);}
.uf.ES {fill: rgb(21,0,233);}
.uf.AC {fill: rgb(43,0,211);}
.uf.RS {fill: rgb(119,0,135);}
.uf.MT {fill: rgb(20,0,234);}
.uf.RR {fill: rgb(59,0,195);}
.uf.PB {fill: rgb(35,0,219);}
.uf.PI {fill: rgb(44,0,210);}
.uf.GO {fill: rgb(16,0,238);}
.uf.RN {fill: rgb(28,0,226);}
.uf.RJ {fill: rgb(34,0,220);}
.uf.PR {fill: rgb(24,0,230);}
.uf.AP {fill: rgb(66,0,188);}
.uf.SP {fill: rgb(20,0,234);}
.uf.DF {fill: rgb(37,0,217);}
.uf.BA {fill: rgb(26,0,228);}
.uf.PA {fill: rgb(59,0,195);}
.uf.PE {fill: rgb(55,0,199);}
.uf.MA {fill: rgb(75,0,179);}
.uf.TO {fill: rgb(31,0,223);}
.uf.CE {fill: rgb(42,0,212);}
.uf.RO {fill: rgb(48,0,206);}
.uf.AM {fill: rgb(57,0,197);}
.uf.SE {fill: rgb(13,0,241);}
.uf.MG {fill: rgb(15,0,239);}
.uf.AL {fill: rgb(27,0,227);}

#tooltip {
    position: absolute;
    width: auto;
    height: auto;
    padding: 5px;
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
    <p><strong></strong></p>
    <p><strong><span id="value"></span></strong></p>
    <p><span id="value2"></span></p>
    <p><span id="value3"></span></p>
</div>

<script src="d3/d3.min.js"></script>
<script src="topojson.v1.min.js"></script>
<script>

uf_dictionary = {"50": ["MS", "Mato Grosso do Sul", "0.08", "5,126"],
                 "42": ["SC", "Santa Catarina", "0.47", "45,222"],
                 "32": ["ES", "Espírito Santo", "0.09", "16,977"],
                 "12": ["AC", "Acre", "0.20", "1,871"],
                 "43": ["RS", "Rio Grande do Sul", "0.88", "83,133"],
                 "51": ["MT", "Mato Grosso", "0.08", "3,202"],
                 "14": ["RR", "Roraima", "0.30", "1,287"],
                 "25": ["PB", "Paraíba", "0.16", "3,941"],
                 "22": ["PI", "Piauí", "0.20", "1,364"],
                 "52": ["GO", "Goiás", "0.06", "8,512"],
                 "24": ["RN", "Rio Grande do Norte", "0.12", "3,663"],
                 "33": ["RJ", "Rio de Janeiro", "0.15", "152,458"],
                 "41": ["PR", "Paraná", "0.10", "43,169"],
                 "16": ["AP", "Amapá", "0.35", "1,672"],
                 "35": ["SP", "São Paulo", "0.08", "175,077"],
                 "53": ["DF", "Distrito Federal", "0.17", "15,218"],
                 "29": ["BA", "Bahia", "0.11", "10,649"],
                 "15": ["PA", "Pará", "0.30", "8,544"],
                 "26": ["PE", "Pernambuco", "0.27", "19,362"],
                 "21": ["MA", "Maranhão", "0.42", "3,540"],
                 "17": ["TO", "Tocantins", "0.14", "961"],
                 "23": ["CE", "Ceará", "0.20", "9,864"],
                 "11": ["RO", "Rondônia", "0.23", "2,017"],
                 "13": ["AM", "Amazonas", "0.29", "10,864"],
                 "28": ["SE", "Sergipe", "0.05", "2,198"], 
                 "31": ["MG", "Minas Gerais", "0.06", "47,396"],
                 "27": ["AL", "Alagoas", "0.11", "2,767"]};

var width = 960,
    height = 650

var projection = d3.geo.mercator()
    .translate([325, 250])
    .center([-53.12, -10.20])
    .scale(900);
    
var path = d3.geo.path()
    .projection(projection);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

function idToStr(d) {
        return uf_dictionary[d];
};

d3.json("br-states.json", function(error, mymap) {
    svg.selectAll(".uf")
        .data(topojson.feature(mymap, mymap.objects.states).features)
        .enter()
        .append("path")
        .attr("class", function(d) {return "uf " + idToStr(d.id)[0];})
        .attr("d", path)
        .on("mouseover", function(d) {
            var coordinates = [0, 0];
            coordinates = d3.mouse(this);
            var x = coordinates[0] + 10;
            var y = coordinates[1] + 10;
            d3.select("#tooltip")
                .style("left", x + "px")
                .style("top", y + "px")
                .select("#value")
                .text(idToStr(d.id)[1])
            d3.select("#tooltip")
                .style("left", x + "px")
                .style("top", y + "px")
                .select("#value2")
                .text("tu/você ratio: " + idToStr(d.id)[2])
            d3.select("#tooltip")
                .style("left", x + "px")
                .style("top", y + "px")
                .select("#value3")
                .text("tweets: " + idToStr(d.id)[3])
            d3.select("#tooltip").classed("hidden", false);
            })
       .on("mouseout", function() {
            d3.select("#tooltip").classed("hidden", true);
            });
});

</script>
</body>
{% endhighlight %}

That's it. More map-based posts should follow.