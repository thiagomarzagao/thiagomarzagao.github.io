---
comments: true
layout: post
title: A better 1RM formula
---

New [manuscript](https://arxiv.org/abs/2603.17495). TL;DR: I used Fitbod data to find a better formula to estimate your one-rep-max (1RM) for a given exercise based on any arbitrary reps x weight combination.

Abstract:

> Classical equations for predicting one-repetition maximum (1RM) from submaximal performance were derived from small samples performing a single exercise, yet are routinely applied to hundreds of exercises. All use a fixed conversion factor relating repetitions to estimated 1RM, regardless of exercise or load. We used large-scale observational data from a consumer fitness app (303,494 near-failure sets from 14,966 users across 388 exercises spanning 16 muscle groups) to derive and evaluate a generalization in which the conversion factor varies logarithmically with the weight lifted: 1RM = w * (1 + (r - 1)^0.85 / (-2.55 + 4.58 * ln(w))). Because the dataset contains no directly measured maxima, we optimized and evaluated the formula using an internal consistency criterion -- the degree to which different weight-repetition combinations from the same person, exercise, and time window yield the same estimated 1RM. The proposed formula reduced inconsistency by 17-22% relative to four classical benchmarks, with the improvement positive for every one of the 183 exercises with sufficient data. Five-fold user-level cross-validation confirmed near-zero overfitting. An ablation analysis attributed 91% of the improvement to the weight-dependent conversion factor and 9% to the sub-linear repetition exponent. The conversion factor increases with load: at light weights each additional repetition implies a larger fraction of maximal capacity than at heavy weights, consistent with prior evidence that the repetitions-%1RM relationship varies by exercise. Classical equations, by applying a single conversion factor across all loads, systematically underestimate this variation -- and the discrepancy is largest for the lighter, more diverse exercises that dominate real-world training programs.
