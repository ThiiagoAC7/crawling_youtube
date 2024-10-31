from constants import *
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
import seaborn as sns


def merge_channel_dfs():
    netw_metrics_df = pd.DataFrame()
    clic_metrics_df = pd.DataFrame()
    comm_metrics_df = pd.DataFrame()

    for y in YTBRS_LIST:
        CURR_YTBR = y
        CURR_PATH = f"./data/{CURR_YTBR}/"

        _network_metrics = pd.read_csv(
            CURR_PATH+"metrics/commenter_network_metrics.csv")
        _clique_metrics = pd.read_csv(
            CURR_PATH+"metrics/commenter_network_clique_metrics.csv")
        _community_metrics = pd.read_csv(
            CURR_PATH+"metrics/commenter_network_community_metrics.csv")

        _network_metrics["youtuber"] = CURR_YTBR
        _clique_metrics["youtuber"] = CURR_YTBR
        _community_metrics["youtuber"] = CURR_YTBR

        netw_metrics_df = pd.concat(
            [netw_metrics_df, pd.DataFrame(_network_metrics)], ignore_index=True)
        clic_metrics_df = pd.concat(
            [clic_metrics_df, pd.DataFrame(_clique_metrics)], ignore_index=True)
        comm_metrics_df = pd.concat(
            [comm_metrics_df, pd.DataFrame(_community_metrics)], ignore_index=True)

    netw_metrics_df.to_csv("./data/youtubers_networks_metrics.csv")
    clic_metrics_df.to_csv("./data/youtubers_networs_clique_metrics.csv")
    comm_metrics_df.to_csv("./data/youtubers_networks_community_metrics.csv")


def build_df_metrics():
    df_network = pd.read_csv("./data/youtubers_networks_metrics.csv")
    df_cliques = pd.read_csv(
        "./data/youtubers_networs_clique_metrics.csv").drop("max_clique_idx", axis=1)

    df_metrics = pd.merge(df_network, df_cliques, on="youtuber")

    return df_metrics


def apply_pca(df, n_components=2):
    features = df.drop(columns=['youtuber'])
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(scaled_features)

    pca_df = pd.DataFrame(data=pca_result, columns=[
                          f'PC{i+1}' for i in range(n_components)])
    pca_df['youtuber'] = df['youtuber'].values
    return pca_df


def apply_kmeans(df, n_clusters=5):
    features = df.drop(columns=['youtuber'])
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans_values = kmeans.fit_predict(features)
    return kmeans_values


def apply_hierarchical(df_metrics, method='single'):
    linked = linkage(df_metrics.drop(columns=['youtuber']), method=method)
    return linked


def visualize_kmeans(pca_df, df_metrics):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='PC1', y='PC2', hue='kmeans_cluster',
                    data=df_metrics, palette='Set1', s=100)
    for i, txt in enumerate(pca_df['youtuber']):
        plt.annotate(
            txt, (pca_df['PC1'][i], pca_df['PC2'][i]), fontsize=8, ha='left')
    # plt.title('K-means Clustering on PCA Components')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    # plt.show()
    plt.savefig("./data/KMeans_PCA.png")


def visualize_dendrogram(linked, labels):
    plt.figure(figsize=(10, 7))
    dendrogram(linked, labels=labels, leaf_rotation=90, leaf_font_size=10)
    # plt.title('Hierarchical Clustering Dendrogram')
    plt.ylabel("Distance")
    # plt.show()
    plt.savefig("./data/Hierarchical_clustering.png")


def plot_feature_simmilarity():
    df_metrics = build_df_metrics()
    pca_df = apply_pca(df_metrics)
    kmeans_values = apply_kmeans(df_metrics)
    df_metrics['kmeans_cluster'] = kmeans_values
    df_metrics.insert(0, 'kmeans_cluster', df_metrics.pop('kmeans_cluster'))
    df_metrics = pd.merge(pca_df, df_metrics, on="youtuber")
    linked = apply_hierarchical(df_metrics)

    visualize_kmeans(pca_df, df_metrics)
    visualize_dendrogram(linked, labels=df_metrics['youtuber'].values)

    df_metrics.to_csv("./data/metrics_per_youtuber.csv", index=False)
