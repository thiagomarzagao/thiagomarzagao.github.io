---
layout: page
title: iesb1
mostra: nao
---

<strong>
DATA MINING E MACHINE LEARNING I - 1/2018 - IESB
</strong>

(Última atualização: 19/02/2018)

**Objetivo da disciplina**:

- Ao final do curso o aluno deverá ser capaz de usar corretamente as seguintes ferramentas: clusterização, detecção de anomalias, raspagem de sites, mineração de textos, análise de redes sociais.

**Pré-requisitos**:

- Não há pré-requisitos. Algum conhecimento de estatística básica e de cálculo pode ser útil mas não é necessário nem esperado.

**Dia, horário e local**:

- Terças, das 19:00 às 22:30. Local a designar.

**Comunicação**:

- A comunicação com o professor e com os demais alunos será por meio de time no Slack: [https://iesb-dados.slack.com/](https://iesb-dados.slack.com/) Você pode se juntar ao time informando seu email ao professor.
- Uma vez no time você pode postar dúvidas, respostas, pedaços de código, etc, no canal #general, que é visível a todos os participantes. Também é possível enviar mensagens privadas dentro do time.
- Não use o time p/ postagem de piadas, correntes, etc.
- O Slack é o único canal de comunicação com o professor. Emails provavelmente serão ignorados.

**Avaliação**:

- Trabalho final (peso: 50%).
    - O trabalho deverá consistir na aplicação de uma ou mais técnicas aprendidas no curso a problema concreto de interesse do aluno. O problema deverá ser previamente discutido com e aprovado pelo professor.
    - O trabalho é individual. 
    - O trabalho será avaliado com base: i) na adequação do(s) método(s) empregados(s) ao problema; ii) no uso e interpretação corretos do(s) método(s); iii) na clareza e precisão ao descrever o problema e o(s) método(s) empregado(s).
    - O trabalho final pode ser em português ou em inglês.
    - Cada aluno apresentará seu trabalho final na penúltima aula do curso. Cada aluno deverá também postar o trabalho final no canal #general do time no Slack. Além do trabalho final o aluno deverá postar também os scripts e datasets utilizados. <font color="red">O prazo para postar o trabalho final, scripts e datasets é 23:59 do dia da apresentação. Não serão aceitos trabalhos entregues fora do prazo.</font>
    - Plágio resultará na reprovação do aluno, no encaminhamento do caso às áreas competentes do IESB e na inclusão do nome do aluno no [Cheaters Hall](/teaching/cheaters_hall).
- Prova (peso: 50%).
    - A prova abordará todo o conteúdo visto ao longo do curso.

<strong>Plano de aulas:</strong>

<strong>1. visão geral, revisão de estatística, pré-processamento</strong>

- slides:
    - [visão geral](/assets/teaching/iesb/slides/overview.pdf)
    - [estatística](/assets/teaching/iesb/slides/estatistica.pdf)
    - [pré-processamento](/assets/teaching/iesb/slides/preprocessamento.pdf)
- leituras/vídeos:
    - [Machine Learning for the Social Sciences](https://www.youtube.com/watch?v=oqfKz-PP9FU)
    - [We Are All Social Scientists Now: How Big Data, Machine Learning, and Causal Inference Work Together](http://stanford.edu/~jgrimmer/bd_2.pdf)
    - [The End of Theory: The Data Deluge Makes the Scientific Method Obsolete](http://www.wired.com/2008/06/pb-theory/)
    - [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/), caps. 0-6
    - [The Quartz guide to bad data](https://github.com/Quartz/bad-data-guide)

<strong>2. clusterização I</strong>

- slides:
    - [k-means](/assets/teaching/iesb/slides/kmeans.pdf)
- exercício/filmes:
    - [movies.csv](/assets/teaching/iesb/exercicios/kmeans/movies/movies.csv)
    - [ratings.csv](https://www.kaggle.com/rounakbanik/the-movies-dataset/downloads/ratings.csv)
    - [movies.py](/assets/teaching/iesb/exercicios/kmeans/movies/movies.py)
- exercício/municípios:
    - [municipios.csv](/assets/teaching/iesb/exercicios/kmeans/municipios/municipios.csv)
    - [municipios.py](/assets/teaching/iesb/exercicios/kmeans/municipios/municipios.py)
- exercício/olimpíadas:
    - [summer.csv](/assets/teaching/iesb/exercicios/kmeans/olympics/summer.csv)
    - [olimpiadas.py](/assets/teaching/iesb/exercicios/kmeans/olympics/olimpiadas.py)
- leituras:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 385-390
    - [Introduction to Data Mining](http://www-users.cs.umn.edu/~kumar/dmbook/ch8.pdf), pp. 496-515
    - [Classificando regimes políticos utilizando análise de conglomerados](http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-62762012000100006)
    - [Financiamento de campanha e apoio parlamentar à Agenda Legislativa da Indústria na Câmara dos Deputados](http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-62762015000100033)

<strong>3. clusterização II</strong>

- slides:
    - [DBSCAN](/assets/teaching/iesb/slides/dbscan.pdf)
- exercício/filmes:
    - [movies.csv](/assets/teaching/iesb/exercicios/dbscan/movies/movies.csv)
    - [ratings.csv](https://www.kaggle.com/rounakbanik/the-movies-dataset/downloads/ratings.csv)
    - [movies.py](/assets/teaching/iesb/exercicios/dbscan/movies/movies.py)
- exercício/municípios:
    - [municipios.csv](/assets/teaching/iesb/exercicios/dbscan/municipios/municipios.csv)
    - [municipios.py](/assets/teaching/iesb/exercicios/dbscan/municipios/municipios.py)
- exercício/olimpíadas:
    - [summer.csv](/assets/teaching/iesb/exercicios/dbscan/olympics/summer.csv)
    - [olimpiadas.py](/assets/teaching/iesb/exercicios/dbscan/olympics/olimpiadas.py)
- leituras:
    - [Introduction to Data Mining](http://www-users.cs.umn.edu/~kumar/dmbook/ch8.pdf), pp. 526-532    
    - [A Density-Based Algorithm for Discovering Clusters](https://www.aaai.org/Papers/KDD/1996/KDD96-037.pdf)

<strong>4. detecção de anomalias</strong>

- slides:
    - [detecção de anomalias](/assets/teaching/iesb/slides/anomalias.pdf)
- exercício/Melbourne:
    - [Melbourne_housing_FULL.csv](/assets/teaching/iesb/exercicios/anomalias/Melbourne_housing_FULL.csv)
    - [melbourne.py](/assets/teaching/iesb/exercicios/anomalias/melbourne.py)
- exercício/vinho:
    - [winequality-red.csv](/assets/teaching/iesb/exercicios/anomalias/winequality-red.csv)
    - [wine.py](/assets/teaching/iesb/exercicios/anomalias/wine.py)

<strong>5. trabalho final: discussões</strong>

<strong>6. raspagem de sites</strong>

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
- exercícios:
    - [raspa_vagalume.py](/assets/teaching/iesb/exercicios/raspagem/raspa_vagalume.py)
    - [raspa_twitter.py](/assets/teaching/iesb/exercicios/raspagem/raspa_twitter.py)
    - [raspa_scielo.py](/assets/teaching/iesb/exercicios/raspagem/raspa_scielo.py)
    - [raspa_scielo_2.py](/assets/teaching/iesb/exercicios/raspagem/raspa_scielo_2.py)
    - [regex.py](/assets/teaching/iesb/exercicios/raspagem/regex.py)
- leitura:
    - webscraping with Selenium (partes [1](http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/), [2](http://thiagomarzagao.com/2013/11/14/webscraping-with-selenium-part-2/), [3](http://thiagomarzagao.com/2013/11/15/webscraping-with-selenium-part-3/), [4](http://thiagomarzagao.com/2013/11/16/webscraping-with-selenium-part-4/) e [5](http://thiagomarzagao.com/2013/11/17/webscraping-with-selenium-part-5/))

<strong>7. mineração de textos I</strong>

- slides:
    - [mineração de textos I](/assets/teaching/iesb/slides/textos1.pdf)
- exercício/notícias:
    - [articles.csv](https://www.kaggle.com/marlesson/news-of-the-site-folhauol/downloads/articles.csv)
    - [folha.py](/assets/teaching/iesb/exercicios/textos/folha.py)   
- exercício/tuítes:
    - [tweets.txt](/assets/teaching/iesb/exercicios/textos/tweets.txt)
- leitura:
    - [Introduction to Information Retrieval](http://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf), pp. 109-133
    - [Text as Data: The Promise and Pitfalls of Automatic Content
Analysis Methods for Political Texts](http://web.stanford.edu/~jgrimmer/tad2.pdf)

<strong>8. mineração de textos II</strong>

- slides:
    - [mineração de textos II](/assets/teaching/iesb/slides/textos2.pdf)
- exercício/notícias:
    - [articles.csv](https://www.kaggle.com/marlesson/news-of-the-site-folhauol/downloads/articles.csv)
    - [folha_lsa.py](/assets/teaching/iesb/exercicios/textos/folha_lsa.py)
    - [folha_lda.py](/assets/teaching/iesb/exercicios/textos/folha_lda.py)
- exercício/tuítes:
    - [tweets.txt](/assets/teaching/iesb/exercicios/textos/tweets.txt)
- leituras:
    - [Introduction to Information Retrieval](http://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf), pp. 403-417
    - [Latent Dirichlet Allocation](http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)
    - [aula de LDA com um dos criadores do modelo](https://www.youtube.com/watch?v=DDq3OVp9dNA)

<strong>9. análise de redes I</strong>

<strong>10. análise de redes II</strong>

<strong>11. trabalho final: apresentações</strong>

<strong>12. prova</strong>