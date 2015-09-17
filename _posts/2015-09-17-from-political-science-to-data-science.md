---
comments: true
layout: post
title: from political science to data science
---

Today it's been a year since I started working as a data scientist. Before that I was doing my Ph.D., in political science. I wonder what other people who've made this sort of transition - from some social science to data science - have learned. Here's what I've found out (so far). Maybe this will encourage others to share their own experiences.

**Causality doesn't matter**

Political scientists want to know what causes what. Does democracy increase GDP per capita? Does oil make a country more authoritarian? Can trade prevent war? And so on. But causality is hard to establish. You need to run controlled experiments or convince the reviewers that you chose the right instruments or that you matched on the right confounders. And Gary King is always around the corner waiting to [stab you in the heart](http://gking.harvard.edu/publications/why-Propensity-Scores-Should-Not-Be-Used-Formatching).

So I was overwhelmed with joy when I found out that causality is not a big deal in the world of data science. Take text classification, for instance. You're mapping word counts to categories. Yes, in a way, the categories do cause the word counts - "let me be clear" appears a lot in Obama's speeches because they are Obama's. But we just don't care about the effect of Obama on the frequency of "let me be clear". We only care about classifying the text correctly.

That's liberating. Think of the time and effort that political scientists spend defending their causal claims. Or debunking others' causal claims. Or trying to accurately measure causal effects. When you remove causality from the equation you suddenly have a lot more time to work on other, potentially more interesting aspects of data analysis.

**Debates have clear winners**

Most political scientists have no notion of test set or validation set. They take a bunch of data and use 100% of it as a training set. They run their regressions and interpret the equations that map dependent variables to independent variables. And that's it. Pages and pages of articles and books and blog posts dedicated to training sets.

Which is of course ok - political scientists are trying to understand how the world works - but is also frustrating: debates never end. When you limit yourself to the training data you just don't have a clear metric of success. It's largely about how convincingly you can defend your theoretical and methodological choices. That leaves ample room for subjectivity, so it's never entirely clear who are the winners and losers.

In the world of data science, however, the training data is just the beginning. Once you've trained your model you use it on data it hasn't seen before and you observe how well it performs. And there are clear metrics for that: accuracy, recall, F-measure, etc. You can compare different models and immediately spot the winners and losers. You can argue all you want that your model is inherently "sounder" because of XYZ but that doesn't matter. What matters is whether your model [misclassifies dogs as cats](https://www.kaggle.com/c/dogs-vs-cats) less often than other models do.

**There is less ideological bias**

Hopefully I don't need to convince you that social scientists are overwhemingly on the left of the ideology spectrum. To give you but one number, the Democratic:Republican ratio is [5.6:1](http://www.criticalreview.com/2004/pdfs/klein_stern.pdf) among political scientists. The ideological distribution is so skewed that there are [survival guides](http://journals.cambridge.org/action/displayAbstract?fromPage=online&aid=8607181&fileId=S1049096512000352) for non-leftists who want to thrive in academia.

Reviewers being humans, sometimes they dislike your instruments or matching or sample because they dislike your paper's conclusions. If you are in political science you probably lean left, so you're unlikely to have seen this happen to one of your papers. But try to argue that Latin America's left turn in the 2000s has eroded democracy in the region. Boy, brace yourself for some angry reviews. It's not that the methodological criticisms will be unfounded. It's just that they would likely not exist if your conclusions were reversed.

In data science, on the other hand, you have [Kaggle](https://www.kaggle.com/) competitions. Winners and losers are not decided on the basis of subjective evaluations of your methods or sample or theory. Winners and losers are decided on the basis of who gets the higher F-measure. It's a fair fight. So, it's not just that debates don't linger forever (see above), but also that they resolved in a much more rigorous way. Sometimes debates do end in political science - but not always as they should.

**You want more error, not less**

Political scientists want a good model fit. But as I mentioned before all they have is a training set. They have no notion of prediction or out-of-sample testing, so they end up overfitting. The fit is too good - the model doesn't generalize.

It's not that political scientists don't know about overfitting. They do. But if all your data are training data then how the heck can you assess overfitting? 

Political scientists believe that you can avoid overfitting by avoiding kitchen-sink regression. If I include only theoretically relevant regressors then everything should be ok, right?

Except we can always twist theory to accomodate whatever variables we need in order to get what we want. Maybe if I square this variable then I'll get the proper p-values. And then I come up with some creative explanation of why its effect is not linear. Reviewers (ideally) assess theory consistency, of course, but then we're back to the subjectivity and bias problems I discussed before.

This was perhaps my biggest methodological shock when I started doing data science. At first I struggled with the idea of a regularization term. What? So you want me to bias my coefficients toward zero? Then Andrew Ng's machine learning course taught me that there is data you use to train your model and data you use to test it. And then regularization made sense. A bit more error is good.

**Programming matters**

Political scientists' code is rigid: each script is meant to produce a pre-determined set of estimates, using a pre-determined dataset. The code always takes the same input and always return the same output. It does one thing and one thing alone. It doesn't matter much if the code could be faster or prettier: as long as it replicates what you did in your paper you have fulfilled your duty.

Data scientists' code is flexible: your code needs to accept a variety of inputs and return a variety of outputs. That's because you're not writing code for yourself, but for others. For instance: you have data in MySQL and other people in your organization want insights from those data. You then write a web app where people can, say, fit a regression line through some subset of the data. You don't know what subsets people will choose. And you don't know what the regression lines will look like. So your code needs to handle many different scenarios. What if the user chooses a non-valid subset? Say, years 2012-2014 when the data end in 2010? What if the user chooses all the data and that overloads the server? What if the regression tool you're using under the hood (say, R's lm() function) returns an error because the chosen subset is too small? In short: data scientists' code has a lot more IF/THEN/ELSE statements than political scientists' code.

So, programming matters in data science. It's about both depth and breadth: you need a firmer grasp of basic programming concepts, like conditionals and functions (that's the depth) and you need to learn web development, SQL, NoSQL, database administration, messaging, server maintenance, security, testing (that's the breadth). 

Some of my political scientist friends would rather poke their own eyes out than endure that sort of technical work. Some even consider technical work to be beneath them. I suppose I understand. You survived [Social Origins of Dictatorship and Democracy](http://www.amazon.com/Social-Origins-Dictatorship-Democracy-Peasant/dp/0807050733)'s 592-page discussion of regime change, class, and modernization - surely you're destined to higher purposes. You are here to understand the world, not center HTML tables.

But if you don't mind getting your hands dirty then programming can be a lot of fun - and at least as intelectually rewarding than political science. With programming there is no "arguing your way out" of anything: either your code works or it doesn't. And when it doesn't you have to figure out why and that requires a lot of sinapses. As in political science, it's largely about hypothesis testing - if the code isn't working because of XYZ then if I try ABC I should get this result, otherwise I should get that other result. Except that there is a finish line: you'll never really know what makes democracy work but you'll eventually figure out which regex matches the string you're looking for. And you will get to the finish line or die trying - you can't just declare regex to be a meaningless social construct and move on. You can't get away with vague wording or selective omissions. The machine is not a journal editor - you can't bullshit your way through it.

**You lose freedom**

Wait, don't quit grad school just yet - there's a lot to miss about academia. First and foremost, I miss the freedom to work on whatever I wanted to.

Don't get the wrong idea: I thoroughly enjoy what I'm doing right now (I help automate cartel detection; you know, when companies that should compete against each other decide to shake hands instead). I'm learning a lot and it's by far the most rewarding job I've ever had. But I can't just wake up tomorrow and decide to work on face recognition for the next six months. I can do whatever I want to do in my spare time, but I still need to show up Mon-Fri and work on cartel detection. Sure, I could find another job. But in academia you don't need to find another job just because you've got a new research interest. You stay in the same job, you just start doing something else. And that is awesome. I'm ok with foregoing that freedom, but I imagine not everyone is.

---

This is it. If you too are in data science as a refugee from the social sciences I would love to hear from you. How did you get here? How is the new life playing out for you? Do you intend to go back some day?