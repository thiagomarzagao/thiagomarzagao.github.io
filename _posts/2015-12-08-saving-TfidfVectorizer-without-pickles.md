---
comments: true
layout: post
title: saving TfidfVectorizer without pickles
---

As [promised](http://thiagomarzagao.com/2015/12/07/model-persistence-without-pickles), here's how to save a trained instance of scikit-learn's [TfidfVectorizer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) without using pickles - in other words, how to save it as human-readable, shareable data.

The general idea is in my previous post: a model is a set of coefficients so you just extract them and save them as you would save any other data (like the very data you used to train the model). That way you avoid the [security and maintainability problems](http://scikit-learn.org/stable/modules/model_persistence.html) of using pickles. You extract the coefficients, save them as data, then later you load them and plug them back in.

Now, that's easier to do with some models than with others. With scikit-learn's [SGDClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html), for instance, that's a breeze. But with TfidfVectorizer that's a bit tricky. I had to do it anyway so I thought I should write a how-to of sorts.

First we instantiate our TfidfVectorizer:

{% highlight python %}
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(lowercase = False,
                             min_df = 2,
                             norm = 'l2',
                             smooth_idf = True)
{% endhighlight %}

Once we've trained the vectorizer it will contain two important attributes: `idf_`, a numpy array that contains the inverse document frequencies (IDFs); and `vocabulary_`, a dictionary that maps each unique token to its column number on the TF-IDF matrix.

To extract the IDF array you can just print it to the screen and then copy and paste it to a .py file. The file will look like this:

{% highlight python %}
import numpy as np

idfs = np.array([7.35689028227,
                 8.07104642361,
                 13.2874331692,
                 16.5531925799,
                 ...
{% endhighlight %}

To extract the vocabulary you can do the same, but depending on how many tokens you have this may not be practical. An alternative is to use JSON. Like this:

{% highlight python %}
import json

json.dump(vectorizer.vocabulary_, open('vocabulary.json', mode = 'wb'))
{% endhighlight %}

The vocabulary is now saved in the `vocabulary.json` file.

That's it, we've disassembled our vectorizer. So far so good.

Now, it's when we try to put everything back together that things get tricky.

We start by importing the TfidfVectorizer class. But we can't instantiate the class right away. Here's the problem: we are not allowed to assign arbitrary values to the `idf_` attribute. If you instantiate the class and then try something like `vectorizer.idf_ = idfs` you get an `AttributeError` exception.

{% highlight python %}
from idfs import idfs # numpy array with our pre-computed idfs
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(lowercase = False,
                             min_df = 2,
                             norm = 'l2',
                             smooth_idf = True)

vectorizer.idf_ = idfs
AttributeError: can't set attribute
{% endhighlight %}

The problem is that the `idf_` attribute is kind of "read-only". I say "kind of" because that's not exactly true: if you train the vectorizer then `idf_` will change (it'll have the IDFs). But `idf_` behaves as read-only if you try to plug the IDFs directly, without training the vectorizer. 

That happens because `idf_` is defined with a `@property` decorator and has no corresponding `setter` method - check TfidfVectorizer's [source code](https://github.com/scikit-learn/scikit-learn/blob/c957249/sklearn/feature_extraction/text.py#L1269).

I can't imagine why the scikit-learn folks made that choice. That's a bunch of smart people with a lot of programming experience, so I imagine they had good reasons. But that choice is getting in the way of proper model persistence, so here's how we get around it:

{% highlight python %}
from idfs import idfs # numpy array with our pre-computed idfs
from sklearn.feature_extraction.text import TfidfVectorizer

# subclass TfidfVectorizer
class MyVectorizer(TfidfVectorizer):
    # plug our pre-computed IDFs
    TfidfVectorizer.idf_ = idfs

# instantiate vectorizer
vectorizer = MyVectorizer(lowercase = False,
                          min_df = 2,
                          norm = 'l2',
                          smooth_idf = True)
{% endhighlight %}

So, what's happening here? We are creating a new class - MyVectorizer -, which inherits all attributes (and everything else) that TfidfVectorizer has. And we are plugging our IDFs into the MyVectorizer class. When we instantiate MyVectorizer our pre-computed IDFs are already there, in the `idf_` attribute. Problem solved.

But we're not done yet. If you try to use the vectorizer now you'll get an error:

{% highlight python %}
vectorizer.transform(['hey macarena'])
ValueError: idf vector not fitted
{% endhighlight %}

So, we're being told that our vectorizer hasn't been trained, even though we've plugged our pre-computed IDFs. What's going on?

When we try to use our vectorizer there is a function `check_is_fitted` that checks, well, whether we have fitted the vectorizer. You'd think it checks the `idf_` attribute but it doen't. Instead it checks the attribute of an attribute: `._tfidf._idf_diag`, which is a sparse matrix made from the IDFs. So we need to plug that matrix into the vectorizer.

We can extract `._tfidf._idf_diag` from the trained vectorizer, save it as data, then load and plug it - just like we did with the other attributes. But an easier alternative is to simply compute `._tfidf._idf_diag` from our IDFs, using scipy.

{% highlight python %}
import scipy.sparse as sp
from idfs import idfs # numpy array with our pre-computed idfs
from sklearn.feature_extraction.text import TfidfVectorizer

# subclass TfidfVectorizer
class MyVectorizer(TfidfVectorizer):
    # plug our pre-computed IDFs
    TfidfVectorizer.idf_ = idfs

# instantiate vectorizer
vectorizer = MyVectorizer(lowercase = False,
                          min_df = 2,
                          norm = 'l2',
                          smooth_idf = True)

# plug _tfidf._idf_diag
vectorizer._tfidf._idf_diag = sp.spdiags(idfs,
                                         diags = 0,
                                         m = len(idfs),
                                         n = len(idfs))
{% endhighlight %}

Problem solved. All we need to do now is plug the vocabulary.

{% highlight python %}
vocabulary = json.load(open('vocabulary.json', mode = 'rb'))
vectorizer.vocabulary_ = vocabulary
{% endhighlight %}

Now our vectorizer works:

{% highlight python %}
vectorizer.transform(['hey macarena'])
<1x505938 sparse matrix of type '<type 'numpy.float64'>'
    with 2 stored elements in Compressed Sparse Row format>
{% endhighlight %}

And we're done.