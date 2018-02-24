import networkx as nx
import matplotlib.pyplot as plt

n_nodes = 15 # variar
connectivity = 0.725 # variar
G = nx.random_geometric_graph(n_nodes, connectivity) # cria grafo aleatorio
pos = nx.kamada_kawai_layout(G) # define o layout (variar!) e extrai a posicao de cada no
plt.figure(1, figsize = (24, 24)) # define o tamanho da imagem
nx.draw(
    G, 
    pos, 
    node_size = 1800, 
    node_color = 'orange', 
    edge_color = 'grey', 
    with_labels = True, 
    font_size = 18
    )
plt.show()