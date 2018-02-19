import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.utils import shuffle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# carrega os dados
X = pd.read_csv('Melbourne_housing_FULL.csv')
# fonte: https://www.kaggle.com/anthonypino/melbourne-housing-market

# remove algumas colunas
del X['Address']
del X['Method']
del X['SellerG']
del X['CouncilArea']
del X['Lattitude']
del X['Longtitude']
del X['Regionname']
del X['Propertycount']
del X['Postcode']

# dummifica variaveis categoricas
suburb = pd.get_dummies(X['Suburb'])
del X['Suburb']
category = pd.get_dummies(X['Type'])
del X['Type']
X = pd.concat((X, suburb, category), axis = 1)

# "conserta" campo data (deixa apenas ano)
X['Date'] = X['Date'].map(lambda x: int(x[-4:]))

# imputa dados faltantes
quant = [
    'Rooms',
    'Price',
    'Date',
    'Distance',
    'Bedroom2',
    'Bathroom',
    'Car',
    'Landsize',
    'BuildingArea',
    'YearBuilt']
imputer_quant = Imputer(
    missing_values = 'NaN',
    strategy = 'median',
    axis = 0
)
imputer_qual = Imputer(
    missing_values = 'NaN',
    strategy = 'most_frequent',
    axis = 0
)
for col in X.columns:
    if col in quant:
        X[col] = imputer_quant.fit_transform(X[col].values.reshape(-1, 1))
    else:
        X[col] = imputer_qual.fit_transform(X[col].values.reshape(-1, 1))

# separa o Y
Y = X['Price']
del X['Price']

# embaralha as amostras
X, Y = shuffle(X, Y)

# separa dados de treinamento e de teste
cutoff = 20000
X_train = X[:cutoff]
X_test = X[cutoff:]
Y_train = Y[:cutoff]
Y_test = Y[cutoff:]

# estima coeficientes
clf = LinearRegression()
clf.fit(X_train, Y_train)

# gera previsoes
Y_hat = clf.predict(X_test)

# identifica anomalias (maiores erros)
X_test['error'] = (Y_test - Y_hat)
print(X_test.sort_values(by = 'error'))

# avalia desepenho do modelo
print('R-squared:', r2_score(Y_test, Y_hat))