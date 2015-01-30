---
layout: post
title: Julia's shortcomings
---

[Here](http://www.johnmyleswhite.com/notebook/2014/11/29/whats-wrong-with-statistics-in-julia/), by John Myles White. 

tl;dr: 

> The primary problem with statistical computing in Julia is that the current tools were all designed to emulate R. Unfortunately, R’s approach to statistical computing isn’t amenable to the kinds of static analysis techniques that Julia uses to produce efficient machine code.

And [here](http://danluu.com/julialang/), by Dan Luu. 

tl;dr:

> It’s not unusual to run into bugs when using a young language, but Julia has more than its share of bugs for something at its level of maturity. If you look at the test process, that’s basically inevitable. [...] Not only are existing tests not very good, most things aren’t tested at all.