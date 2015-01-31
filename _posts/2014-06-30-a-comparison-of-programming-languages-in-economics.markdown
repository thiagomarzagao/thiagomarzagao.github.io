---
author: thiagomarzagao
comments: true
date: 2014-06-30 15:21:02+00:00
layout: post
slug: a-comparison-of-programming-languages-in-economics
title: a comparison of programming languages in economics
wordpress_id: 911
categories:
- Python
- stats
tags:
- C
- Fortran
- Julia
- Mathematica
- Python
- R
- stats
---

[Here](http://www.nber.org/papers/w20263?utm_campaign=ntw&utm_medium=email&utm_source=ntw).

Highlights:



> 1. C++ and Fortran are still considerably faster than any other alternative, although one needs to be careful with the choice of compiler.

> 2. C++ compilers have advanced enough that, contrary to the situation in the 1990s and some folk wisdom, C++ code runs slightly faster (5-7 percent) than Fortran code.

> 3. Julia, with its just-in-time compiler, delivers outstanding performance. Execution speed is only between 2.64 and 2.70 times the execution speed of the best C++ compiler.

> 4. Baseline Python was slow. Using the Pypy implementation, it runs around 44 times slower than in C++. Using the default CPython interpreter, the code runs between 155 and 269 times slower than in C++.

> 5. However, a relatively small rewriting of the code and the use of Numba (a just-in-time compiler for Python that uses decorators) dramatically improves Python’s performance: the decorated code runs only between 1.57 and 1.62 times slower than the best C++ executable.

> 6. Matlab is between 9 to 11 times slower than the best C++ executable. When combined with Mex files, though, the difference is only 1.24 to 1.64 times.

> 7. R runs between 500 to 700 times slower than C++. If the code is compiled, the code is between 240 to 340 times slower.

> 8. Mathematica can deliver excellent speed, about four times slower than C++, but only after a considerable rewriting of the code to take advantage of the peculiarities of the language. The baseline version our algorithm in Mathematica is much slower, even after taking advantage of Mathematica compilation.



