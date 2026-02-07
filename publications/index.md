---
layout: page
title: publications
---

<strong>book chapter</strong>:

Chapter 9 in <a href="https://www.amazon.com/Non-Academic-Careers-Quantitative-Social-Scientists-ebook/dp/B0C6D4YKT6/">Non-Academic Careers for Quantitative Social Scientists</a> (Springer, 2023).

<strong>peer-reviewed</strong>:

<a href="https://www.scielo.br/j/rbe/a/DJjtmWw4ZYjVyLMXHXBWx4P/">A note on real estate appraisal in Brazil</a>. (with Rodrigo Peres and Leonardo Sales). Brazilian Review of Economics, 75(1), 29-36, 2021. Brazilian banks commonly use linear regression to appraise real estate: they regress price on features like area, location, etc, and use the resulting model to estimate the market value of the target property. But Brazilian banks do not test the predictive performance of those models, which for all we know are no better than random guesses. That introduces huge inefficiencies in the real estate market. Here we propose a machine learning approach to the problem. We use real estate data scraped from 15 thousand online listings and use it to fit a boosted trees model. The resulting model has a median absolute error of 8,16%. We provide all data and source code. <u>Data and code</u> It's all [here](https://github.com/thiagomarzagao/wimoveis). 

<a href="http://bibliotecadigital.fgv.br/ojs/index.php/bre/article/view/58160">Automated Democracy Scores</a>. Brazilian Review of Econometrics, 37(1), 31-43, 2017. In this paper I use natural language processing to create the first machine-coded democracy index, which I call Automated Democracy Scores (ADS). I base the ADS on 42 million news articles from 6,043 different sources. The ADS cover all independent countries in the 1993-2012 period. Unlike the democracy indices we have today the ADS are replicable and have standard errors small enough to actually distinguish between cases. (I also wrote a <a href="https://arxiv.org/abs/1502.06161">related paper</a> where I try a bunch of other methods - LSA, LDA, Random Forest.) <u>Data and code</u> I created a <a href="http://democracy-scores.org">web app</a> that lets anyone tweak the training data and see how the results change - without having to write any code. If you do want to see the gory details, [here](https://gist.githubusercontent.com/thiagomarzagao/51ee10feb5e5c6762403d68dc2a635ff/raw/67aef2a1408b1781000e5f9bf54c25b6ecfc19d2/howto.html)'s what you need to know. 

<a href="http://ieeexplore.ieee.org/document/7838276/">Deep Learning Anomaly Detection as Support Fraud Investigation in Brazilian Exports and Anti-Money Laundering</a> (with Ebberth Paula, Marcelo Ladeira, and Rommel Carvalho). 15th IEEE International Conference on Machine Learning and Applications (ICMLA), 2016. Here we use deep learning to detect fake Brazilian exports. <u>Data and code</u> Sorry, it's company-level data and therefore protected by Brazilian privacy laws (only had access to it because co-author works at Brazil's tax authority.)

<a href="http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-62762013000200002">A dimensão geográfica das eleições brasileiras</a> (“The spatial dimension of Brazilian elections”). Opinião Pública (Public Opinion), 19(2), 270-290, 2013. Here I use spatial econometrics and the Brazilian election of 2010 to understand why neighboring counties tend to vote similarly. The <a href="/assets/spatial.pdf">preprint</a> is in English. <u>Data and code</u>. I used a mix of Stata (<a href="https://gist.github.com/thiagomarzagao/0542e82973ea86d78a03">here</a>) and R (<a href="https://gist.github.com/thiagomarzagao/fd1d86ec744b6d6430c3">here</a>) code. The dataset is <a href="/assets/replication/Brazil2010election.dta">here</a> (it's in Stata format; convert it to CSV format to run the R code). The list of missing observations is <a href="/assets/replication/missingdata.xlsx">here</a>. (To produce the plots I used GeoDa and ArcGIS, using the respective GUIs, so there's no code for those.)

<a href="http://www.scielo.br/pdf/rbe/v62n3/a02v62n3.pdf">Lobby e protecionismo no Brasil contemporâneo</a> (“Lobby and protectionism in Brazil”). Revista Brasileira de Economia (Brazilian Review of Economics), 62(3), 263-178, 2008. Here I regress tariffs on industry-level indicators of political power (economic concentration, number of workers, etc). <u>Data and code</u>. I ran everything almost a decade ago and back then I used Excel spreadsheets to store data (<a href="http://lemire.me/blog/archives/2014/05/23/you-shouldnt-use-a-spreadsheet-for-important-work-i-mean-it/">I know, I know...</a>) and I clicked buttons instead of writing code (I didn't know any better), so I don't have much to offer here. The spreadsheets are all in <a href="/assets/replication/REPLICATION+MATERIAL.zip">this zipped folder</a>.

<strong>not peer-reviewed (yet)</strong>:

[Predictors of long-term resistance exercise adherence among beginners
](https://sportrxiv.org/index.php/server/preprint/view/709/version/894) (2026). With Federica Conti, Andy Galpin, and Brad Schoenfeld. Here we mine Fitbod's data to find the predictors of long-term strength training adherence.

[Insider trading in Brazil's stock market]([https://osf.io/fu9mg/](https://ideas.repec.org/p/osf/osfxxx/fu9mg.html)) (2021). Here I estimate the probability of insider trading for each stock in Brazil's stock market, for each quarter from 2019Q4 through 2021Q1.

[Putting a price on tenure](https://osf.io/dvy9w/) (2021). Here I estimate how much tenure is worth in $ to the employees who benefit from it.

[Using SVM to pre-classify government expenditures](http://arxiv.org/abs/1601.02680)<a name="classify"></a> (2015). Here I use support vector machines (SVM) to create an [app](https://github.com/thiagomarzagao/catmatfinder) that could reduce misclassification of government purchases in Brazil. The app suggests likely categories based on the description of the good being purchased.

<a href="/assets/replication/bias.pdf">Ideological bias in democracy measures</a> (2012). Here I use Monte Carlos to reassess some studies on the biases behind the Freedom House, Polity IV, etc. I find that the evidence of bias is robust but that we can't know which measures are biased or in what direction (e.g., for all we know the Freedom House may as well have a leftist bias, contrary to popular belief). <u>Data and code</u>. I used a mix of Stata (<a href="https://gist.github.com/thiagomarzagao/e49541433d474d11d1fb">here</a> and <a href="https://gist.github.com/thiagomarzagao/18fed6a8afbb484e0c9c">here</a>) and R (<a href="https://gist.github.com/thiagomarzagao/c916e2a3ce77ea23d9a8">here</a>) code. <a href="/assets/replication/data-bollenpaxton.dta">Here's</a> the data in Stata format; <a href="/assets/replication//bollenpaxtondata.csv">here's</a> the same data in CSV format (for the R code).

<a href="/assets/replication/democracy_in_retreat_Thiago_Marzaga%CC%83o.pdf">Why is democracy declining in Latin America?</a> (2011). Here I argue that Latin America’s “left turn” in the 2000s was accompanied by democratic erosion, as the new governments that came to power relied on constituencies that did not value democracy (which in turn reduced the electoral cost of suppressing press freedom, violating term limits, etc). <u>Data and code</u>. [Here](https://gist.github.com/thiagomarzagao/625cffa2023faad79ec443ab172b7284)'s the Stata do file and [here](/assets/replication/dataset.dta)'s the dta file.

<strong>newspaper articles</strong>:

<a href="http://www.estadao.com.br/noticias/impresso,o-terceiro-fracasso-do-mercosul,675591,0.htm">O terceiro fracasso do Mercosul</a> ("The third failure of Mercosur"). O Estado de São Paulo, 2/5/2011. Here I discuss why Mercosur failed to lock in the trade liberalization of the 1990s.

<a href="http://www.imil.org.br/artigos/o-preco-de-aceitar-a-venezuela/">O preço de aceitar a Venezuela</a> ("The price of accepting Venezuela"). O Estado de São Paulo, 5/28/2009. Here I discuss the policy consequences of Venezuela's entry into Mercosur (a trade bloc comprising Brazil, Argentina, Paraguay, Uruguay, and Venezuela).
