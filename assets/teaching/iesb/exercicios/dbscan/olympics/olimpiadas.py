import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

# fonte dos dados: https://www.kaggle.com/the-guardian/olympic-games

# carrega dados
olimp = pd.read_csv(
    'summer.csv',
    usecols = [
        'Sport',
        'Country',
    ]
)

# adiciona coluna de 1s
olimp['1'] = 1

# pivota tabela somando os 1s
olimp = olimp.pivot_table(
    index = 'Country', 
    columns = 'Sport', 
    aggfunc = 'sum',
    fill_value = 0
)

# "achata" DataFrame multi-indice
cols = [e[1] for e in olimp.columns]
rows = list(olimp.index)
olimp = pd.DataFrame(olimp.as_matrix())
olimp.columns = cols

# prepara dados
X = olimp.as_matrix()

# inicializa clusterizador
dbscan = DBSCAN(
    eps = 0.5, # variar
    min_samples = 5 # variar
)

# clusteriza
dbscan.fit(X)

# checa silhuetas
olimp['cluster'] = dbscan.labels_
olimp['country'] = rows
for k in set(dbscan.labels_):
    print(olimp[olimp['cluster'] == k])
silhouette_avg = silhouette_score(X, dbscan.labels_)
print('silhueta media:', silhouette_avg)