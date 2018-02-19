import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

noticias = pd.read_csv('articles.csv', usecols = ['text'], nrows = 1000)
noticias = [e for e in noticias['text'] if isinstance(e, str)]
noticias = pd.DataFrame(noticias)

# vetoriza
vectorizer = TfidfVectorizer() # variar parametros (L1/L2, etc)
X = vectorizer.fit_transform(noticias[0])

# LSA
lda = LatentDirichletAllocation(n_components = 10)
X_reduced = lda.fit_transform(X)

# clusteriza c/ k-means
kmeans = KMeans(
    n_clusters = 3, # variar
    n_init = 15, 
    max_iter = 450, 
    init = 'k-means++'
)
kmeans.fit(X_reduced)

# vetoriza de novo (mas c/ CountVectorizer)
vectorizer = CountVectorizer() # variar parametros (L1/L2, etc)
X = vectorizer.fit_transform(noticias[0])

# clusteriza c/ DBSCAN
dbscan = DBSCAN(
    eps = 0.5, # variar
    min_samples = 5 # variar
)
dbscan.fit(X_reduced)

# inspeciona clusters
noticias['kmeans'] = kmeans.labels_ # adiciona coluna c/ clusters k-means
noticias['dbscan'] = dbscan.labels_ # adiciona coluna c/ clusters DBSCAN