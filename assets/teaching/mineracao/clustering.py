import pandas as pd
from sklearn.cluster import KMeans
from sklearn.utils import shuffle

# carrega dataset
fulldata = pd.read_csv('municipios_clustering.csv')

# mantem apenas variaveis quantitativas
data = fulldata[['latitude', 
                 'longitude', 
                 'bolsapibcap', 
                 'rural', 
                 'analfabetismo', 
                 'saneamentoruim']]

# inicializa classificador
kmeans = KMeans(n_clusters = 27,
                max_iter = 450, 
                n_init = 15, 
                init = 'random')

# clusteriza
kmeans.fit(data)

# inspeciona clusters (correspondem a UFs?)
fulldata['cluster'] = kmeans.labels_
fulldata = shuffle(fulldata)
print fulldata[['uf', 'cluster']]

# SP
print fulldata['cluster'][fulldata['uf'] == 'SP']
print set(fulldata['cluster'][fulldata['uf'] == 'SP'])

# MG
print fulldata['cluster'][fulldata['uf'] == 'MG']
print set(fulldata['cluster'][fulldata['uf'] == 'MG'])