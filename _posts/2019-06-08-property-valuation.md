---
comments: true
layout: post
title: how much is your apartment worth?
---

I'm buying an apartment and in the process I've learned a lot about property valuation. I've learned that there are people who do that for a living, that there are academic researchers who specialize in the subject, and that there is even regulation and licensing requirements. 

In particular, I've learned that people are using statistical models - like linear regression - to appraise properties. I thought that was super cool, so I got curious and read a bunch of model-based appraisal reports. And that, dear reader, was a fascinating lesson in the misuse of quantitative tools. And by the entities we'd expect to be most proficient in their use: banks.

In what follows I show how Brazilian banks are doing it today and why it's seriously messed up. Then in part 2 (forthcoming) I'll show a better way to do it.

(Trigger warning: if you've recently bought or sold property in Brazil, and if you paid those obscene appraisal fees that Brazilian banks charge, you may want to save yourself some aggravation and stop reading here.)

**regression and Rio**

The folks using statistical models to appraise real estate in Brazil are usually banks. If you don't pay your mortgage the bank gets your property, so the bank needs to know beforehand whether the property is worth enough $.

In Brazil [70%](https://www1.folha.uol.com.br/mercado/2018/09/volume-de-credito-imobiliario-e-metade-do-concedido-ha-quatro-anos.shtml) of all mortgages are concentrated in one bank: Caixa Econômica Federal (CEF), which is owned by the state. You'd think that the bank with the most mortgages would be pretty good at estimating the value of real estate. You'd be wrong.

I downloaded dozens of property valuation reports by CEF. Well, they are not actually made by CEF: CEF outsources the appraisals to other companies. But CEF reviews and approves every appraisal report. And in any case the ultimate responsibility rests with CEF.

Let's look at [this](https://www.brameleiloes.com.br/principal/pub/Image/20181025040759LAUDO_CAIXA.pdf) report, which is pretty typical.

The property here is a plot of 41.695m<sup>2</sup> in a small town not far from Rio de Janeiro (about 100km away). The appraiser started by gathering data on 38 other plots, all in the same small town. For each of the plots he collected four variables: area (in m<sup>2</sup>), whether the lot is paved, average family income of the area, and price (in R$) per m<sup>2</sup>. Then he dropped 13 of the 38 samples and used the remaining 25 to run a linear regression: price per m<sup>2</sup> ~ area + paved + income. He then used the resulting model to estimate the price of the original plot. The resulting estimate was R$ 1.056.866,78, with an 80% confidence interval of [R$ 898.423,01, R$ 1.215.513,48]. The appraiser saw fit to manually adjust the estimated value to R$ 990.000,00 because, well, there's some stuff that the model doesn't capture.

There is a lot that's wrong here, but the main thing is: the appraiser doesn't test the model.

Normally, in machine learning tasks like this, we train the model using only a subset of the samples, ask the model to produce estimates for the samples that were left out, then check how close these estimates are to the actual values. Ideally we repeat this several times over, rotating which samples are left out at each iteration.

But here there is no separation between training and testing. The appraiser used 100% of the 25 samples to train the model. There were no samples left for testing the model. So we have absolutely no idea how good or bad the model is. Maybe the actual market value of the plot is indeed close to R$ 1.056.866,78. But maybe it's R$ 2 million. Or R$ 500k. We have no idea. Since the model isn't tested, its performance is a complete mystery.

<a href="https://imgur.com/s55GvZa"><img src="https://i.imgur.com/s55GvZa.jpg" title="source: imgur.com" /></a>

In response to which the appraiser may direct your attention to page 11 of the report, where you see this scatter plot of observed vs estimated values:

<a href="https://imgur.com/nfxEGTy"><img src="https://i.imgur.com/nfxEGTy.png" title="source: imgur.com" /></a>

Clearly the model has a tremendously good fit: all estimates are super close to the actual values.

Except that that's cheating: the appraiser used the same 25 samples for both training *and* testing the model. You don't know a model's performance until it has been subjected to samples it hasn't seen before.

Not that it would make much sense to split training and testing samples with n=25. But if n=25 the thing to do is get more samples (more on this later). A small sample size doesn't give you a license to simply not test your model.

**"but that's just one report"**

Nope, that's how every single model-based appraisal report I downloaded does it. Every. Single. One. No exceptions. At all. Google 'CEF laudo imóvel' or 'Caixa Econômica laudo imóvel' or 'laudo avaliação imóvel' and check for yourself. The only appraisals that are not like that are the ones that don't use any statistical model whatsoever.

In other words: billions of R$ in real estate transactions are based on property valuations that are completely worthless.

**let's worry about all the wrong things**

If you ask the appraiser why he didn't test the model he'll be genuinely shocked and answer that he did test it. And he did run a bunch of tests, as it's clear on the report: he tested whether the residuals are normally distributed, whether each coefficient is statistically significant, whether the model as a whole is statistically significant, and so on. Other reports go as for as testing for heteroskedasticity and autocorrelation.

None of which makes the slightest sense here. This is not an econometrics problem. We're not interested in the effect of each additional m<sup>2</sup> on the price of the property. This is a machine learning problem. We're interested in producing price estimates as close as possible to the actual prices. We don't care about the assumptions behind linear regression in this context.

In fact we don't care about linear regression at all. The appraiser could have (and probably should have) used boosted trees or any other machine learning algorithm. The way to go about these things is to try different algorithms and pick the one that produced the best estimates. There is no reason to limit yourself to linear regression.

**regulation and its unintended consequences**

To be fair, this is not entirely the appraiser's fault. It turns out that there is a set of semi-official guidelines for how to use linear regression to do property valuation. That's regulation [NBR-14653-2](http://bittarpericias.com.br/wp-content/uploads/2017/02/Avaliacao-Bens-Imoveis-Urbanos-Procedimentos-Gerias-NBR-14653-2.pdf). It is not legally binding - you don't go to jail or lose your license if you violate it. But it ends up being enforced anyway. CEF won't subcontract your company to do appraisals if you don't follow it.

Regulation NBR-14653-2 tells appraisers to check for normality of the residuals, heteroskedasticity, autocorrelation, etc. It doesn't say a word about testing the performance of the model. It's completely silent on the topic of training vs testing samples, cross validation, accuracy, etc. In other words, regulation NBR-14653-2 recommends an econometric approach to a machine learning problem, which is bonkers.

**more wrongness (and a lesson in public policy)**

Suppose for a moment that the econometric approach were the right one here. Even then the current appraisals would be worthless.

Take the report we discussed before. The sample size is 25. That's just not good enough. "Oh, but it's a small town, there probably aren't that many plots for sale." Yes, but Brazil has over five thousand small towns. Your samples don't need to be in the same town where the property you're appraising is. Yes, different towns will differ in GDP per capita, homicide rate, etc. But we have data on all that, so we can include those indicators in our models. And/or dummify "name of town".

Such a small sample is particularly egregious here, since CEF has 70% of all mortgages in Brazil, so they surely have a ton of data they could have used (or shared with the company they contracted to do the job). Imagine having millions of samples and then using only 25.

<blockquote class="imgur-embed-pub" lang="en" data-id="a/QcGxS4V"><a href="//imgur.com/QcGxS4V"></a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>

(I suspect this has to do with appraisers' lack of programming skills. They use software with graphical interfaces and probably just type every data point manually. So 1 million samples would be of no use to them. But I'm just guessing here.)

Also, the appraiser doesn't tell us which 25 - out of the original 38 - samples he actually used in the regression. I considered trying to replicate his results but there are 5.414.950.296 possible combinations of 25 elements out of 38, so that might take a while to run.

The appraiser also doesn't tell us *why* he dropped 13 of the 38 original samples. Were they outliers? Or maybe dropping them helped produce that incredible R<sup>2</sup> of 0.98 we see on page 9...?

At times it feels like the appraiser doesn't really understand what he is doing. Like when he reports a p-value for the dependent variable (R$ per m<sup>2</sup>). Only independent variables have coefficients. Maybe he is confusing the constant and the dependent variable?

I also don't know what the variable "average family income in the area" means or where it comes from. What's "area" here? The neighborhood? The block? The zip code? What's the source? He says it comes from "senso", a misspelling of "censo" - census. But I have no idea which census he is talking about.

It's also weird that he codes "is paved?" as no=1 and yes=2, instead of no=0 and yes=1.

So, just like in the other reports I read, I get the sense that the appraiser doesn't have any quantitative training. It looks like all he can do is operate the software that produces the estimates (appraisers seem to like [SisDEA](https://pellisistemas.com/software/sisdea/)). You input the data, you press this and that button, the software spits out content that mostly looks Greek to you (some of it is actual Greek), plus an estimate for the property you're supposed to appraise. You copy and paste everything into a Word document, save it as a PDF file and email it to your client. That's the job.

The stuff you copied and pasted contains, among other things, tests of the assumptions behind linear regression. You don't understand any of that, but you see words that also appear on regulation NBR-14653-2 - normality, heteroskedasticity, autocorrelation -, so clearly you're following the rules. No one can yell at you or fire you, right?

In other words, regulation substitutes for actual knowledge.

(Let this be a lesson to the perpetually outraged online mobs demanding that algorithms be regulated. They think they'll get Andrew Ng to write the regulations, but Andrew Ng has better things to do. In the real world regulations are produced by a mix of bureaucrats with no skin in the game and politicians with too much skin in the game.)

**"well, criticizing is easy! why don't you do something about it instead?"**

Fair enough. In part 2 I'll show how we can improve things.