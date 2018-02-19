import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_samples
from sklearn.metrics import silhouette_score

# carrega os dados
data = pd.read_csv('winequality-red.csv')
# fonte: https://www.kaggle.com/uciml/red-wine-quality-cortez-et-al-2009

# normaliza X
#X = normalize(data.as_matrix())
X = data.as_matrix()

# inicializa clusterizador
dbscan = DBSCAN(
    eps = 0.5, # variar
    min_samples = 2 # variar
)

# clusteriza
dbscan.fit(X)

# checa "-1"
data['cluster'] = dbscan.labels_ # adiciona coluna c/ cluster

# checa silhuetas
silhouettes = silhouette_samples(X, dbscan.labels_)
data['sil'] = silhouettes

# checa silhueta media (clusterizacao ficou boa?)
silhouette_avg = silhouette_score(X, dbscan.labels_)