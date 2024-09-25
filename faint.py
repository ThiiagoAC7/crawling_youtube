import pickle
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

def filter_graph_for_visualization(G, min_degree=1, top_n_nodes=10000, min_edge_weight=1):
    """
    Filter a large graph for visualization.
    
    Params:
    - G: networkx Graph object
    - min_degree: minimum degree for a node to be included
    - top_n_nodes: number of top nodes by degree to include
    - min_edge_weight: minimum weight for an edge to be included
    
    Return:
    - filtered_G: filtered networkx Graph object
    """
    
    # filter nodes by degree
    node_degrees = dict(G.degree())
    high_degree_nodes = [node for node, degree in node_degrees.items() if degree >= min_degree]
    
    # select top N nodes by degree
    top_nodes = sorted(high_degree_nodes, key=lambda x: node_degrees[x], reverse=True)[:top_n_nodes]
    
    subgraph = G.subgraph(top_nodes)
    
    # filter edges by weight
    filtered_G = nx.Graph()
    for u, v, data in subgraph.edges(data=True):
        if data['weight'] >= min_edge_weight:
            filtered_G.add_edge(u, v, **data)
    
    filtered_G.remove_nodes_from(list(nx.isolates(filtered_G)))
    
    print(f"Original graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"Filtered graph: {filtered_G.number_of_nodes()} nodes, {filtered_G.number_of_edges()} edges")
    
    return filtered_G


def load_graph(path, filter=False, threshold=1, n=10000):
    """
    Loads graph saved in pickle format

    Params:
    - path: Path where graph was saved
    - filter: Filter graph to aid in visualization
    - threshold: edge weights thershold value
    - n: top n nodes to show 

    Return:
    - G: graph 
    """
    G = pickle.load(open(path, 'rb'))
    if filter:
        return filter_graph_for_visualization(G, 
                                              # min_degree=threshold, 
                                              top_n_nodes=n,
                                              min_edge_weight=threshold)
    print(f"Graph Nodes: {G.number_of_nodes()}")
    print(f"Graph Edges: {G.number_of_edges()}")
    return G

def calc_clustering_coef(G, threshold, path):
    """
    Calculates clustering coeficcient of a given graph 
    and saves values to a .csv

    Params:
    - G: graph 
    - threshold: Edge weights threshold
    """
    df = pd.read_csv(path)
    print('calculating node coefs ...')
    clustering_coeffs = nx.clustering(G) # backend="cugraph"
    print('calculating ...')
    avg_clustering_coeff = sum(clustering_coeffs.values()) / len(clustering_coeffs)
    print(f"Clustering Coefficient: {avg_clustering_coeff}")

    new_d = {
        "name": [f"co_commenter_net_threshold_{threshold}"],  # name is CSV file name + threshold
        "threshold": threshold,
        "coef_value": avg_clustering_coeff
    }
    
    _df = pd.DataFrame(new_d)

    
    df = pd.concat([df, _df], ignore_index=True)
    df.to_csv(path, index=False)


def get_subgraph_with_threshold(G, threshold):
    """
    Filters a graph given a edge weight threshold
    any edges with its weight < threshold gets filtered out

    Params:
    - G: NetworkX Graph
    - threshold: threshold int
    """
    edges_below_thresh = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] < threshold]
    print('got edges above threshold')
    G.remove_edges_from(edges_below_thresh)
    print(f"Threshold: {threshold}")
    return G

def plot_elbow_point(path):
    df = pd.read_csv(path)

    plt.figure(figsize=(10, 6))
    plt.plot(df['threshold'], df['coef_value'], marker='o', linestyle='-', color='b')

    plt.title('Clustering Coefficient vs Threshold', fontsize=14)
    plt.xlabel('Threshold', fontsize=12)
    plt.ylabel('Clustering Coefficient', fontsize=12)

    plt.xticks(ticks=range(1, 26))

    for i, txt in enumerate(df['coef_value']):
        plt.text(df['threshold'][i], df['coef_value'][i], f'{txt:.3f}', fontsize=10, ha='center')

    plt.grid(True)
    # plt.show()
    plt.savefig(f"./data/{ytbr}/imgs/clustering_coef_x_treshold25.png")

def main(path):
    # threshold = 20
    for threshold in range(11,26):
        G = get_subgraph_with_threshold(load_graph(path), threshold)
        _path = f'./data/{ytbr}/co_commenter_net_threshold.csv'
        calc_clustering_coef(G, threshold, _path)

ytbr = "felipeneto"
if __name__ == "__main__":
    path = f'./data/{ytbr}/co_commenter_network.pickle'
    # main(path)
    plot_elbow_point(f"./data/{ytbr}/co_commenter_net_threshold.csv")
