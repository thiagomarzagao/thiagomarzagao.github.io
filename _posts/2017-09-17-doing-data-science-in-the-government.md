---
comments: true
layout: post
title: doing data science in the government
---

Today it's been three years since I first started working as a data scientist in the Brazilian government. Overall it's been a great experience and I think this is a good time to reflect upon what I've learned so far. I'll start with the ugly and the bad and then I'll move on to the good.

**bureaucrats won't share data unless physically compelled to do so**

There is no shortage of decrees saying that government agencies will give their data to other government agencies when requested to do so ([here](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2016/decreto/d8789.htm)'s the latest one). But between the pretty text of the law and what really goes on in the intestines of the bureaucracy there is a huge gap. Every government agency is in favor of data sharing - except when it comes to its own data.

Excuses abound. I can't share my data because it's too sensitive. I can't share my data because extracting it would be too costly. I can't share my data because we're in the middle of a major IT restructuring and things are too messy right now. I can't share my data because we've lost its documentation. I can't share my data because the IT guy is on vacation. I can't share my data because you might misinterpret it (this is my favorite).

<img src="https://i.imgur.com/ZduSiik.png" align="right"> The actual reasons are not always easy to pinpoint. Sometimes there are legitimate concerns about privacy, as in the case of fiscal data. But this is rare. More often than not the alleged privacy concerns are just a convenient excuse. In some cases the privacy excuse is used even when the data is already public. For instance, everything the government buys (other than, say, spy gear) goes in the [official bulletin](http://portal.imprensanacional.gov.br/), which anyone can read. The equivalent of the IRS in Brazil - [Receita Federal](https://idg.receita.fazenda.gov.br/) - has all the corresponding tax invoices neatly collected and organized in a database. That database would make it much easier to compute, say, the average price the Brazilian government pays for ballpoint pens. You'd think that database would be readily available not just for the entire government but for the citizenry as well.

You'd be wrong. Government agencies have been trying - and failing - to put their hands in that database for years. Our IRS says it's protected by privacy laws. But the law says that government purchases must be public. And they already are, it's all in the official bulletin - but that's unstructured data that would require lots of scraping, OCRing, and parsing. The data is already public but not in a machine-readable format. That's why the IRS database is so valuable. But the IRS legal folks haven't found their match yet.

(Meanwhile data that is actually sensitive - like people's addresses and tax returns - can be bought for $10 from shady vendors not too hard to find; all it takes is a walk along [Rua 25 de Março](https://en.wikipedia.org/wiki/Rua_25_de_Mar%C3%A7o), in São Paulo. In Brazil if the government has any data on you then you can be sure it's for sale at Rua 25 de Março.)

Sometimes bureaucrats don't share data because they worry that the data will make them look bad. What if my data shows that I'm paying too much for office paper? What if my data shows that I have way more people than I need? What if my data shows that my agency is a complete waste of taxpayers' money and should not exist? I suppose I understand the survival instinct behind such concerns, but those are precisely the cases where we absolutely must get the data, for that's where the ugliest inefficiencies are. In general the more an agency refuses to share its data the more important it is to get it.

(It doesn't help that I work for the Office of the Comptroller-General, whose main goal is to find and punish irregularities involving taxpayers' money. People sometimes assume that our asking for their data is the prelude of bad things. We need to explain that inside the Office of the Comptroller-General there is this little unit called the Observatory of Public Spending and that our goal at the OPS is often to *help* other agencies by extracting insights from their data.)

**government data is a mess**

The idea that you should document your databases is something that hasn't taken root in the Brazilian government. Nine times out of ten all you get is a MSSQL dump with no accompanying data dictionary. You try to guess the contents based on the names of the tables and columns, but these are usually uninformative (like `D_CNTR_IN_APOSTILAMENTO` or `SF_TB_SP_TAB_REM_GDM_PST` - both real-life examples). So you end up guessing based on the contents themselves. As in: if it's an 11-digit numeric field then that's probably the Brazilian equivalent of the Social Security Number.

As you might imagine, sometimes you guess wrong. You mistake quantity for total price and vice-versa and the resulting unit prices don't make any sense. You think that a time field is in years but it's actually in months. You mistake an ID field for a numeric field. Etc etc. You're lucky when you catch the errors before whatever you're doing becomes policy. And some fields you just leave unused because they are too mysterious and you can't come up with any reasonable guesses. Like when it's probably a dummy variable because the values are all 0s and 1s but you have no clue what the 0s and 1s mean.

Besides the lack of documentation there are also many errors. Null names, misclassification, missing data, typos (according to one database the Brazilian government signed an IT contract of US$ 1 quadrillion back in 2014 - that's 26 times the budget of the entire US government). To give you an idea, half the government purchases classified as "wheeled vehicles" are under R$ 1,000 (roughly US$ 300); when we inspect the product descriptions we see that they are not actually vehicles but spare parts, which have a different code and should have been classified elsewhere.

<img src="https://i.imgur.com/FoF9zbC.jpg" align="left"> The problem begins in the data generation process, i.e., in the systems bureaucrats use to enter the data. These systems are too permissive; they lack basic validation like checking input type (numeric, text, date, etc), input length (does the state code have more than two characters?), and the like. And there is no punishment for the bureaucrat who enters incorrect data.

The most frequent result is absurd averages. You try to compute, say, spending per employee, and what you get back is a bazillion dollars or something close to zero. That means many hours of data cleaning before we can really get started. You have to do all the sanity checks that the government systems fail to do - or else it's garbage in, garbage out. After you've filtered out the US$ 1 quadrillion IT contracts and the US$ 0 hospitals and schools you are left with lots of missing data - and that's often not missing at random, which poses additional problems. It's no wonder that most of our academic work is about cleaning up data (like [here](https://arxiv.org/abs/1601.02680) and [here](http://www.lbd.dcc.ufmg.br/colecoes/eniac/2013/0033.pdf)).

**recruiting is a different ball game**

The Brazilian government does not deliberately recruit data scientists. Data scientists come in through a bunch of miscellaneous doors and then we find each other - by word-of-mouth or Twitter or conferences - and come up with ways to work together. By now there are a few well-known "data science places" in the government - like the [OPS](http://www.cgu.gov.br/assuntos/informacoes-estrategicas/observatorio-da-despesa-publica) (where I work) and the [TCU](http://portal.tcu.gov.br/inicio/index.htm) - and data-curious government employees have been flocking to them, by various means; but there isn't a clear policy to attract data talent.

In order to enter the Brazilian government you usually have to pass a public exam and such exams do not cover any content even remotely related to data. What you do need to learn to pass these exams is a large number of arcane pieces of legislation, mostly relating to government procedures - like the three phases of a procurement process, what they are called, what the deadlines are, what the many exceptions are, and so on. As you may imagine, that doesn't usually attract people interested in data. A few of us slip through the cracks somehow, but that's largely by accident.

That makes recruiting for your team a lot harder than in the private sector, where you can simply post a job ad on LinkedIN and wait for applications. In the government you normally can't recruit people that are not already in the government. It goes more or less like this: You start by identifying the person you want to bring to your team. He or she will usually be in another government agency, not in your own. You will need to negotiate with his or her agency so that they okay their coming to work for you. That may require you to find someone in your agency willing to go work for them. Such negotiations can last for months and they look a lot like an exchange of war prisoners (I was "traded" myself once and it's not fun). If the head of your agency (your minister or whatever) has sufficient political clout (and know that you exist), he or she may try to prevail over his or her counterpart at the other agency. Either way, there's no guarantee that you'll succeed.

<center><img src="https://i.imgur.com/tcXJVm4.jpg"></center>

If it's hard for the recruiter it's even harder for the person being recruited. They need to tell their current agency that they no longer want to work there, but they have no guarantee that they will get transferred. Imagine telling your significant other that you want to break up but then being somehow legally compelled to stay in the relationship. It can be awkward. You're unlikely get a promotion if your bosses know that you don't want to work there. They may start giving you less important tasks. Such possibilities often kill any recruitment before it even begins.

There is also the issue of salary negotiations. The issue being that they are not possible. When you work for the government the law determines your salary - there is no room for negotiation. Sometimes you can offer a potential candidate a little extra money if they agree to take up some administrative responsibilities but this is usually under US$ 1000/month and most data scientists prefer to avoid having any responsibilities that involve paperwork. So whoever you are trying to lure must be really excited by the work you and your team do because the work itself is pretty much all you have to offer.

But enough with the bad and the ugly.

**you have a lot of freedom to experiment**

Paradoxically, in the midst of this red tape jungle we have a lot of leeway to play around and try new things. Data science is a highly technical subject, one that takes at least a few Coursera courses to even begin to grasp, and that helps keep it unregulated. We have to fill out the same stupid forms everyone else does when we want to buy stuff, but whether we use Hadoop or not, whether we adopt Python or R for a project, whether we go with an SVM or a neural network or both, and whether we think any given project is worth pursuing is all entirely up to us. Legal doesn't have a say in any of that. The budget folks don't have a say in any of that. The minister himself - heck, the president himself - doesn't have a say in any of that. They wouldn't even know where to start. So, thanks to the highly specialized nature of our trade we don't have higher-ups trying to micromanage what we do.

<img src="https://i.imgur.com/6JLCFSH.jpg" align="right"> There is also the tenure factor. You see, in Brazil once you enter the civil service you get automatically tenured after three years. And the constitution says that, once tenured, you need to do something really outrageous to get fired - and even then there are several appeal instances and often times nothing happens in the end. I bet that if I showed up naked for work tomorrow I still wouldn't get fired; I *might* get a written warning or something along these lines, and I'd probably appear in the local news, but I would still have my job. It takes something outright criminal to get a government employee fired. Like, they need to catch you taking a bribe or not showing up for work for months. And even then sometimes people don't get fired.

Overall tenure is bad: too many lazy idiots spend their days browsing Facebook and entertaining themselves with hallway gossip. But for experimenting purposes tenure is great. It makes "move fast and break things" possible. Some bureaucrats want our assistance and happily give us their data and collaborate with us, helping us understand their problems and needs. But other bureaucrats get upset that you're even daring to ask for their data. And they worry that you might disrupt the way they work or that you might automate them altogether. If we had to worry about our jobs at every step of the way we wouldn't accomplish much. Without tenure heads might roll.

**you can help taxpayers; a lot**

The Brazilian government is humongous - it takes up ~40% of the country's GDP. Most of that money goes down the toilet: the government overpays for everything it buys; it contracts suppliers that do not deliver the goods and services they promised; corruption is generalized. But data science can help. For instance, at the OPS we have trained a model that predicts whether a supplier is likely to become a headache (say, because it won't deliver or because it will shut down). ([Here](https://speakerdeck.com/thiagomarzagao/predicting-irregularities-in-public-bidding-an-application-of-neural-networks)'s a talk I gave about it earlier this year.) We're now refining that model so that we can later appify it and plug it into the government's procurement system. That way the government will be alerted of potential problems *before* it signs the contract. 

That project has taken a lot of time and effort - the first version of the model was the master's research of my colleague [Leonardo](https://twitter.com/leonardojs1981) and since then he and other people have put a lot more work into it. That's a lot of salary-hours. But if a single problematic contract of small size - say, US$ 100k or so - is prevented because of the model then all that effort will have been worth it. And given the size of the government's budget - around US$ 1 trillion a year - we should be able to save a lot more money than US$ 100k. That's money that could go back to taxpayers.

**is it worth it?**

If you can stomach the ugly and the bad and are excited about the good, then yes. :-)