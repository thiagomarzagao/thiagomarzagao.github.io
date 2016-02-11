---
layout: post
title: Wordscores in Python
comments: true
---

The Python script below implements the ‘wordscores’ algorithm (see [Laver, M., Benoit, K., Garry, J. Extracting policy positions from political texts using words as data. American Political Science Review, 97(2), 2003, pp. 311-331](http://journals.cambridge.org/action/displayAbstract?fromPage=online&aid=152187)). It takes as inputs word-frequency matrices. These matrices must be in CSV format. The first column must contain the words, the second column must contain the absolute frequencies, and the third column must contain the relative frequencies (if there are additional columns they will simply be ignored). These matrices need to be in the specified input folder - change 'ipath' as needed (line 9). The output is a set of word scores, which is saved to a CSV file (line 52), and a set of document scores (and corresponding confidence intervals), which are printed on the screen (lines 102-115) and saved to a CSV file (line 118). These CSV files are saved to the specified output folder - change 'opath' as needed (line 10).

Because this script processes one file at a time, it can handle corpora that are too large to fit in memory (unlike the R and Stata versions).

<script src="https://gist.github.com/thiagomarzagao/68ee390967893c9b6de9.js"></script>