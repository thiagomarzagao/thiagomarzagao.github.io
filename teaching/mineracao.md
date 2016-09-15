---
layout: page
title: mineracao
mostra: nao
---

<strong>
MINERAÇÃO DE DADOS - 2/2016 - IPOL/UnB
</strong>

(Última atualização: 15/09/2016)

**Objetivo da disciplina**:

- Ao final do curso o aluno deverá ser capaz de usar corretamente algumas das principais ferramentas de mineração de dados: regressão, classificação e clusterização; computação em nuvem; Python.

**Pré-requisitos**:

- Não há pré-requisitos. Algum conhecimento de estatística básica de cálculo pode ser útil mas não é necessário nem esperado.

**Dia, horário e local**:

- Segundas-feiras, das 18:00 às 19:50, no laboratório de informática do Instituto de Ciência Política.

**Matrícula**:

- É a turma A da disciplina [Seminário em Ciência Política](https://www.matriculaweb.unb.br/posgraduacao/oferta_dados.aspx?cod=385433&dep=588), da pós-graduação (mestrado & doutorado) em ciência política da UnB. Há um número limitado de computadores disponíveis, portanto a participação de alunos de outros programas e de ouvintes depende de eventual sobra de vagas.

**Comunicação**:

- A comunicação com o professor e com os demais alunos será por meio de time no Slack: [https://mineracao.slack.com/signup](https://mineracao.slack.com/signup) Você pode se juntar ao time informando seu email @unb.br ou @aluno.unb.br
- Uma vez no time você pode postar dúvidas, respostas, pedaços de código, etc, no canal #general, que é visível a todos os participantes. Também é possível enviar mensagens privadas dentro do time.
- Não use o time p/ postagem de piadas, correntes, etc.
- O Slack é o único canal de comunicação com o professor. Emails provavelmente serão ignorados.

**Avaliação**:

- Trabalho final. O trabalho deverá consistir na aplicação de uma ou mais técnicas aprendidas no curso (classificação, clusterização, regressão) a problema concreto de interesse do aluno. O problema deverá ser previamente discutido com e aprovado pelo professor. 
- O trabalho é individual. 
- O trabalho será avaliado com base: i) na adequação do(s) método(s) empregados(s) ao problema; ii) no uso e interpretação corretos do(s) método(s); iii) na clareza e precisão ao descrever o problema e o(s) método(s) empregado(s).
- O aluno pode usar quaisquer linguagens de programação desde que sejam open source. Sugestões: [Python](https://www.python.org/) (veremos no curso), [R](https://www.r-project.org/), [Octave](https://www.gnu.org/software/octave/), [Julia](http://julialang.org/), [Scala](http://www.scala-lang.org/).
- Os scripts usados deverão ser disponibilizados publicamente no [GitHub](https://github.com/).
- Os datasets usados deverão ser disponibilizados publicamente em um dos seguintes repositórios: [OpenICPSR](https://www.openicpsr.org/), [DataVerse Network](http://dataverse.org/), [DataCite](https://www.datacite.org/) ou [AcademicTorrents](http://academictorrents.com/). Os datasets deverão estar em formato não-proprietário (nada de .dta, .sav, etc). Datasets que contêm microdados confidenciais devem ser mascarados (conversaremos sobre isso em sala).
- O trabalho final deverá ser disponibilizado no [SocArXiv](https://osf.io/view/socarxiv/) ou no [arXiv](http://arxiv.org/). O link p/ o trabalho final deverá ser postado no canal #general do nosso time no Slack (não é p/ enviar o arquivo do trabalho - .pdf, .tex, .docx, etc).
- <font color="red">O prazo para postar o link p/ o trabalho final é 23:59 do dia 2/12. Não serão aceitos trabalhos entregues fora do prazo.</font>
- Importante: tanto no arXiv quanto no SocArXiv as submissões levam alguns dias p/ serem processadas, portanto é preciso submeter o trabalho ao repositório escolhido com atencedência, para que o link esteja disponível até as 23:59 do dia 2/12.
- A comunidade open source trabalhou duro - e de graça - p/ criar os pacotes Python, R, etc, que você usou no seu trabalho. Retribua citando esses pacotes na bibliografia.
- Plágio resultará na reprovação do aluno, no encaminhamento do caso às áreas competentes da UnB e na inclusão do nome do aluno no [Cheaters Hall](/teaching/cheaters_hall).

<strong>Plano de aulas:</strong>

<strong>1. motivação: para que serve mineração de dados?</strong>

- aplicações
    - recommender systems (Amazon, Netflix)
    - detecção de fraude (cartões de crédito, cartéis)
    - AI (Siri, carros autônomos)
    - mercado financeiro (seleção de ativos)
    - textos (atribuição de autoria, classificação)
- mercado de trabalho (médias salariais, etc)
- outline do curso (tópicos, material didático, avaliação)
- leitura obrigatória:
    - [Machine Learning for the Social Sciences](https://www.youtube.com/watch?v=oqfKz-PP9FU)
    - [We Are All Social Scientists Now: How Big Data, Machine Learning, and Causal Inference Work Together](http://stanford.edu/~jgrimmer/bd_2.pdf)
    - [The End of Theory: The Data Deluge Makes the Scientific Method Obsolete](http://www.wired.com/2008/06/pb-theory/)
- [slides](/assets/teaching/mineracao/slides1.pdf)

<strong>2. regressão linear</strong>

- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 61-109
- leitura opcional:
    - [Basic Econometrics](http://www.amazon.com/Basic-Econometrics-Damodar-Gujarati/dp/0073375772/ref=sr_1_1?ie=UTF8&qid=1448210562&sr=8-1&keywords=basic+econometrics), pp. 13-96
    - [Estatística Básica](http://www.livrariacultura.com.br/p/estatistica-basica-61737525), pp. 454-503
    - [Basic Econometrics](http://www.amazon.com/Basic-Econometrics-Damodar-Gujarati/dp/0073375772/ref=sr_1_1?ie=UTF8&qid=1448210562&sr=8-1&keywords=basic+econometrics), pp. 188-232
    - [Forecasting U.S. House Elections](http://www.jstor.org/stable/439492) (sem acesso ao JSTOR? [Sci-Hub](http://www.sci-hub.bz))
- [slides](/assets/teaching/mineracao/slides4.pdf) (regressão linear simples)
- [slides](/assets/teaching/mineracao/slides5.pdf) (regressão linear múltipla)
- [dataset](/assets/teaching/mineracao/aula5dataset.csv) usado na aula

<strong>3. introdução à programação</strong>

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
- [slides](/assets/teaching/mineracao/slides2.pdf)

<strong>4. pré-processamento</strong>

- pandas
- problemas comuns:
    - int/float como str
    - formatos inconsistentes
    - missing data
    - etc
- leitura obrigatória:
    - [The Quartz guide to bad data](https://github.com/Quartz/bad-data-guide)
- datasets usados na aula:
    - [municipios.csv](/assets/teaching/mineracao/municipios.csv)
    - [municipios2.csv](/assets/teaching/mineracao/municipios2.csv)
- [slides](/assets/teaching/mineracao/slides3.pdf)

<strong>5. discussão dos projetos (primeira rodada)</strong>

- alunos apresentam suas idéias p/ trabalho final

<strong>6. árvores de decisão & validação</strong>

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
- [slides](/assets/teaching/mineracao/slides6.pdf)

<strong>7. árvores de decisão & validação II</strong>

- [matematica.csv](/assets/teaching/mineracao/matematica.csv)
- [matematica.py](/assets/teaching/mineracao/matematica.py)
- [condicional.csv](/assets/teaching/mineracao/condicional.csv)
- [condicional.py](/assets/teaching/mineracao/condicional.py)

<strong>8. máquinas de suporte vetorial & parameter tuning & seleção de modelos</strong>

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
- [slides](/assets/teaching/mineracao/slides7.pdf)
- [matematica_svm.py](/assets/teaching/mineracao/matematica.py)
- [condicional_svm.py](/assets/teaching/mineracao/condicional.py)

<strong>9. clusterização</strong>

- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 385-390
    - [Introduction to Data Mining](http://www-users.cs.umn.edu/~kumar/dmbook/ch8.pdf), pp. 487-568
- leitura opcional:
    - [Classificando regimes políticos utilizando análise de conglomerados](http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-62762012000100006)
    - [Financiamento de campanha e apoio parlamentar à Agenda Legislativa da Indústria na Câmara dos Deputados](http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-62762015000100033)
- [slides](/assets/teaching/mineracao/slides9.pdf)
- [clustering.py](/assets/teaching/mineracao/clustering.py)
- [municipios_clustering.csv](/assets/teaching/mineracao/municipios_clustering.csv)

<strong>10. discussão dos projetos (segunda rodada)</strong>

- alunos apresentam suas idéias p/ trabalho final

<strong>11. mineração de textos</strong>

- bag of words
- matriz de termos-freqüências
- normalização
- TF-IDF
- pré-processamento
- leitura obrigatória:
    - [Introduction to Information Retrieval](http://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf), pp. 109-133
    - [Text as Data: The Promise and Pitfalls of Automatic Content
Analysis Methods for Political Texts](http://web.stanford.edu/~jgrimmer/tad2.pdf)
- [slides](/assets/teaching/mineracao/slides10.pdf)

<strong>12. raspagem de sites</strong>

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
- [raspa_vagalume.py](/assets/teaching/mineracao/raspa_vagalume.py)
- [raspa_twitter.py](/assets/teaching/mineracao/raspa_twitter.py)
- [raspa_scielo.py](/assets/teaching/mineracao/raspa_scielo.py)
- [raspa_scielo_2.py](/assets/teaching/mineracao/raspa_scielo_2.py)
- [regex.py](/assets/teaching/mineracao/regex.py)

<strong>13. computação em nuvem</strong>

- supercomputadores de universidade vs AWS, GCP, etc
- Amazon Web Services
    - EC2, S3
- SSH e PuTTY
- comandos Linux básicos
    - ls, cd, mkdir, rm, cp, mv, less, cat, nano, clear, echo, etc
- comandos Linux p/ processamento de texto
    - grep, awk, sed
- shell scripts (#!/bin/bash)
- variáveis de ambiente
- sudo
- chmod
- ./configure, make, make install

<strong>14. redução de dimensionalidade & extração de tópicos</strong>

- LSA
- LDA
- leitura opcional:
    - [Introduction to Information Retrieval](http://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf), pp. 403-417
    - [Latent Dirichlet Allocation](http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)
    - [aula de LDA com um dos criadores do modelo](https://www.youtube.com/watch?v=DDq3OVp9dNA)
    - [Online Learning for Latent Dirichlet Allocation](https://www.cs.princeton.edu/~blei/papers/HoffmanBleiBach2010b.pdf)
- [slides](/assets/teaching/mineracao/slides11.pdf)

<strong>15. discussão dos projetos (terceira rodada)</strong>

- alunos apresentam suas idéias p/ trabalho final

<strong>16. SQL</strong>

- bases relacionais
- chaves primárias
- SELECT
- WHERE
- ORDER BY
- COUNT, SUM, etc
- LIKE
- NOT
- IN
- CASE
- GROUP BY
- JOIN
- subqueries
- wildcards
- interfaces (pyODBC, RODBC, etc)
- leitura obrigatória:
    - [tutorial SELECT](https://technet.microsoft.com/en-us/library/bb264565(v=sql.90).aspx)
    - [tutorial GROUP BY](http://www.w3schools.com/sql/sql_groupby.asp)
    - [tutorial JOIN](https://technet.microsoft.com/en-us/library/ms191517(v=sql.105).aspx)
- leitura opcional:
    - [SQL in 10 Minutes](http://www.amazon.com/Sams-Teach-Yourself-SQL-Minutes-ebook/dp/B009XDGF2C/ref=mt_kindle?_encoding=UTF8&me=), pp. 5-144

<strong>17. "appificando" seu modelo</strong>

- como transformar um trabalho estático (paper, dissertação, etc) num trabalho dinâmico (aplicativo, visualização, interativa, etc)
- Google App Engine
- Plotly
- Shiny