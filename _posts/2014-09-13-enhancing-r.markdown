---
comments: true
layout: post
title: enhancing R
---

From [here](http://arxiv.org/pdf/1409.3144.pdf):



> I describe an approach to compiling common idioms in R code directly to native machine code and illustrate it with several examples. Not only can this yield significant performance gains, but it allows us to use new approaches to computing in R. Importantly, the compilation requires no changes to R itself, but is done entirely via R packages. This allows others to experiment with different compilation strategies and even to define new domain-specific languages within R. We use the Low-Level Virtual Machine (LLVM) compiler toolkit to create the native code and perform sophisticated optimizations on the code. By adopting this widely used software within R, we leverage its ability to generate code for different platforms such as CPUs and GPUs, and will continue to benefit from its ongoing development. This approach potentially allows us to develop high-level R code that is also fast, that can be compiled to work with different data representations and sources, and that could even be run outside of R. The approach aims to both provide a compiler for a limited subset of the R language and also to enable R programmers to write other compilers. This is another approach to help us write high-level descriptions of what we want to compute, not how.


