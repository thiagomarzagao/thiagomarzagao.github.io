import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# fonte dos dados: https://www.kaggle.com/marlesson/news-of-the-site-folhauol/data

# carrega e limpa artigos
noticias = pd.read_csv('articles.csv', usecols = ['text'], nrows = 1000)
noticias = [e for e in noticias['text'] if isinstance(e, str)]
noticias = pd.DataFrame(noticias)

# vetoriza
vectorizer = TfidfVectorizer() # variar parametros (L1/L2, etc)
X = vectorizer.fit_transform(noticias[0])
X = normalize(X)

# clusteriza
# inicializa clusterizador
kmeans = KMeans(
    n_clusters = 3, # variar
    n_init = 15, 
    max_iter = 450, 
    init = 'k-means++'
)

kmeans.fit(X)

# inspeciona clusters
noticias['cluster'] = kmeans.labels_ # adiciona coluna c/ cluster

# mede similaridade do co-seno
text = ['Kim Jong-un diz estar aberto a se reunir com presidente da Coreia do Sul,"O líder norte-coreano, Kim Jong-un, disse nesta quinta-feira em seu discurso de Ano Novo emitido pela televisão estatal KCTV que ""não há razão para não manter conversas"" com a presidente da vizinha Coreia do Sul, Park Geun-hye, sempre que o clima diplomático seja propício.  ""Dependendo dos ânimos e das circunstâncias que se criem, não há razão para não manter conversas do mais alto nível"", explicou o líder do regime comunista.  Kim ressaltou a necessidade de um ""grande mudança"" nas relações Norte-Sul, e disse que Pyongyang fará ""todos os esforços possíveis"" para melhorar o diálogo e a cooperação com Seul.  O líder norte-coreano também disse que estes encontros de alto nível, assim como negociações de outro tipo, poderão ser retomadas sempre que a Coreia do Sul queira melhorar os laços bilaterais através do diálogo.  Esta mesma semana, um comitê para a reunificação do Sul propôs um encontro entre ministros das duas Coreias em Janeiro para aproximar posturas.  A Coreia do Sul espera progressos significativos em sua relação com o Norte no recém iniciado 2015, ano no qual se completa o 70º aniversário do fim do domínio colonial (1910-1945) do Japão sobre a península coreana.  As duas Coreias continuam tecnicamente em guerra já que o conflito que as colocou em confronto entre 1950 e 1953 se encerrou com um cessar-fogo em vez de um tratado de paz.']
X_new = vectorizer.transform(text)
noticias['coseno'] = cosine_similarity(X_new, X)[0]
print(noticias.sort_values(by = 'coseno'))