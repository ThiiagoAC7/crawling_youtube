import networkx as nx

G = nx.karate_club_graph()  # Example graph
community_nodes = [0, 1, 2, 3, 7, 8, 13, 27]  # Example community

community_subgraph = G.subgraph(community_nodes)

community_density = nx.density(community_subgraph)
print(f"Community Density: {community_density:.4f}")

community_degrees = [deg for node, deg in nx.degree(community_subgraph)]
avg_community_degree = sum(community_degrees) / len(community_degrees)
print(f"Average Community Degree: {avg_community_degree:.4f}")

community_degree_centralities = nx.degree_centrality(community_subgraph)
avg_community_degree_centrality = sum(community_degree_centralities.values()) / len(community_degree_centralities)
print(f"Average Community Degree Centrality: {avg_community_degree_centrality:.4f}")

community_clustering_coefficients = nx.clustering(community_subgraph)
avg_community_clustering_coefficient = sum(community_clustering_coefficients.values()) / len(community_clustering_coefficients)
print(f"Average Community Clustering Coefficient: {avg_community_clustering_coefficient:.4f}")
