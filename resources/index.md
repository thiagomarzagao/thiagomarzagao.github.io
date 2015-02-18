---
layout: page
title: resources
---

(last updated: February 18th, 2015)

<strong>machine learning</strong>:

Prof. Ng’s online [class](https://class.coursera.org/ml-003/class). It’s certainly the best possible intro to machine learning you can find. Prof. Ng is an authority on the subject (he is director of the AI lab in Stanford) and a superb instructor.

Hastie, Tibshirani, and Friedman’s “The elements of statistical learning”. Comprehensive and [free](http://statweb.stanford.edu/~tibs/ElemStatLearn/).

Prof. Shalizi’s [lecture notes](http://www.stat.cmu.edu/~cshalizi/350/). They contain great informal presentations of difficult machine learning subjects and thus are a great companion to machine learning textbooks and courses.

Caltech’s machine learning [video library](http://work.caltech.edu/library/). It’s incredibly comprehensive. If you feel overwhelmed start with this video, where Prof. Abu-Mostafa gives a nice overview of the field.

Manning, Raghavan, and Schütze’s “Introduction to information retrieval”. A [draft version](http://nlp.stanford.edu/IR-book/) is available online. This book is an excellent starting point for text mining. If your interest is in text mining only (and not in search algorithms), you can start with chapter 6, which lays some foundations, then proceed to chapters 13-17.

Prof. Grimmer’s [lecture notes](http://www.justingrimmer.org/teaching.html). They are from his text analysis course at Stanford. He covers the main text analysis methods, giving both the intuition and the math. He also helps you make sense of the field as a whole – what’s related to what, in what way.

<strong>webscraping</strong>:

Katharine Jarmul’s PyCon 2014 [talk](http://pyvideo.org/video/2592/introduction-to-web-and-data-scraping-with-pyt) teaches you how to webscrape with Python. It’s by far the best webscraping_with_Python resource I’ve ever seen.

Prof. Caren’s [tutorials](http://nealcaren.web.unc.edu/an-introduction-to-text-analysis-with-python-part-1/) teach you the basics of webscraping with Python. No previous exposure to Python is assumed, so it’s a great place to start if you are in a hurry (if you are not, learn Python first, then webscraping).

[Selenium](http://docs.seleniumhq.org/) lets you “remote control” your browser. It’s tremendously useful when you need to scrape difficult sites that don’t like to be scraped (e.g., LexisNexis and Factiva). In my own research Selenium has saved me months of manual, tedious work.

When I first started I couldn’t find any good tutorial on how to webscrape with Selenium, so I wrote one myself. It’s divided in five parts:

* [part 1](http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/): installing Selenium, locating page elements, interacting with page elements
* [part 2](http://thiagomarzagao.com/2013/11/14/webscraping-with-selenium-part-2/): handling dynamic names and downloading files
* [part 3](http://thiagomarzagao.com/2013/11/15/webscraping-with-selenium-part-3/): handling network errors
* [part 4](http://thiagomarzagao.com/2013/11/16/webscraping-with-selenium-part-4/): pacing your bot
* [part 5](http://thiagomarzagao.com/2013/11/17/webscraping-with-selenium-part-5/): headless browsing and parallel webscraping

Katharine Jarmul’s recent talk (see above) also covers Selenium (it starts about 2h30m in) and she does a great job, so you should check it.

Will Larson’s [tutorial](http://lethain.com/an-introduction-to-compassionate-screenscraping/) teaches you the art of compassionate webscraping — i.e., getting the stuff you want without disrupting the website’s operation.

<strong>data sources</strong>:

[WordNet](http://wordnet.princeton.edu/). This dataset groups related words — synonyms, antonyms, hyponyms (as in “chair” being a type of “furniture”), and meronyms (as in “leg” being a part of a “chair”). There are also [similar datasets for other languages](http://www.globalwordnet.org/gwa/wordnet_table.html).

[LexisNexis Academic](http://www.lexisnexis.com/hottopics/lnacademic/) and [Factiva](http://www.dowjones.com/factiva/index.asp). These are comprehensive repositories of newspapers, magazines, and other news sources.

[GDELT](http://eventdata.psu.edu/data.dir/GDELT.html) (Global Data on Events, Location, and Tone). It contains over 200 million georeferenced events starting in 1979.

<strong>Python</strong>:

If you are new to programming, [Udacity’s online class](https://www.udacity.com/course/cs101) is the best place to start. Prof. Evans uses Python to teach you the basics of programming – things like hashing, recursion, and computational cost. The course is self-paced (unlike Coursera courses), so you may complete it in a week or two if you clear your schedule.

If you already know the basics of programming but never used Python, [“Python in a Nutshell”](http://www.amazon.com/Python-Nutshell-Second-Edition-In/dp/0596100469) is my pick. I would recommend reading it from cover to cover (it only takes a day or two). Otherwise you may waste precious time later on trying to google what a “tuple” is, or how to “unpack a list of lists”. It’s better to learn all the essentials upfront.

Here’s a [flowchart](http://mdalums95.files.wordpress.com/2013/12/wrujv6r.png) with the most common newbie mistakes.

Once you get the basic stuff out of the way, [Problem Solving with Algorithms and Data Structures Using Python](http://interactivepython.org/courselib/static/pythonds/index.html) is an excellent introduction to, well, algorithms and data structures. Why learning these? Because by carefully designing your algorithms and by choosing the correct data structures you can make your code run much faster (or run at all, in case your current code exceeds your machine’s processing power or memory size).

To keep up-to-date with what’s going on in terms of Python tools for data analysis check the [PyData](http://vimeo.com/pydata) talks on vimeo.

[Here](https://www.airpair.com/python/posts/top-mistakes-python-big-data-analytics)'s a useful list of common mistakes you should avoid when using Python with big data.

Python has great stats libraries. The must-have are [NumPy](http://www.numpy.org/) and [pandas](http://pandas.pydata.org/). NumPy is great for matrix operations — transpose, multiply, etc. Pandas is great for data management — merging tables, naming columns, and so on. So together they give you the matrix tools of R with the dataset tools of Stata. If that’s not good enough for you, NumPy and pandas can run at near-C speeds.

If you know [Matlab](http://wiki.scipy.org/NumPy_for_Matlab_Users), here is a neat equivalence table between Matlab and NumPy.

You’ll probably also want to have [SciPy](http://www.scipy.org/) and [scikit-learn](http://scikit-learn.org/stable/). SciPy gives you regression, otimization, distributions, advanced linear algebra (e.g., matrix decomposition), and much more. Scikit-learn gives you machine learning — Naïve Bayes, support vector machines, k-nearest neighbors, and so on.

If you have large datasets you may want to look into [PyTables](http://pytables.github.io/) as well. It has some tools that let you manage “out-of-core” data, i.e., data that doesn’t fit in memory.

To make the most out of NumPy, pandas, SciPy, scikit-learn, and PyTables you need to have some dependencies installed, like [HDF5](http://www.hdfgroup.org/HDF5/) and [MKL](http://software.intel.com/en-us/intel-mkl). These tools can be a pain to install, but are worth it – your code will run much faster. If you want a quick-and-dirty solution you can simply download and install [Anaconda Python](https://store.continuum.io/cshop/anaconda/) or [Enthought Canopy](https://www.enthought.com/products/canopy/). These are “bundles” that come with everything included (Python itself, all the important modules, and all those low-level tools). There are downsides though (Anaconda issues annoying warnings, Canopy is a pain to use in remote machines, both crash sometimes).

If you have non-English texts, it’s worth learning the intricacies of character encoding and here is a nice [tutorial](http://docs.python.org/2/howto/unicode.html) on that (and here is [a bit of historical context](http://www.joelonsoftware.com/articles/Unicode.html)). I’ve have to deal with texts in Spanish, Portuguese, and French, and all those accented letters (‘é’, ‘ã’, ‘ü’, etc) must be handled carefully (so the code doesn’t break or the output doesn’t become unintelligible).

Python’s [Natural Language Toolkit](http://www.nltk.org/) (NLTK) gives you some tools for text-processing: tokenizing, chunking, etc. Two alternatives worth mentioning are the [Stanford CoreNLP](http://nlp.stanford.edu/software/corenlp.shtml) toolkit, which has several Python wrappers, and [spaCy](http://honnibal.github.io/spaCy/). If you’re looking for windows and buttons [JFreq](http://conjugateprior.org/software/jfreq/) is a popular choice, but it chokes on large corpora and I’ve found that it doesn’t handle accented characters well.

If you are into text analysis then you also should check [gensim](http://radimrehurek.com/gensim/). It gives you TF-IDF, LSA and LDA transformations, which means that you can do dimensionality reduction, handle synonymy and polysemy, and extract topics. And here is the best part: gensim handles huge datasets right out-of-the-box, not need to do any low-level coding yourself. I used gensim for one of my dissertation papers and it has saved me months of coding.

<strong>miscellanea</strong>

This is domain-specific, but if you're doing text analysis in political science you should definitely check [Prof. Benoit's](http://www.kenbenoit.net/) from time to time. Also, he just created a [website](http://www.textasdata.com/) dedicated to text analysis.

In case you are plagued by the curse of too much data, the University of Oklahoma has a [workshop series](http://www.oscer.ou.edu/education.php) on supercomputing.

Prof. Howe’s online [class](https://class.coursera.org/datasci-001/class/index) teaches you MapReduce and some SQL, which may come in very handy if you have tons of data.

<strong>next on the list</strong>:

Here’s some stuff I haven’t touched yet but am eager to:

[Data Structures and Algorithms in Python](http://www.wiley.com/WileyCDA/WileyTitle/productCd-EHEP002510.html) (book). It seems to be more comprehensive than Problem Solving with Algorithms and Data Structures Using Python (mentioned above).

[The Elements of Computing Systems: Building a Modern Computer from First Principles](http://www.amazon.com/The-Elements-Computing-Systems-Principles-ebook/dp/B004HHORGA/ref=tmm_kin_title_0?ie=UTF8&qid=1383623175&sr=8-1) and [Operating System Concepts](http://www.amazon.com/Operating-System-Concepts-9th-Edition-ebook/dp/B00APSZCEQ/ref=dp_kinw_strp_1) (books). I don’t have any formal training in computer science, so to me the hardware is, by and large, a mystery. I want to learn the basics.

[High Performance Scientific Computing](https://www.coursera.org/course/scicomp) (course). I’ve been using high-performance environments for some time (the Ohio Supercomputer Center and Amazon EC2), learning on the fly, but I feel that there is a lot out there that I ignore and that could be useful to me. Particularly when it comes to memory management and parallel code.

[Paradigms of Computer Programming](https://www.edx.org/course/louvain/louv1-01x/paradigms-computer-programming/1203) (course).