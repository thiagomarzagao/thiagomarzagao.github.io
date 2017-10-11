import pandas as pd
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import cross_val_score

# comeca-se o script importando os pacotes necessarios

# origem da base
# https://archive.ics.uci.edu/ml/datasets/Student+Performance

# caminho ate o arquivo

# Windows (notem barra nao-invertida)
#file_path = 'C:/Users/thiago.marzagao/Dropbox/dataScience/UnB-ADM/aula6/matematica.csv'

# OS X
file_path = '/Users/thiagomarzagao/Dropbox/dataScience/UnB-ADM/aula6/matematica.csv'

# carrega arquivo
# notem separador = ';' (default eh ',')
data = pd.read_csv(file_path, sep = ';')

# separa variaveis categoricas
categoricals = data[['escola',
                     'genero',
                     'rural',
                     'tamfamilia',
                     'paisjuntos',
                     'trabmae',
                     'trabpai',
                     'escolha',
                     'guarda',
                     'ajudaextra',
                     'suportefam',
                     'aulaparticular',
                     'extracurricular',
                     'enfermagem',
                     'querfaculdade',
                     'internet',
                     'relacionamento']]

# transforma variaveis categoricas em dummies
# scikit-learn nao lida com variaveis categoricas nativamente
# (nao eh preciso fazer isso no R)
# cuidado: isso gera dummies desnecessarias; ok aqui, mas nao com regressao
categoricals = pd.get_dummies(categoricals)

# separa variaveis quantitativas
numericals = data[['idade',
                   'educmae',
                   'educpai',
                   'distancia',
                   'horasestudo',
                   'reprovacoes',
                   'qualfamilia',
                   'tempolivre',
                   'sai',
                   'alcoolsem',
                   'alcoolfds',
                   'saude',
                   'ausencias']]

# concatena dummies e variaveis quantitativas
x = pd.concat([categoricals, numericals], axis = 1)

# separa variavel-resposta
y = data['aprovacao']

# embaralha as amostras
# notem que a ordem das amostras no data nao eh aleatoria
x, y = shuffle(x, y)

# inicializa o classificador
clf1 = SVC(C = 1.0)
# treina o classificador
clf1.fit(x[:300], y[:300])
# mede a acuracia do classificador
accuracy1 = clf1.score(x[300:], y[300:])
# observa a matriz de confusao
yhat = clf1.predict(x[300:])
cm = confusion_matrix(y[300:], yhat)

# repete, mas c/ alteracoes

clf2 = SVC(C = 0.1)
clf2.fit(x[:300], y[:300])
accuracy2 = clf2.score(x[300:], y[300:])

clf3 = SVC(C = 10.0)
clf3.fit(x[:300], y[:300])
accuracy3 = clf3.score(x[300:], y[300:])

clf4 = SVC(C = 1.0)
clf4.fit(numericals[:300], y[:300])
accuracy4 = clf4.score(numericals[300:], y[300:])

clf5 = SVC(C = 1.0)
accuracies1 = cross_val_score(clf5, x, y, cv = 10)
avg_accuracies1 = sum(accuracies1) / len(accuracies1)

clf7 = SVC(C = 0.1)
accuracies2 = cross_val_score(clf7, x, y, cv = 10)
avg_accuracies2 = sum(accuracies2) / len(accuracies2)

clf8 = SVC(C = 10.0)
accuracies3 = cross_val_score(clf8, x, y, cv = 10)
avg_accuracies3 = sum(accuracies3) / len(accuracies3)