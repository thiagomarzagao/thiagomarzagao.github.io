---
comments: true
layout: post
title: '"I''ve been using Python for 3 years and I''ve never defined a class"'
---

[Here](http://www.reddit.com/r/Python/comments/1qvoop/ive_been_using_python_for_3_years_and_ive_never/).

I guess that's the case for many of us who use general-purpose languages (like Python) to do math. When I only knew R and Stata my typical script was a bunch of math expressions, one after the other, some of them put inside functions. And that seemed to work fine. Then I started learning Python and noticed that that's not what textbook scripts look like. They don't have functions hanging around by themselves; everything is organized around classes and subclasses.

Realizing the huge gap between the scripts I wrote and the ones on textbooks was a bit demoralizing. Edsger Dijkstra once famously said that "It is practically impossible to teach good programming to students that have had a prior exposure to BASIC: as potential programmers they are mentally mutilated beyond hope of regeneration." I thought that maybe R and Stata were my BASIC, that learning them had destroyed any chances that I would ever write decent code. (Though I have also learned some BASIC, as a kid, so perhaps I was already mentally mutilated by the time I encountered R and Stata).

[![](http://i.imgur.com/CdiAnVD.png)](http://imgur.com/CdiAnVD)
(This may have impaired my programming skills but I enjoyed tweaking [Nibbles](http://en.wikipedia.org/wiki/Nibbles_(video_game)). And using `goto`)

Turns out I made too much of it. Yes, my scripts were ugly and I shouldn't let things happen outside functions and I shouldn't have global variables. I firmly intend to go back and refactor my [Wordscores](/2013/06/10/wordscores-in-python/) and "[Fightin' Words](/2013/06/24/130/)" implementations. But if you are doing math and your script is small and you won't integrate it into a larger project, then not everything needs be organized around classes.

As [someone in the thread above](http://www.reddit.com/r/Python/comments/1qvoop/ive_been_using_python_for_3_years_and_ive_never/cdh6c79) noted, writing math code is fundamentally different than writing a desktop application.

> In a program designed to calculate a result, an input gets heavily processed through several phases of computation. It might be useful to define classes here, and it might not: I could see cases where heterogenous input needed to be processed along a common axis, but with the heterogenous identity preserved. Named tuples or classes might serve this goal well. But the concept of the program is essentially a stream or blob of data that moves through a processing pipeline until an intermediate or final result is produced. In a program designed to provide a set of interactive workflows, you can envision the data instead as a set of related data objects -- documents perhaps, or account credentials, or card catalog records, or all of the above -- upon which the program performs operations at the request of the user. The objects are like a lattice of interrelated data, waiting to be tickled or touched in exactly the right way. Classes fit this paradigm perfectly.

We also don't get many _opportunities_ to define our own classes when we are doing math. Need a matrix? There is the [NumPy](http://www.numpy.org/) array class. Need a time series? There is the [pandas](http://pandas.pydata.org/) Series class. Need a matrix that does relational joins fast? There is the pandas DataFrame class. Math-wise there is a lot of work already done for us. It would be silly to reinvent the wheel. True, it would be great if someone created a sparse matrix class that allowed relational joins (neither `scipy.sparse` nor `pandas.SparseDataFrame` do). But defining classes cannot be an end in itself.

Maybe that applies to non-math code as well.

<iframe width="420" height="315" src="https://www.youtube.com/embed/o9pEzgHorH0" frameborder="0" allowfullscreen></iframe>

Granted, using a language like Python or Ruby without defining classes may feel weird. It feels like we are not doing actual object-oriented programming. And we are not quite doing functional programming either, since we mutate data, our functions have side-effects, and most of us don't use lambda calculus. So we are in a sort of programming limbo. Perhaps we should just embrace the functional paradigm wholeheartedly and switch to Haskell or Scheme. Alas, that is hard to do after learning to love Python or Ruby, what with their intuitive syntaxes and extensive libraries, and so many people to answer our questions on StackOverflow. So maybe we should just learn to love the limbo.
