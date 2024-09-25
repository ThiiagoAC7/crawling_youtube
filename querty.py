import matplotlib.pyplot as plt
import networkx as nx

from faint import load_graph


def plot_co_commenter_graph(G):
    print('plotting ...')
    plt.figure(figsize=(20, 20))

    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=20, node_color='red')
    print('Nodes desenhados ...')

    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos,
                           width=[0.001 * edge[2]['weight'] for edge in edges])
    print('edges desenhados ...')

    plt.title("Co-commenter Network")
    plt.axis('off')  # Turn off the axis
    print('sarvano ...')
    # plt.show()
    plt.savefig(f"./data/{ytbr}/co_commenter_network_thresh_10.png")
    print('sarvado')


def plot_video_commenter_graph(G):
    print("plotting ...")
    node_colors = []
    for node in G.nodes():
        if len(node) == 11: # video_id has fixed length
            node_colors.append('green')  # Video nodes are blue
        else:
            node_colors.append('red')   # Commenter nodes are red

    pos = nx.spring_layout(G)
    plt.figure(figsize=(20, 20))

    print("defined layout")

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=20)

    print("nodes drawn ...")

    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, 
                           width=[0.01 * edge[2]['weight'] for edge in edges])

    print("edges drawn ...")

    plt.title("Video-Commenter Network ")
    plt.axis('off')  # Turn off the axis
    plt.show()
    # plt.savefig(f"./data/{ytbr}/video_commenter_network.png")


ytbr = "felipeneto"
def main():
    co_commenter_path = f'./data/{ytbr}/co_commenter_network.pickle'
    vid_commenter_path = f'./data/{ytbr}/video_commenter_network.pickle'
    # G = load_graph(co_commenter_path, filter=True, threshold=17, n=10000)
    # plot_co_commenter_graph(G)
    G = load_graph(vid_commenter_path, 
                   filter=True)
    plot_video_commenter_graph(G)


if __name__ == "__main__":
    main()
