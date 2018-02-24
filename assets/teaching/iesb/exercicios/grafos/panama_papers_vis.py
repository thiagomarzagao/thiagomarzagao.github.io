import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

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

# extrai subgrafo
subgraph = nx.ego_graph(G, 12179009, radius = 1, undirected = True)

# visualiza
pos = nx.kamada_kawai_layout(subgraph) # define o layout (variar!) e extrai a posicao de cada no
plt.figure(1, figsize = (24, 24)) # define o tamanho da imagem
nx.draw(
    subgraph, 
    pos, 
    node_size = 1800, 
    node_color = 'orange', 
    edge_color = 'grey', 
    with_labels = True, 
    font_size = 18
    )
plt.show()