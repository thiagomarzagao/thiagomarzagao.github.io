---
layout: page
permalink: teaching/mineracao1.md
---

<strong>
MINERAÇÃO DE DADOS - 1/2016 - ADM/UnB
</strong>

Objetivo da disciplina:

- Ao final do curso o aluno deverá ser capaz de usar corretamente algumas das principais ferramentas de mineração de dados: regressão, classificação e clusterização; computação em nuvem; Python; SQL.

Site da disciplina:

- thiagomarzagao.com/teaching/mineracao1
- Todo o material obrigatório da disciplina estará disponível no site (incluindo slides, tarefas e datasets).

Avaliação:

- 8 tarefas de 8,75 pontos cada.
- 5 tarefas de 6,00 pontos cada.

Plano de aulas:

#1 motivação: para que serve mineração de dados?

- aplicações
    - recommender systems (Amazon, Netflix, Match.com)
    - detecção de fraude (cartões de crédito, cartéis)
    - AI (Siri, carros autônomos)
    - mercado financeiro (seleção de ativos)
    - textos (atribuição de autoria, classificação)
- mercado de trabalho (médias salariais, etc)
- outline do curso (tópicos, material didático, avaliação)

#2: regressão linear simples

- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 61-71
- leitura opcional:
    - [Basic Econometrics](http://www.amazon.com/Basic-Econometrics-Damodar-Gujarati/dp/0073375772/ref=sr_1_1?ie=UTF8&qid=1448210562&sr=8-1&keywords=basic+econometrics), pp. 13-96
    - [Estatística Básica](http://www.livrariacultura.com.br/p/estatistica-basica-61737525), pp. 454-503
- tarefa (6,00 pontos)

#3: introdução à programação (laboratório)

- Python
- tipos de dados (str, int, float, etc)
- condicionais (IF/ELSE)
- operadores (AND/OR/NOT)
- FOR loops
- estruturas de dados (listas, conjuntos, dicionários)
- pacotes, classes, funções
- REPL vs scripts
- I/O
- regressão linear simples em Python
- leitura opcional:
    - [Automating the Boring Stuff with Python](http://www.amazon.com/Automate-Boring-Stuff-Python-Programming/dp/1593275994/ref=sr_1_2?ie=UTF8&qid=1448215811&sr=8-2&keywords=python), pp. 11-144
- tarefa (8,75 pontos)

#4 - regressão linear múltipla

- regularização
- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 71-109
- leitura opcional:
    - [Basic Econometrics](http://www.amazon.com/Basic-Econometrics-Damodar-Gujarati/dp/0073375772/ref=sr_1_1?ie=UTF8&qid=1448210562&sr=8-1&keywords=basic+econometrics), pp. 188-232
- tarefa (8,75 pontos)

#5 - árvores de decisão

- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 303-316
- tarefa (8,75 pontos)

#6 - árvores de decisão: bagging e boosting

- random forest
- AdaBoost
- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 316-323
- tarefa (8,75 pontos)

#7 - máquinas de suporte vetorial: soft margin

- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 337-350
- tarefa (8,75 pontos)

#8 - máquinas de suporte vetorial: kernel trick

- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 350-356
- tarefa (8,75 pontos)

#9 - clusterização: K-means

- leitura obrigatória:
    - [Introduction to Statistical Learning](http://www-bcf.usc.edu/~gareth/ISL/ISLR%20Sixth%20Printing.pdf), pp. 385-390
- tarefa (8,75 pontos)

#10 - mineração de textos

- o problema da dimensionalidade
- bag of words
- TF-IDF
- similaridade do co-seno
- classificação
    - árvores de decisão
    - SVM
    - clusterização
- leitura obrigatória:
    - [Introduction to Information Retrieval](http://nlp.stanford.edu/IR-book/pdf/irbookonlinereading.pdf), pp. 109-133
- tarefa (8,75 pontos)

#11 - raspagem de sites (laboratório)

- APIs
    - ex.: Twitter
- requests
- Selenium
- BeautifulSoup
- expressões regulares
- leitura obrigatória:
    - webscraping with Selenium (partes [1](http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/), [2](http://thiagomarzagao.com/2013/11/14/webscraping-with-selenium-part-2/), [3](http://thiagomarzagao.com/2013/11/15/webscraping-with-selenium-part-3/), [4](http://thiagomarzagao.com/2013/11/16/webscraping-with-selenium-part-4/) e [5](http://thiagomarzagao.com/2013/11/17/webscraping-with-selenium-part-5/))
- tarefa (6,00 pontos)

#12 - SQL

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
- tarefa (6,00 pontos)

#12 - trabalhando c/ dados sujos (laboratório)

- acentuação e caracteres especiais
    - encoding
- números como texto e vice-versa
    - trailing zeroes, etc
- separador de campos
- convertendo formatos de arquivo
- missing data
- NULL
- datas
- tarefa (6,00 pontos)

#14 - computação em nuvem (laboratório)

- Amazon Web Services
- SSH
- comandos básicos do Linux
- tarefa (6,00 pontos)