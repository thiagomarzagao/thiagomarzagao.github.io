import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
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
num_clusters = 3
kmeans = KMeans(
    n_clusters = num_clusters, # testar diferentes valores
    n_init = 150, 
    max_iter = 450, 
    init = 'k-means++'
)

# clusteriza
kmeans.fit(X)

# checa silhuetas
olimp['cluster'] = kmeans.labels_
olimp['country'] = rows
for k in range(num_clusters):
    print(olimp[olimp['cluster'] == k])
silhouette_avg = silhouette_score(X, kmeans.labels_)
print('silhueta media:', silhouette_avg)

# notem:
# 1) EUA sozinho num cluster (anomalia)
# 2) silhueta nem sempre eh um bom indicador de "encaixe"
# 3) matriz eh esparsa! isso frequentemente eh um problema