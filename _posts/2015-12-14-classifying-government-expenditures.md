---
comments: true
layout: post
title: classifying public procurement
---

New [manuscript](https://s3.amazonaws.com/thiagomarzagao/classifyingProcurement.pdf) and [app](https://github.com/thiagomarzagao/catmatfinder). Abstract:
 
> The Brazilian government often misclassifies the goods it buys. That makes it hard to audit government expenditures. We cannot know whether the price paid for a ballpoint pen (code \#7510) was reasonable if the pen was misclassified as a technical drawing pen (code \#6675) or as any other good. This paper shows how we can use machine learning to reduce misclassification. I trained a support vector machine (SVM) classifier that takes a product description as input and returns the most likely category codes as output. I trained the classifier using 20 million goods purchased by the Brazilian government between 1999-04-01 and 2015-04-02. In 83.3% of the cases the correct category code was one of the three most likely category codes identified by the classifier. I used the trained classifier to develop a web app that might help the government reduce misclassification. I open sourced the [code](https://github.com/thiagomarzagao/catmatfinder) on GitHub;  anyone can use and modify it free of charge.

