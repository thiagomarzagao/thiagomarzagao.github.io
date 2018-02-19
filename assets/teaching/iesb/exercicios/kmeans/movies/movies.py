import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# fonte dos dados: https://www.kaggle.com/rounakbanik/the-movies-dataset

# carrega todos os ratings
ratings = pd.read_csv(
    'ratings.csv',
    usecols = [
        'userId', 
        'movieId', 
        'rating'
    ]
)

# deixa apenas 25 filmes c/ mais avaliacoes
# (do contrario ha muitos missing values)
top_movies = list(ratings['movieId'].value_counts().index[:25])
ratings = ratings[ratings['movieId'].isin(top_movies)]

# transforma long -> wide
ratings = ratings.pivot_table(
    index = 'userId', # variavel que queremos como linhas
    columns = 'movieId', # variavel que queremos como colunas
    values = 'rating' # variavel que queremos como valores
)

# deixa apenas quem avaliou todos os 25 filmes
ratings = ratings.dropna()
X = ratings.as_matrix()

# poe tudo entre 0 1
# (aqui funciona melhor que normalizacao)
scaler = MinMaxScaler()
X = scaler.fit_transform(X)
#X = normalize(X)

# extrai qtde de categorias (comedia, acao, romance, etc)
movies = pd.read_csv('movies.csv')
overlap = movies[movies['movieId'].isin(top_movies)]
l = [e.split('|') for e in overlap['genres']]
genre_set = set([item for sublist in l for item in sublist])
num_genres = len(genre_set)

# inicializa clusterizador
kmeans = KMeans(
    n_clusters = 2, # tentar num_genres, 100, 2
    n_init = 15, 
    max_iter = 450, 
    init = 'k-means++'
)

# clusteriza
kmeans.fit(X)

# inspeciona clusters
ratings['cluster'] = kmeans.labels_ # adiciona coluna c/ cluster
grouped = ratings.groupby('cluster')
clusters = {}
for group in grouped:
    cluster = group[0]
    df = group[1]
    del df['cluster']
    means = df.mean(axis = 0)
    sorted_means = means.sort_values(0, ascending = False)
    top_rated = []
    for e in sorted_means[:10].iteritems():
        title = movies[movies['movieId'] == e[0]]['title'].values[0]
        rating = round(e[1], 2)
        top_rated.append((rating, title))
    clusters[cluster] = top_rated
for key in clusters:
    print(' ')
    print(key)
    for tup in clusters[key]:
        print(tup[0], tup[1])

# checa silhuetas
silhouette_avg = silhouette_score(X, kmeans.labels_)
print('silhueta media:', silhouette_avg)