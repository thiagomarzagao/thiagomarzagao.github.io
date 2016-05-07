---
layout: post
title: classifying goods and services
comments: true
---

I needed to produce an automated classifier of goods and services: something that takes a short description and returns the corresponding category, according to some taxonomy. For instance, you enter "jelly beans" and the classifier returns "[Harmonized System](http://en.wikipedia.org/wiki/Harmonized_System) heading 1704 - Sugar Confection". The end goal is to classify all goods and services purchased with taxpayers' money in Brazil, in all levels (federal, state, municipal) and branches (executive, legislative, judiciary) of government. I've spent the last few weeks working on this and here I summarize what worked and what didn't. 

<strong>getting some data</strong> 

First I needed to get some data. For availability reasons I decided to use the purchases of the Federal District. (The Federal District s kind of like a state, except that it contains Brasília, the nation's capital, and is subject to some special rules.) So, I scraped all the purchases of the Federal District off [their website](https://www.compras.df.gov.br/publico/). That yielded a total of 139,624 purchases, which is about everything the Federal District has bought since 2005 (earlier purchases are not on the website). Some purchases involved a single item and others involved multiple items. For each purchase I got several data fields (price, date, etc), but the only one that interested me was the description of whatever it is that was being bought ("jelly beans", "aircraft parts", etc). If you are into that, [here](https://gist.github.com/thiagomarzagao/0288f7ec358caf40a554)'s the script I wrote to do the scraping and [here](https://gist.github.com/thiagomarzagao/f5b78bd8a4bc874b9846)'s the script I wrote to parse the HTML into JSON files. They're both in Python. (The comments are in Portuguese - sorry!) Naturally, these scripts may become useless if the website changes (I last used them on 12/18/14). 

<strong>clustering</strong> 

I decided to start with clustering - more specifically, k-means. I thought that if I could cluster similar items together then maybe I wouldn't even need a taxonomy at all, I could just create my own taxonomy based on whatever the clusters were. In case this is the first you hear about k-means, here's how it works: you treat every text (in my case, every item description) as a vector of term-frequencies, randomly create K centroids (K being the number of clusters you want to produce), assign each vector to its closest centroid, compute the squared distances between each vector and its centroid, recompute the centroids based on that assignment, reassign the vectors based on the new centroids, and repeat these last two steps until assignments stop changing. In practice you don't use the vectors of term-frequencies themselves, but a transformation thereof (TF-IDF, which gives more weight to more discriminant words). And you also normalize the vectors, to account for the different sizes of the texts. (See Manning, Raghavan, and Schültze's [Introduction for Information Retrieval](http://www-nlp.stanford.edu/IR-book/), chapter 16, for a proper explanation of k-means.)

I tried tweaking the number of clusters and removing some stopwords. I also tried using different initial centroids and k-means++ (which avoids convergence to local optima).

Programming-wise, I used Python and its [scikit-learn](http://scikit-learn.org/stable/) package. 

The results were a complete mess. The clusters were all over the place: for instance, "surgical gloves" and "buses" were in the same cluster. I briefly considered trying other clustering algorithms (maybe a hierarchical one) but the results were so bad that I just gave up on clustering for good. 

<strong>cosine similarity</strong> 

I moved on to cosine similarity, using the Harmonized System. In case you're not familiar with cosine similarity, it's just the cosine of the angle between two vectors - in this case, we're talking about vectors of term-frequencies (or, as discussed before, their normalized TF-IDF transformation). The Harmonized System, in turn, is the taxonomy used in international trade. It's structured in 96 chapters (ex.: Chapter 74 - Copper and Articles Thereof), which unfold in headings (ex.: 7408 - Copper Wire), which unfold in subheadings (ex.: 7408.21 - Wire of Copper-Zinc Base Alloys-Brass). (I used the Portuguese translation, not the English version.) 

So, I took the description of each item purchased by the Federal District, measured its cosine similarity to the description of each of the subheadings of the Harmonized System, and then classified the item in the subheading with highest similarity. 

I also tried using the Harmonized System headings instead of the subheadings. I noticed that the descriptions of the headings and subheadings are pretty short, so I also tried merging them together (so as to produce a more informative description). I noticed that the item descriptions were usually in the singular whereas the Harmonized System descriptions were usually in the plural, so I applied the first step of the [RSLP-S](http://www.inf.ufrgs.br/~viviane/rslp/) stemmer in order to bring everything to singular. I noticed that quantity- and measurement-related words and abbreviations - "kg", "mm", "caixa" (box) - were causing some confusion, so I also tried adding them to the list of stopwords. 

Finally, I tried dimensionality reduction - instead of computing the similarity of vectors of term-frequencies, I computed the similarity of lower-dimensionality vectors, which perhaps could capture the underlying categories behind the descriptions. I tried Latent Semantic Analysis, Latent Dirichlet Allocation, and Hierarchical Dirichlet Process (which unlike the first two doesn't require us to set the number of dimensions a priori).

Programming-wise, I used Python and its [Natural Language Toolkit](http://www.nltk.org/) and [gensim](https://radimrehurek.com/gensim/) packages. 

The results were awful. They were not entirely nonsensical but even the best results were still wrong: for instance, "battery charger" was classified under "battery". You can see that something gets captured correctly, but not enough to yield usable results. 

So, I gave up on the vector space model altogether and decided that I needed a supervised learning approach. 

<strong>taxonomy</strong> 

To do supervised classification we need labeled data - i.e., government-purchased items that have already been classified. That limits our choices because only the federal government bothers to classify its purchases - the states and municipalities do not (if they did I wouldn't need to come up with a classifier in the first place). 

The federal government uses two taxonomies: the CATMAT (short for Catalog of Materials) and the CATSER (short for Catalog of Services). The CATMAT and CATSER are like the Harmonized System, with numerical codes and hierarchical levels. If we merge the CATMAT and CATSER into a single taxonomy we have 79 groups, 670 classes, a couple thousand headings, and about 200,000 materials/services. To give a concrete example, material "191505 - Aircraft" goes under heading "16733 - Aircraft", which goes under class "1505 - Aircraft", which goes under group "15 - Aircraft and its structural components". 

As you see, the CATMAT/CATSER is not exactly a beauty of logic: in the above example (which is not fictional) the first three hierarchical levels all mean the same thing (aircraft) and the more detailed levels do not inherit the numerical code of the less detailed levels (material 191505 goes under heading 16733, which goes under class 1505). Worse still, in group "15 - Aircraft" we also find class "1510 - Aircraft with fixed pitch propellers", which clearly should not be a class but a heading under "1505 - Aircraft". 

I googled around but I didn't find a correspondence table with the Harmonized System, so I had to do with the CATMAT/CATSER (the Harmonized System, on the other hand, doesn't have services, only goods, so there is that). 

<strong>labeled data</strong> 

Ok, so much for the taxonomy - on to the data. There is a [public API](http://dados.gov.br/dataset/compras-publicas-do-governo-federal/resource/df58d72e-fd34-4f11-be1a-a7c1665c9d35) anyone can use to scrape the purchases of the federal government. The problem is, it doesn't always return the item descriptions - sometimes it does, sometimes it just says "see documentation". The API is still in beta, so I guess over time more data will be added, but for now it doesn't quite serve my purposes. 

I found the data in [this DW](http://dw.comprasnet.gov.br/asp/main.aspx). Now, before you get your hopes high (in case you're looking for the same data), that DW is gated. If you want access you need to write to the Ministry of Planning and ask them to give you a password. I didn't do that myself (the agency I work for did), so I don't know whom to contact there. Also, your username is your CPF number - the CPF is the Brazilian equivalent of the Social Security Number. So I have no idea what happens when you ask for access but you are a foreigner. 

Anyway. I scraped all 5,049,563 purchased items I found in the DW, which covers the 1998-2014 period. The DW is poorly documented, but it doesn't look like all purchases are there, especially for the late 90s and early 00s period. But five million is good enough and for each purchased item I have its description and its CATMAT/CATSER classification - material/service, heading, class, and group. 

The 5,049,563 descriptions of purchased items contain a total of 450,680 unique words. That gives us a term-document matrix with 2,275,737,052,840 cells, which is a bit too much. Thus after some pre-processing (I lowercased everything, removed some special characters - but kept all the accented letters used in Portuguese -, TF-IDF'ed, and normalized the data) I split the data into 504 chunks of 10,000 samples each (and one chunk of 9,563 samples). Then I split the chunks into 70% training (353 chunks), 15% validating (76 chunks), 15% testing (76 chunks). 

<strong>support vector machines</strong> 

I went for support vector machines (SVM) right off the bat. The math behind SVM is more involved than that of k-means or cosine similarity, but the gist of it is that you want to separate your apples and oranges by the widest possible margin. You don't just draw a line in the middle, you also draw two other, parallel lines (the "support vectors"), some distance away from the middle line, and you want the space between these two lines to be as empty as possible. You achieve that goal by having your loss function penalize any classification that falls in that region ("soft-margin" classification) and by (sort of) projecting your data onto a higher-dimensional space where no classifications fall in that region (the "kernel trick"; you don't really need to project your data onto a higher-dimensional space: you use kernels, functions that can get to the solution implicitly, using only the dot prodcuts of your samples). (Check Hastie, Tibshirani, and Friedman's [The Elements of Statistical Learning](http://statweb.stanford.edu/~tibs/ElemStatLearn/), chapter 12, for an introduction to SVM.) 

I used scikit-learn's [SGDClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html) class. Its `partial_fit` method allows online learning, i.e., it allows us to use one chunk of the data at a time (as opposed to batch learning, where we use all the data at the same time). The SGDClassifier uses (as the name suggests) stochastic gradient descent as an optimizer (its SGD implementation is influenced by [Léon Bottou](http://leon.bottou.org/projects/sgd)'s). To do multiclass classification (number of classes &gt; 2, which is the case here) it uses a "one vs all" approach. The SGDClassifier is a flexible class: we can tweak the loss function, the regularization term (the term that penalizes model complexity), and a number of hyperparameters. The downside is that it doesn't let us use a non-linear kernel. 

I tried different loss functions (hinge, squared hinge, modified Huber) and different regularization terms (L1, L2, ElasticNet). I tried classifying based on the CATMAT/CATSER group (79 groups in total) and on the CATMAT/CATSER class (670 classes in total). I tried with and without stopwords and I tried tweaking a number of other hyperparameters (like the number of passes through the data and the learning rate). 

I also tried weighing different words based on their position in the description. That's because the initial words are usually the most relevant: a typical item description would be, for instance, "t-shirt in black, made of cotton, size M". It's clear that we want the classifier to pay more attention to "t-shirt" than to the other words. Hence, in one experiment, I gave each word a weight that increases roughly exponentially the closer the word is to the beginning of the description. (I say <em>roughly</em> exponentially because, to keep the implementation simple, I simply repeated the word \\( (n \times n) / length(description) \\) times, with \\( n \\) being the inverse of the word's position. This often resulted in decimal numbers, but we can't repeat a word 0.3 times, so in these cases I rounded up the result. I could have solved this by removing the \\( length(description) \\) denominator, but that would take forever to run.) This departs from the bag-of-words model, but I thought it might work. I also tried simply repeating the first and second words a number of times, leaving the other words as they were. 

Finally, I tried classifying each sample in both a CATMAT/CATSER group and a CATMAT/CATSER class but ensuring that the group and class were consistent. The goal was to avoid having a sample classified in group "aircraft" and in class "jelly beans", for instance. To do that I applied a three-stage strategy. First I classified according to CATMAT/CATSER groups. Then instead of classifying according to CATMAT/CATSER classes I estimated the probability of each sample belonging to each of the 670 classes. I then assigned the sample to the CATMAT/CATSER class of highest probability <em>among those classes that belonged to the predicted group</em>. 

The whole thing (training, validating, testing) takes about 12 minutes to run (on a late 2013 MacBook Pro with 2.3 GHz Intel Core i7, 16GB of RAM, using Python 2.7.9 and scikit-learn 0.15.2 on an IPython notebook). I'm storing each data chunk as a SciPy sparse matrix saved as a Python pickle - certainly not the most efficient format, but with only 12 minutes of runtime that's good enough. 

<strong>results</strong> 

I got the best results using the modified Huber function as the loss function, L1 as the regularization term, and CATMAT/CATSER groups as the categories: 73% of correct classifications (76% with the validation data). With CATMAT/CATSER classes (instead of groups) performance degrades to 62% of correct classifications (66% with the validation data). The other choices - stopwords, number of passes through the data, learning rate, weighing words by their positions, ensuring group-class consistency, etc - didn't make much difference. 

I re-ran the algorithm using subsets of the data and here's how the percentage of correct classifications change: 

<img src="http://i.imgur.com/5rv2Yr1.png" alt="" /> 

As we see, performance seems to plateau after 1 million training samples or so. This is bad news: it means that my having 5 million samples is, by and large, just adding computational cost. 

In general the more frequent the group or class, the better the corresponding classifications. The correlation between frequency, on the one hand, and percentage of correct classifications, on the other, is 0.5 for groups and 0.35 for classes. But it's not like the bulk of the misclassifications is concentrated in a few rare groups or classes. The median frequency (in the test data, which has 759,763 samples) is 187 for classes and 3,400 for groups. So, most groups and classes just don't appear that often and the misclassifications are pretty spread across them. 

I'm not sure algorithms - random forest or neural networks - would help (I may give them a try if time permits). (I did try multinomial logit, just for the fun of it, but the results worsened considerably.) 

Fortunately, the SGDClassifier class can produce probability estimates - with the `predict_proba` method - so we have an uncertainty measure. Right now I'm inspecting the probability distributions to find a threshold above which the classifications are sufficiently correct. Then, when using the classifier to query the data, I can instruct it to discard any samples whose classification probability is lower than that threshold. 

Suggestions are welcome!