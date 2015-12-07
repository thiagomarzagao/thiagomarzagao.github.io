---
comments: true
layout: post
title: model persistence without pickles
---

So, I trained this SVM classifier and I wanted to use it in a web [app](https://github.com/thiagomarzagao/catmatfinder) I built. I used Python for everything, so it seemed straightforward at first: just use the [pickle](https://docs.python.org/3/library/pickle.html) module to save the classifier to disk, then have the app load the pickle. But things got complicated. In the end I found a better way to achieve model persistence, so I thought I should share the experience.

The fundamental problem is that the classifier turned out huge. Not surprising: it was trained with 20 million documents and intended to pick one of 560 possible document categories. The resulting coefficient matrix has dimensions 560 (categories) by 505,938 (unique tokens). That's a matrix with 283,325,280 cells. When pickled to a file it takes up 8GB of disk space.

I didn't mind that at first. I thought "fine, so the app will take a few seconds to be ready after I deploy it, no problem". But the app can't load an 8GB pickle if there is only, say, 1GB of RAM. I did some tests and realized that I would need a server with at least 16GB of RAM to (barely!) host the app. I looked up server prices on Amazon Web Services and on Google Compute Engine. It would cost me some US$ 200 a month to keep the app alive. Not happening. (Have I mentioned that I live in Brazil and that our currency was massive devalued this year?)

So I gave up on hosting the app. I decided to open source the [code](https://github.com/thiagomarzagao/catmatfinder) instead and let users download and host the app themselves. But that turned my 8GB pickle into a problem. It's ok to consume your own pickles (well, [not really](https://www.youtube.com/watch?v=7KnfGDajDQw)) but it's [not ok](http://scikit-learn.org/stable/modules/model_persistence.html#security-maintainability-limitations) to expect other people to consume your pickles. Pickles can have malicious code. And pickles are not guaranteed to work across different versions of the same Python packages.

Now, a model is basically a bunch of coefficients - so why not store it as data? We shouldn't have to store a model in a pickle or in any format that is not human readable. We can store a model as we store the very data that we used to estimate the model. And that's what I propose we do.

I used scikit-learn's stochastic gradient descent [class](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html) to train my SVM classifier, which I instantiated with the following paramters:

{% highlight python %}
from sklearn import linear_model

clf = linear_model.SGDClassifier(loss = 'modified_huber',
                                         penalty = 'l2',
                                         alpha = 0.0001,
                                         fit_intercept = True,
                                         n_iter = 60,
                                         shuffle = True,
                                         random_state = None,
                                         n_jobs = 4,
                                         learning_rate = 'optimal',
                                         eta0 = 0.0,
                                         power_t = 0.5,
                                         class_weight = None,
                                         warm_start = False)
{% endhighlight %}

Once the model is trained the coefficients are stored in the `clf.coef_` attribute as a numpy array of dimensions 560 (classes) by 505,938 (unique tokens).

{% highlight python %}
array([[ -9.86766641e-03,  -6.35323529e-03,  -2.78639093e-05, ...,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
       [ -1.08928684e-03,  -5.49497974e-04,  -1.72031659e-08, ...,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
       [ -1.13471047e-05,  -8.34983019e-06,   0.00000000e+00, ...,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
       ..., 
       [ -4.71493271e-06,   0.00000000e+00,   0.00000000e+00, ...,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
       [ -1.51909841e-03,  -1.58582663e-03,  -1.53207693e-04, ...,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
       [ -8.46919968e-07,  -3.21041555e-07,  -3.67708175e-10, ...,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00]])
{% endhighlight %}

As you can see, extracting the coefficients is trivial: just get `clf.coef_`. But how do we store them as data? I toyed with a couple of ideas and in the end I chose [HDF5](https://www.hdfgroup.org/HDF5/whatishdf5.html). If you haven't used it before, an HDF5 file is a "container" inside which you can store arrays. I had used HDF5 before and it's great for fast retrieval of large amounts of data. To use it from Python you must have [pytables](http://www.pytables.org/) installed. You don't need to call pytables though - pandas has a nice [interface](http://pandas.pydata.org/pandas-docs/stable/io.html#hdf5-pytables) to it. Here's how I did it:

{% highlight python %}
import pandas as pd

store = pd.HDFStore('coefficients.h5')
counter = 0
for row in clf.coef_:
    # annoyingly I couldn't store each row of the
    # numpy array directly, I had to convert each
    # row into a pandas DataFrame, as you see here,
    # or else I got an error message
    store['row' + str(counter)] = pd.DataFrame(row)
    counter += 1
store.close() 
{% endhighlight %}

That's it - we have extracted our coefficients and stored them in an HDF5 file. Here I had 560 categories and 505,938 unique tokens, so my HDF5 file contains 560 pandas DataFrames, each of length 505,938.

We are not done though. Each of the 560 classes has not only 505,938 coefficients but also one intercept. These are stored in the `clf.intercept_` attribute. You can store them with HDF5 as well but with only 560 intercepts I didn't bother doing that. I just printed `clf.intercept_` to the screen and then copied and pasted it into a .py file. Dirty, I know, but quick and easy. The file looks like this:

{% highlight python %}
import numpy as np

intercepts = np.array([-1.0378634 , -1.00160445, -1.00561022, -1.35181801, -1.00007832,
                       -1.00009826, -1.00010426, -1.00985818, -1.00165959, -1.00020922,
                       -1.00417335, -1.003692  , -1.00178602, -1.00047299, -1.00073538,
                       -1.00008621, -1.00021723, -1.00037028, -1.00055338, -1.09941216,
                       -1.00037199, -1.00204897, -1.03388095, -1.00933133, -1.02132215,
                       -1.04021753, -1.00289487, -1.00191766, -1.00168548, -1.00053103,
                       ...
{% endhighlight %}

Finally we need to extract our class labels. They are in `clf.classes_`. Same as with the intercepts: I just printed the array to the screen and then copied and pasted it into a .py file.

{% highlight python %}
import numpy as np

class_labels = np.array(['11005', '11010', '11015', '11020', '11025', '11030', '11035',
                         '11040', '11045', '11055', '11080', '11090', '11095', '11110',
                         '11125', '11135', '11190', '11240', '11280', '11305', '11310',
                         '11315', '11325', '11330', '11340', '11370', '11375', '11385',
                         ...
{% endhighlight %}

Now we have our model nicely stored as data. People can inspect the HDF5 and .py files without (much) risk of executing arbitrary code. Our model is human readable and shareable. Now my [app](https://github.com/thiagomarzagao/catmatfinder) is indeed open source.

Ok, so much for disassembling the model. How do we put it back together? 

Quick and easy. Instantiate the model, load the class labels, the coefficients and the intercepts, and plug everything in:

{% highlight python %}
import numpy as np
import pandas as pd
from sklearn import linear_model

# load class labels
from class_labels import class_labels # or however you named the file and array

# load intercepts
from intercepts import intercepts # or however you named the file and array

# instantiate model
clf = linear_model.SGDClassifier(loss = 'modified_huber',
                                 penalty = 'l2',
                                 alpha = 0.0001,
                                 fit_intercept = True,
                                 n_iter = 60,
                                 shuffle = True,
                                 random_state = None,
                                 n_jobs = 4,
                                 learning_rate = 'optimal',
                                 eta0 = 0.0,
                                 power_t = 0.5,
                                 class_weight = None,
                                 warm_start = False)

# load coefficients
store = pd.HDFStore('coefficients.h5')

# convert from pandas DataFrame back to numpy array
coefs = np.array([np.array(store['row' + str(i)]).T[0] for i in range(len(class_labels)]))

# close HDF5 file
store.close()

# plug class labels
clf.classes_ = class_labels

# plug intercepts
clf.intercept_ = intercepts

# plug coefficients
clf.coef_ = coefs
{% endhighlight %}

And voilà, we have reconstructed our model. The labels, intercepts and coefficients are in their proper places (i.e., assigned to the proper `clf` attributes) and the model is ready to use. And everything runs a lot faster than if we were loading pickles.

Some models are more easily "datafied" than others. "Datafying" an instance of scikit-learn's TfidfVectorizer's [class](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), for instance, is a bit tricky. I'll cover that in another post.