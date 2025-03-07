import numpy as np
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import normalize
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

# fontes dos dados: IBGE, DATASUS, INEP

# carrega todos os municipios
municipios = pd.read_csv('municipios.csv')
del municipios['pop2016']
del municipios['despesa2016']
del municipios['transf2016']

# separar codigo, municipio e uf do resto
X = municipios[[
    'govpop2015',
    'mortalidade2015',
    'tx_homicidios2015',
    'enem_media2015',
    'enem_desvpad2015',
    'ideb_i2015',
    'ideb_f2015'
]]

# imputa dados faltantes
imputer = Imputer(
    missing_values = 'NaN',
    strategy = 'median',
    axis = 0
)
for col in X.columns:
    X[col] = imputer.fit_transform(X[col].values.reshape(-1, 1))

# normaliza X
X = normalize(X.as_matrix())

# inicializa clusterizador
dbscan = DBSCAN(
    eps = 0.5, # variar
    min_samples = 5 # variar
)

# clusteriza
dbscan.fit(X)

# inspeciona clusters
municipios['cluster'] = dbscan.labels_ # adiciona coluna c/ cluster
grouped = municipios.groupby('cluster')
stacked = pd.DataFrame()
for group in grouped:
    means = group[1].mean(axis = 0)
    del means['cod_ibge']
    del means['cluster']
    stacked[group[0]] = means
print(stacked)

# checa silhuetas
silhouette_avg = silhouette_score(X, dbscan.labels_)
print('silhueta media:', silhouette_avg)