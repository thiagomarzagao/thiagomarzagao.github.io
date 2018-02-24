import pandas as pd
import networkx as nx
from datetime import datetime
from networkx.algorithms.distance_measures import diameter
from networkx.algorithms import degree_centrality, closeness_centrality, betweenness_centrality, pagerank, clustering, average_clustering
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# fonte: https://offshoreleaks.icij.org/pages/database (ZIP file)

# carrega nos do tipo 'endereco'
addresses = pd.read_csv('csv_panama_papers/panama_papers.nodes.address.csv',
    usecols = [
        'node_id',
        'address'
        ]
    )

# carrega nos do tipo 'entidade'
entities = pd.read_csv('csv_panama_papers/panama_papers.nodes.entity.csv', 
    usecols = [
        'node_id',
        'name'
        ]
    )

# carrega nos do tipo 'intermediario'
intermediaries = pd.read_csv('csv_panama_papers/panama_papers.nodes.intermediary.csv',
    usecols = [
        'node_id',
        'name'
        ]
    )

# carrega nos do tipo 'executivo'
officers = pd.read_csv('csv_panama_papers/panama_papers.nodes.officer.csv',
    usecols = [
        'node_id',
        'name'
        ]
    )

# carrega links
edges = pd.read_csv('csv_panama_papers/panama_papers.edges.csv', 
    usecols = [
        'START_ID',
        'link',
        'END_ID',
        'end_date'
        ]
    )
edges['status'] = edges['end_date'].map(lambda x: 'inactive' if isinstance(x, str) else 'active')
del edges['end_date']

# cria grafo
G = nx.DiGraph()
for n, row in addresses.iterrows():
    G.add_node(row.node_id, node_type = 'address', details = row.to_dict())
for n, row in entities.iterrows():
    G.add_node(row.node_id, node_type = 'entity', details = row.to_dict())
for n, row in intermediaries.iterrows():
    G.add_node(row.node_id, node_type = 'intermediary', details = row.to_dict())
for n, row in officers.iterrows():
    G.add_node(row.node_id, node_type = 'officer', details = row.to_dict())
for n, row in edges.iterrows():
    G.add_edge(row.START_ID, row.END_ID, rel_type = row.link)

# inspeciona
G.number_of_nodes()
G.number_of_edges()

# 5 nos mais centrais de acordo c/ diferentes metricas
# demora um bocado!
rank_grau = sorted([(round(value, 5), key) for (key, value) in degree_centrality(G).items()])[::-1]
rank_prox = sorted([(round(value, 5), key) for (key, value) in closeness_centrality(G).items()])[::-1]
rank_intr = sorted([(round(value, 5), key) for (key, value) in betweenness_centrality(G).items()])[::-1]
rank_page = sorted([(round(value, 5), key) for (key, value) in pagerank(G).items()])[::-1]

# calcula nos c/ maiores coeficientes de clusterizacao
coeffs = clustering(G)

# calcula coeficiente de clusterizacao medio do grafo
avg_cluster = average_clustering(G)

# calcula diametro do grafo
diameter = diameter(G)

# inspeciona nos especificos
id_no = rank_grau[4][1]
G.in_degree(id_no)
G.out_degree(id_no)
G.node[id_no]
G[id_no]

# calcula distancia minima entre dois nos
# nem sempre existe! e frequentemente demora uma enormidade
nx.shortest_path(G, source = rank_grau[4][1],target = rank_grau[3][1])