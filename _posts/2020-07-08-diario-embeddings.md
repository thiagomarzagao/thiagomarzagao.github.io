---
comments: true
layout: post
title: word embeddings for bureaucratese
---

You can find pre-trained word embeddings for hundreds of different languages - FastText alone has pre-trained embeddings for 157 languages (see [here](https://fasttext.cc/docs/en/crawl-vectors.html)). But a single language can come in multiple "flavors". I'm not talking about dialects, but about the different vocabulary and writing styles you find in news articles vs social media vs academic papers, etc. Most word embeddings come from a limited number of sources, with Wikipedia and news articles being the most common ones. If you have, say, social media texts, using word embeddings trained on Wikipedia entries may not yield good results.

So I decided to train my own Brazilian Portuguese word embeddings on the source that interests me the most: government publications. Decrees, invitations for bids, contracts, appointments, all that mind-numbingly boring stuff that makes up the day-to-day life of the public sector. Those embeddings might help me in future text-related tasks, like classifying government decrees and identifying certain types of contracts. I imagine it could be useful for other folks working with Brazilian government publications, so here's how I did that.

I started by scraping the official bulleting where all the acts of the Brazilian government are published: the Diário Oficial da União. To give you an idea of how much text that is, the Diário's 2020-07-06 issue has a total of 344 pages - with a tiny font and single spaces. (The Brazilian state is humongous and the size of the Diário reflects that.) The Diário is available online going as far back as 2002-01-01 and I scraped all of it. That amounted to about 8GB of zip files. Here is how to scrape it yourself (I used Python for everything):

{% highlight python %}
import os
import requests
from bs4 import BeautifulSoup

months = [
    # month names in Portuguese
    'janeiro',
    'fevereiro',
    'marco',
    'abril',
    'maio',
    'junho',
    'julho',
    'agosto',
    'setembro',
    'outubro',
    'novembro',
    'dezembro'
]

# path to the folder that will store the zip files
basepath = '/path/to/diario/' # create the folder first

# loop through years and months
for year in range(2002, 2021): # change end year if you're in the future
    for month in months:
        print(year, month)
        url = 'http://www.in.gov.br/dados-abertos/base-de-dados/publicacoes-do-dou/{}/{}'.format(str(year), month)
        r = requests.get(url)
        soup = BeautifulSoup(r.content)
        tags = soup.find_all('a', class_ = 'link-arquivo')
        urls = ['http://www.in.gov.br' + e['href'] for e in tags]
        fnames = [e.text for e in tags]
        for url, fname in zip(urls, fnames):
            if not os.path.isfile(basepath + fname):
                try:
                    r = requests.get(url)
                    with open(basepath + fname, mode = 'wb') as f:
                        f.write(r.content)
                except:
                    continue
{% endhighlight %}

After the scraping is done you can unzip each of those 400+ files manually or you can automate the job:

{% highlight python %}
import os
import zipfile

ipath = '/path/to/diario/'
opath = '/path/to/diario_xml/' # create folder first
for fname in os.listdir(ipath):
    if '.zip' in fname:
        year = fname[5:9]
        month = fname[3:5]
        section = fname[2:3]
        print(year, month, section, fname)
        destination = opath + year + '/' + month + '/' + section + '/'
        os.makedirs(destination)
        try:
            with zipfile.ZipFile(ipath + fname) as zip_ref:
                    zip_ref.extractall(destination)
        except:
            print('error; moving on') # some zip files are corrupted
{% endhighlight %}

This won't give you all the text in the Diário Oficial da União since 2002-01-01. Some zip files are corrupted and most issues are incomplete. For 2016, for instance, only the May issues are available. And for all years except 2019 and 2020 one of the sections (section 3) is missing entirely (the Diário is divided in three sections - 1, 2, and 3). Also, after you unzip the files you find out that in many cases the text is not in XML but in JPEG format. I wasn't in the mood to do OCR so I just ignored the JPEG files.

If you want to get in touch with the Diário's publisher to discuss those problems be my guest. Here I don't care much about those problems because all I need to train my word embeddings is *a ton of data*, not *all of the data*. And with the XML files that I got I have over 4 million government acts, which is probably way more than I need here.

After unzipping everything I trained my word embeddings. I chose to go with gensim's [implementation](https://radimrehurek.com/gensim/models/word2vec.html) of word2vec. The beauty of gensim's implementation is that you can stream the texts one by one straight from disk, without having to keep everything in memory. Now, that's a little tricky to accomplish. Gensim's documentation says that instead of a list of documents you can use a generator, but I found that not to be the case. I got this error: `TypeError: You can't pass a generator as the sentences argument. Try an iterator.` But I googled around and found a nifty [workaround](https://jacopofarina.eu/posts/gensim-generator-is-not-iterator/) that tricks gensim into using a generator by wrapping it inside an iterator. So here I have a generator (`yield_docs`) that yields one document at a time and then I wrap it inside an iterator (`SentencesIterator`) so that gensim won't complain.

About the documents, I have some 4.2 million XML files in total. In theory all these XML files should be easily parsable - they have tags with metadata, main content, etc. But in reality many are invalid. They have unclosed quotation marks and other problems that trip BeautifulSoup's parser. So I ignored all the metadata and just focused on the stuff inside the `<Texto>` (text) tags, which is always a collection of `<p>` tags. Now, different paragraphs of the same publication can talk about entirely different issues, so instead of treating each publication (i.e., each XML file) as a document I'm treating each `<p>` content as a document. That should yield more coherent word associations. So while I have 4.2 million XML files, in the end I have 72 million documents, one corresponding to each `<p>` tag. That's... a lot of text.

Back to word2vec. I don't really know the ideal number of dimensions here. I found a nice [paper](https://www.aclweb.org/anthology/I17-2006.pdf) that provides a way to estimate the ideal number of dimensions for any dimensionality reduction algorithm. But it's too computationally expensive: you need to create a graph where each unique token is a node and the co-occurrences are represented by edges. I tried it but the thing got impossibly slow at around 200k nodes - and I have over 1M unique tokens. By my estimates it would take about half a year for the nodes to be created, and then I would need to find the graph's maximum clique, which is also computationally expensive. So... no. If I had a specific text classification task in mind I would just try different numbers of dimensions and see what works best, but that's not what I'm doing right now. So instead of relying on any theoretical or empirical approaches I just went with 300 dimensions because that's a nice round number and I've seen it used in other word embeddings.

I'm discarding all words that appear in fewer than 1000 paragraphs (probably too rare to matter) and I'm using a short window of 5 (maximum distance between current and predicted word in a sentence).

Here's the code:

{% highlight python %}
import os
from bs4 import BeautifulSoup
from string import punctuation
from gensim.models import Word2Vec

def tokenize(raw_text):
    '''
    'Hey, dogs are awesome!' -> ['hey', 'dogs', 'are', 'awesome']

    using `re` would probably make it run faster but I got lazy
    '''

    # lowercase everything
    text = raw_text.lower()

    # remove punctuation
    for p in punctuation:
        text = text.replace(p, ' ')

    # remove extra whitespaces
    while '  ' in text:
        text = text.replace('  ', ' ')

    # tokenize
    tokens = text.strip().split()

    # remove digits
    tokens = [e for e in tokens if not e.isdigit()]

    return tokens

def yield_docs():
    '''
    crawl XML files, split each one in paragraphs
    and yield one tokenized paragraph at a time
    '''
    n = 0
    path = '/path/to/diario_xml/'
    for root, dirpath, fnames in os.walk(path):
        if not dirpath:
            for fname in fnames:
                if '.xml' in fname:
                    filepath = root + '/' + fname
                    with open(filepath, mode = 'r') as f:
                        content = f.read()
                    soup = BeautifulSoup(content, features = 'lxml')
                    paragraphs = soup.find_all('p')
                    for p in paragraphs:
                        print(n)
                        n += 1
                        tokens = tokenize(p.text)
                        if len(tokens) > 1:
                            yield tokens

class SentencesIterator():
    '''
    this tricks gensim into using a generator,
    so that I can stream the documents from disk
    and not run out of memory; I stole this code
    from here: 

    https://jacopofarina.eu/posts/gensim-generator-is-not-iterator/
    '''
    def __init__(self, generator_function):
        self.generator_function = generator_function
        self.generator = self.generator_function()

    def __iter__(self):
        # reset the generator
        self.generator = self.generator_function()
        return self

    def __next__(self):
        result = next(self.generator)
        if result is None:
            raise StopIteration
        else:
            return result

# train word2vec
model = Word2Vec(
    SentencesIterator(yield_docs), 
    size = 300, 
    window = 10, 
    min_count = 1000, 
    workers = 6
    )

# save to disk
model.save('word2vec.model')
{% endhighlight %}

And voilà, we have our word embeddings. We have a total of 27198 unique tokens (remember, we ignored any tokens that appeared in fewer than 1000 paragraphs) and 300 dimensions, so our word embeddings are a 27198x300 matrix. If you're not familiar with word2vec Andrew Ng explains it [here](https://www.coursera.org/lecture/nlp-sequence-models/word2vec-8CZiw). The TL;DR is that word2vec's output is a matrix where each unique token is represented as a vector - in our case, a 300-dimensional vector. That allows us to do a bunch of interesting stuff with that vocabulary - for instance, we can compute the cosine similarity between any two words to see how related they are. In gensim there is a neat method for that. For instance, suppose we want to find the words most related to "fraude" (fraud):

{% highlight python %}
model.wv.most_similar(positive = ['fraude'])
>>> [('fraudes', 0.5694327354431152),
>>> ('conluio', 0.5639076232910156),
>>> ('superfaturamento', 0.5263874530792236),
>>> ('irregularidade', 0.4860353469848633),
>>> ('dolo', 0.47721606492996216),
>>> ('falsidade', 0.47426754236221313),
>>> ('suspeita', 0.47147220373153687),
>>> ('favorecimento', 0.4686395227909088),
>>> ('ilícito', 0.4681907892227173),
>>> ('falha', 0.4664713442325592)]
{% endhighlight %}

We can see that bid rigging ("conluio") and overpricing ("superfaturamento") are the two most fraud-related words in government publications ("fraudes" is just the plural form of "fraude"). Kinda cool to see it. You can also cluster the word embeddings to find groups of inter-related words; use t-SNE to reduce dimensionality to 2 so you can plot the embeddings on an XY plot; and try a bunch of other [fun ideas](https://www.kaggle.com/pierremegret/gensim-word2vec-tutorial).

Here I trained the word embeddings from scratch but you could also take pre-trained Brazilian Portuguese embeddings and use the Diário to fine-tune them. You could also tweak the parameters, changing the window (10 here) and the number of dimensions (300). Whatever works best for the task you have at hand.

That's all for today! And remember, bureaucratese is bad writing - don't spend too long reading those texts, lest you start emulating them. The best antidote to bureaucratese (or to any bad writing) that I know is [William Zinsser](https://www.amazon.com/Writing-Well-Classic-Guide-Nonfiction/dp/0060891548).
