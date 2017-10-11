import pandas as pd
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import cross_val_score

# origem do dataset
# https://github.com/TarekDib03/Analytics/blob/master/Week3%20-%20Logistic%20Regression/Data/parole.csv

# Windows (notem barra nao-invertida)
#file_path = 'C:/Users/thiago.marzagao/Dropbox/dataScience/UnB-ADM/aula6/condicional.csv'

# OS X
file_path = '/Users/thiagomarzagao/Dropbox/dataScience/UnB-ADM/aula6/condicional.csv'

# carrega arquivo
# notem separador = ';' (default eh ',')
data = pd.read_csv(file_path, sep = ';')

# separa variaveis categoricas
categoricals = data[['estado',
                     'crime']]

# transforma variaveis categoricas em dummies
# scikit-learn nao lida com variaveis categoricas nativamente
# (nao eh preciso fazer isso no R)
# cuidado: isso gera dummies desnecessarias; ok aqui, mas nao com regressao
categoricals = pd.get_dummies(categoricals)

# separa variaveis quantitativas (e variaveis jah dummificadas)
numericals = data[['genero',
                   'raca',
                   'idade',
                   'mesespreso',
                   'sentencamaxima',
                   'multiploscrimes']]

# concatena dummies e variaveis quantitativas
x = pd.concat([categoricals, numericals], axis = 1)

# separa variavel-resposta
y = data['violou']

# embaralha as amostras
# notem que a ordem das amostras no dataset nao eh aleatoria
x, y = shuffle(x, y)

# inicializa o classificador
clf1 = SVC(C = 1.0)
# treina o classificador
clf1.fit(x[:450], y[:450])
# mede a acuracia do classificador
accuracy1 = clf1.score(x[450:], y[450:])
# observa a matriz de confusao
yhat1 = clf1.predict(x[450:])
cm1 = confusion_matrix(y[450:], yhat1)

# repete, mas c/ alteracoes

clf2 = SVC(C = 0.1)
clf2.fit(x[:450], y[:450])
accuracy2 = clf2.score(x[450:], y[450:])

clf3 = SVC(C = 10.0)
clf3.fit(x[:450], y[:450])
accuracy3 = clf3.score(x[450:], y[450:])

clf4 = SVC(C = 1.0)
clf4.fit(numericals[:450], y[:450])
accuracy4 = clf4.score(numericals[450:], y[450:])

clf5 = SVC(C = 1.0)
accuracies1 = cross_val_score(clf5, x, y, cv = 10)
avg_accuracies1 = sum(accuracies1) / len(accuracies1)

clf7 = SVC(C = 0.1)
accuracies2 = cross_val_score(clf7, x, y, cv = 10)
avg_accuracies2 = sum(accuracies2) / len(accuracies2)

clf8 = SVC(C = 10.0)
accuracies3 = cross_val_score(clf8, x, y, cv = 10)
avg_accuracies3 = sum(accuracies3) / len(accuracies3)
clf8.fit(x[:450], y[:450])
yhat8 = clf8.predict(x[450:])
cm8 = confusion_matrix(y[450:], yhat8)

# acuracia aqui nao eh uma boa metrica:
# +/-90% de 0s, poucos 1s; chutar tudo "0" dah acuracia grande
# eh preciso observar a matriz de confusao
# e checar o % de acertos p/ 1s

# ha alternativas p/ quando as classes nao sao balanceadas:
# 1) bootstrapping/oversampling
# 2) aumentar o custo de classificar erroneamente a classe rara
# cf. http://statistics.berkeley.edu/sites/default/files/tech-reports/666.pdf

print("matriz de confusao do modelo 1:")
print(cm1)
print("matriz de confusao do modelo 8:")
print(cm8)

# dilema: um modelo preve 1s melhor, outro modelo preve 0s melhor
# trade off: eh pior conceder a condicional a alguem que vai viola-la ou negar a condicional a alguem que nao vai viola-la?
# algoritmo nenhum tem a resposta p/ isso

# outro dilema: convem usar raca e genero como preditores?
# debate em curso nos EUA