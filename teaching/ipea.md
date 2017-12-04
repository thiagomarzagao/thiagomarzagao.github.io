---
layout: page
title: ipea
mostra: nao
---

<strong>
APRENDIZAGEM DE MÁQUINA USANDO PYTHON - 2/2017 - IPEA
</strong>

(Última atualização: 04/12/2017)

**Objetivo da disciplina**:

- Ao final do curso o aluno deverá ser capaz de usar corretamente algumas das principais ferramentas de mineração de dados: regressão, classificação e clusterização; Python.

**Pré-requisitos**:

- Não há pré-requisitos. Algum conhecimento de estatística básica de cálculo pode ser útil mas não é necessário nem esperado.

**Dia, horário e local**:

- Terças e quintas, das 9:00 às 11:00, de 14/11 a 14/12, no laboratório de informática do 6o andar do edifício-sede do IPEA.

**Comunicação**:

- A comunicação com o professor e com os demais alunos será por meio de time no Slack: [https://join.slack.com/t/ipea-ml/signup](https://join.slack.com/t/ipea-ml/signup) Você pode se juntar ao time informando seu email @ipea.gov.br
- Uma vez no time você pode postar dúvidas, respostas, pedaços de código, etc, no canal #general, que é visível a todos os participantes. Também é possível enviar mensagens privadas dentro do time.
- Não use o time p/ postagem de piadas, correntes, etc.
- O Slack é o único canal de comunicação com o professor. Emails provavelmente serão ignorados.

**Avaliação**:

- Trabalho final. O trabalho deverá consistir na aplicação de uma ou mais técnicas aprendidas no curso (classificação, clusterização, regressão) a problema concreto de interesse do aluno. O problema deverá ser previamente discutido com e aprovado pelo professor.
- O trabalho é individual. 
- O trabalho será avaliado com base: i) na adequação do(s) método(s) empregados(s) ao problema; ii) no uso e interpretação corretos do(s) método(s); iii) na clareza e precisão ao descrever o problema e o(s) método(s) empregado(s).
- O trabalho final não precisa ser um paper publicável. A idéia é apenas o aluno demonstrar domínio de pelo menos uma das ferramentas aprendidas ao longo do curso. Não há necessidade de revisão de literatura ou discussão teórica. Um trabalho final de ~5 páginas é perfeitamente aceitável.
- O trabalho final pode ser em português ou em inglês.
- O trabalho final deverá ser postado no canal #general do time no Slack. Dessa forma todo mundo verá o trabalho de todo mundo.
- Além do trabalho final o aluno deverá postar também os scripts e datasets utilizados.
- <font color="red">O prazo para postar o trabalho final é 23:59 do dia 15/12. Não serão aceitos trabalhos entregues fora do prazo.</font>
- Plágio resultará na reprovação do aluno, no encaminhamento do caso às áreas competentes do IPEA e na inclusão do nome do aluno no [Cheaters Hall](/teaching/cheaters_hall).

<strong>Plano de aulas:</strong>

<strong>1. motivação: para que serve mineração de dados?</strong>

- aplicações
    - recommender systems (Amazon, Netflix)
    - detecção de fraude (cartões de crédito, cartéis)
    - AI (Siri, carros autônomos)
    - mercado financeiro (seleção de ativos)
    - textos (atribuição de autoria, classificação)
- outline do curso (tópicos, material didático, avaliação)
- leitura obrigatória:
    - [Machine Learning for the Social Sciences](https://www.youtube.com/watch?v=oqfKz-PP9FU)
    - [We Are All Social Scientists Now: How Big Data, Machine Learning, and Causal Inference Work Together](http://stanford.edu/~jgrimmer/bd_2.pdf)
    - [The End of Theory: The Data Deluge Makes the Scientific Method Obsolete](http://www.wired.com/2008/06/pb-theory/)
- [slides](/assets/teaching/ipea/slides1.pdf)

<strong>2. introdução à programação</strong>

- Python
- str, int, float
- condicionais (IF/ELSE)
- operadores (AND/OR/NOT)
- FOR loops
- listas, conjuntos, dicionários
- funções
- pacotes
- leitura opcional:
    - [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/), caps. 0-6
- [slides](/assets/teaching/ipea/slides2.pdf)

<strong>3. pré-processamento</strong>

- pandas
- problemas comuns:
    - int/float como str
    - formatos inconsistentes
    - missing data
    - etc
- leitura obrigatória:
    - [The Quartz guide to bad data](https://github.com/Quartz/bad-data-guide)
- datasets usados na aula:
    - [municipios.csv](/assets/teaching/ipea/municipios.csv)
- [slides](/assets/teaching/ipea/slides3.pdf)

<strong>4. árvores de decisão & validação</strong>

- árvores de decisão simples
- random forest
- validação de modelos
    - métricas de desempenho: precisão, recall, etc
    - validação cruzada
- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 303-323
    - [Introduction to Data Mining](http://www-users.cs.umn.edu/~kumar/dmbook/ch4.pdf), pp. 145-205
- leitura opcional:
    - [Predicting the Behavior of the Supreme Court of the United States: A General Approach](http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2463244)
    - [The Politics of Need: Examining Governors' Decisions to Oppose the "Obamacare" Medicaid Expansion](http://spa.sagepub.com/content/14/4/437.short)
- [slides](/assets/teaching/ipea/slides5.pdf)

<strong>5. árvores de decisão & validação II</strong>

- [matematica.csv](/assets/teaching/ipea/matematica.csv)
- [matematica.py](/assets/teaching/ipea/matematica.py)
- [condicional.csv](/assets/teaching/ipea/condicional.csv)
- [condicional.py](/assets/teaching/ipea/condicional.py)

<strong>6. máquinas de suporte vetorial & parameter tuning & seleção de modelos</strong>

- SVM
    - soft margin
    - kernel trick
- parameter tuning
- seleção de modelos
- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 337-356
    - [grid search no scikit-learn](http://scikit-learn.org/stable/modules/grid_search.html)
    - [Automating Machine Learning](https://speakerdeck.com/amueller/automating-machine-learning)
- leitura opcional:
    - [Language and Ideology in Congress](http://journals.cambridge.org/action/displayAbstract?fromPage=online&aid=8444227&fileId=S0007123411000160)
- [slides](/assets/teaching/ipea/slides6.pdf)
- [matematica_svm.py](/assets/teaching/ipea/matematica_svm.py)
- [condicional_svm.py](/assets/teaching/ipea/condicional_svm.py)

<strong>7. clusterização</strong>

- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 385-390
    - [Introduction to Data Mining](http://www-users.cs.umn.edu/~kumar/dmbook/ch8.pdf), pp. 487-568
- leitura opcional:
    - [Classificando regimes políticos utilizando análise de conglomerados](http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-62762012000100006)
    - [Financiamento de campanha e apoio parlamentar à Agenda Legislativa da Indústria na Câmara dos Deputados](http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-62762015000100033)
- [slides](/assets/teaching/ipea/clustering.pdf)
- exercício 1:
- [municipios.py](/assets/teaching/ipea/municipios.py)
- [municipios.csv](/assets/teaching/ipea/municipios.csv)
- exercício 2:
- [movies.py](/assets/teaching/ipea/movies.py)
- [ml-latest.zip](http://files.grouplens.org/datasets/movielens/ml-latest.zip)
- exercício 3:
- [olimpiadas.py](/assets/teaching/ipea/olimpiadas.py)
- [summer.csv](https://www.kaggle.com/the-guardian/olympic-games/downloads/summer.csv)

<strong>8. mineração de textos</strong>

- bag of words
- matriz de termos-freqüências
- normalização
- TF-IDF
- pré-processamento
- leitura obrigatória:
    - [Introduction to Information Retrieval](http://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf), pp. 109-133
    - [Text as Data: The Promise and Pitfalls of Automatic Content
Analysis Methods for Political Texts](http://web.stanford.edu/~jgrimmer/tad2.pdf)
- [slides](/assets/teaching/ipea/slides8a.pdf)

<strong>9. redução de dimensionalidade & extração de tópicos</strong>

- LSA
- LDA
- leitura opcional:
    - [Introduction to Information Retrieval](http://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf), pp. 403-417
    - [Latent Dirichlet Allocation](http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)
    - [aula de LDA com um dos criadores do modelo](https://www.youtube.com/watch?v=DDq3OVp9dNA)
    - [Online Learning for Latent Dirichlet Allocation](https://www.cs.princeton.edu/~blei/papers/HoffmanBleiBach2010b.pdf)
- [slides](/assets/teaching/ipea/slides8b.pdf)

<strong>10. raspagem de sites</strong>

- com APIs
    - Vagalume, Twitter (Streaming API vs Search API), Facebook (Graph API)
    - diferença entre usar HTTP diretamente e usar pacotes
        - requests
        - Tweepy
    - metadados
    - JSON
    - limites por minuto
    - 'while True' p/ contornar erros
- sem APIs
    - HTML, CSS, JavaScript: o código-fonte da página
    - BeautifulSoup
    - Selenium
    - captchas (http://www.deathbycaptcha.com)
- expressões regulares
- resultado é probabilístico (time.sleep(), try/catch)
- leitura obrigatória:
    - webscraping with Selenium (partes [1](http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/), [2](http://thiagomarzagao.com/2013/11/14/webscraping-with-selenium-part-2/), [3](http://thiagomarzagao.com/2013/11/15/webscraping-with-selenium-part-3/), [4](http://thiagomarzagao.com/2013/11/16/webscraping-with-selenium-part-4/) e [5](http://thiagomarzagao.com/2013/11/17/webscraping-with-selenium-part-5/))
- [raspa_vagalume.py](/assets/teaching/ipea/raspa_vagalume.py)
- [raspa_twitter.py](/assets/teaching/ipea/raspa_twitter.py)
- [raspa_scielo.py](/assets/teaching/ipea/raspa_scielo.py)
- [raspa_scielo_2.py](/assets/teaching/ipea/raspa_scielo_2.py)
- [regex.py](/assets/teaching/ipea/regex.py)

<strong>11. regressão linear</strong>

- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 61-109
- leitura opcional:
    - [Basic Econometrics](http://www.amazon.com/Basic-Econometrics-Damodar-Gujarati/dp/0073375772/ref=sr_1_1?ie=UTF8&qid=1448210562&sr=8-1&keywords=basic+econometrics), pp. 13-96
    - [Estatística Básica](http://www.livrariacultura.com.br/p/estatistica-basica-61737525), pp. 454-503
    - [Basic Econometrics](http://www.amazon.com/Basic-Econometrics-Damodar-Gujarati/dp/0073375772/ref=sr_1_1?ie=UTF8&qid=1448210562&sr=8-1&keywords=basic+econometrics), pp. 188-232
    - [Forecasting U.S. House Elections](http://www.jstor.org/stable/439492) (sem acesso ao JSTOR? [Sci-Hub](http://www.sci-hub.bz))
- [slides](/assets/teaching/ipea/slides4a.pdf) (regressão linear simples)
- [slides](/assets/teaching/ipea/slides4b.pdf) (regressão linear múltipla)
- [dataset](/assets/teaching/ipea/dados_regressao.csv) usado na aula