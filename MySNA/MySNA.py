import networkx as nx
from operator import itemgetter
import matplotlib.pyplot as plt
import community.community_louvain as community_louvain


def node_with_max_degree(G):
    """Find the node of the graph with the highest degree.

    Parameters
    ----------
    G : graph
        An undirected graph


    Returns
    -------
    max_node_degree: tuple
        The node with the highest degree and the degree of that node
    """
    highest_degree_node = max(G.nodes, key=G.degree)
    max_node_degree = highest_degree_node, G.degree(highest_degree_node)
    return max_node_degree


def node_with_min_degree(G):
    """Find the node of the graph with the lowest degree.

    Parameters
    ----------
    G : graph
        An undirected graph


    Returns
    -------
    min_node_degree: tuple
        The node with the lowest degree and the degree of that node
    """
    lowest_degree_node = min(G.nodes, key=G.degree)
    min_node_degree = lowest_degree_node, G.degree(lowest_degree_node)
    return min_node_degree


def get_first_n_highest_betweenness_nodes(G, n):
    """Find the first n nodes with the highest betweenness centrality

    Parameters
    ----------
    G : graph
        An undirected graph
        
    n : int
        The number of nodes
        

    Returns
    -------
    top_n : list
        The list of the first n nodes with highest betweenness centrality (from highest to lowest in order)
    """
    betweenness_dict = nx.betweenness_centrality(G)
    nx.set_node_attributes(G, betweenness_dict, 'betweenness')
    sorted_betweenness = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)
    top_n = [tup[0] for tup in sorted_betweenness][:n]

    return top_n


def get_first_n_highest_closeness_nodes(G, n):
    """Find the first n nodes with the highest closeness centrality

    Parameters
    ----------
    G : graph
        An undirected graph
        
    n : int
        The number of nodes
        

    Returns
    -------
    top_n : list
        The list of the first n nodes with highest closeness centrality (from highest to lowest in order)
    """
    closeness_dict = nx.closeness_centrality(G)
    nx.set_node_attributes(G, closeness_dict, 'closeness')
    sorted_closeness = sorted(closeness_dict.items(), key=itemgetter(1), reverse=True)
    top_n = [tup[0] for tup in sorted_closeness][:n]

    return top_n

def get_first_n_highest_eigenvector_nodes(G, n):
    """Find the first n nodes with the highest eigenvector centrality

    Parameters
    ----------
    G : graph
        An undirected graph

    n : int
        The number of nodes


    Returns
    -------
    top_n : list
        The list of the first n nodes with highest eigenvector centrality (from highest to lowest in order)
    """
    eigenvector_dict = nx.eigenvector_centrality_numpy(G)
    nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')
    sorted_eigenvector = sorted(eigenvector_dict.items(), key=itemgetter(1), reverse=True)
    top_n = [tup[0] for tup in sorted_eigenvector][:n]

    return top_n

def find_communities(G):
    """Find the communities within the graph

    The function uses the Louvain method to find the best partition of the graph.
    The communities are then stored in a dictionary, where the keys are the
    communities and the values are lists of nodes in a community.

    Parameters
    ----------
    G : graph
        An undirected graph
        

    Returns
    -------
    dict_com: dict
        A dictionary where the keys are the communities and the values are the lists
        containing the the corresponding nodes
    """
    partition = community_louvain.best_partition(G)
    nx.set_node_attributes(G, partition, 'community')
    dict_com = {}
    for i in range(0, max(partition.values())+1):
        selected_data = dict((n, d['community']) for n, d in G.nodes().items()
                             if d['community'] == i)
        dict_com[list(selected_data.values())[0]] = list(selected_data.keys())

    return dict_com


def community_with_node(G, node):
    """Find the community that contains the given node

    Parameters
    ----------
    G : graph
        An undirected graph
        
    node : int or str
        The node whose community you want to find
        

    Returns
    -------
    list_com : list
        A list containing the nodes that are in the same community as the given node
    """
    communities = find_communities(G)
    list_com = [nodes for community, nodes in communities.items() if node in nodes][0]

    return list_com


def draw_communities(G, label=True):
    """Draw the communities using Louvain's best partition method

    Parameters
    ----------
    G : graph
        An undirected graph
        
    label : Boolean
         (Default value = True)
         True for showing labels on the graph, False otherwise

    Returns
    -------
    ax : graph
        The graph, using different colors for each of the communities
    """
    pos = nx.spring_layout(G, seed=394)
    partition = community_louvain.best_partition(G)
    ax = nx.draw(G, with_labels=label, pos=pos, node_color=list(partition.values()),
                 edge_color='black', font_color="whitesmoke")

    return ax


def find_community_influencers(G):
    """Partition the graph into communities and find influencers for each one

    Parameters
    ----------
    G : graph
        An undirected graph
        

    Returns
    -------
    influencers: dict
        A dictionary where the keys are the communities and the values are lists
        containing the influencer nodes of the respective communities
    """
    communities = find_communities(G)
    influencers = {}
    for community, nodes in communities.items():
        sg = G.subgraph(list(nodes))
        top_betweenness = get_first_n_highest_betweenness_nodes(sg, 3)
        top_closeness = get_first_n_highest_closeness_nodes(sg, 3)
        top_influencers = list(set(top_betweenness) & set(top_closeness))
        influencers[community] = top_influencers

    return influencers


def draw_community_influencers(G, label=True):
    """Draw the graph, showing the influencer nodes within the whole graph

    Parameters
    ----------
    G : graph
        An undirected graph
        
    label : Boolean
         (Default value = True)
         True for showing labels on the graph, False otherwise

    Returns
    -------
    ax : graph
        The graph, highlighting the influencer nodes within the whole graph
    """
    influencers = find_community_influencers(G)
    all_influencers = [i for j in influencers.values() for i in j]
    color_map = ['red' if node in all_influencers else 'green' for node in G]
    ax = nx.draw(G, with_labels=label,  node_color=color_map,
                 edge_color='black', font_color="whitesmoke")

    return ax


def draw_community_with_node(G, node, label=True):
    """Draws the community that contains the given node, highlighting the influencer nodes
    within that community

    Parameters
    ----------
    G : graph
        An undirected graph
        
    node : int
        The node whose community you want to find
        
    label : Boolean
         (Default value = True)
         True for showing labels on the graph, False otherwise

    Returns
    -------
    ax : graph
        The graph of the community of the given node, highlighting the influencer
        nodes within the community
    """
    nodes = community_with_node(G, node)
    sg = G.subgraph(list(nodes))
    top_betweenness = get_first_n_highest_betweenness_nodes(sg, 3)
    top_closeness = get_first_n_highest_closeness_nodes(sg, 3)
    top_influencers = list(set(top_betweenness) & set(top_closeness))

    color_map = ['red' if node in top_influencers else 'green' for node in sg]
    nx.draw(sg, with_labels=label, node_color=color_map, edge_color='black', font_color="whitesmoke")

    ax = plt.gca()
    ax.collections[0].set_edgecolor("black")

    return ax


def problemsolver(G):
    """A summary of the problem

    The functions used here can be called separately. This functions simply summarizes
    some of the functions and visualizations

    Parameters
    ----------
    G : graph
        An undirected graph


    Returns
    -------
    Does not return anything. Prints a summary of the graph, containing the nodes with
    highest/lowest degree, Betweenness/Closeness/Eigenvector centralities, number of
    communities, and visualizes the communities and influencers.
    """
    node_with_max_degree_ = node_with_max_degree(G)
    max_node = node_with_max_degree_[0]
    max_degree = node_with_max_degree_[1]

    node_with_min_degree_ = node_with_min_degree(G)
    min_node = node_with_min_degree_[0]
    min_degree = node_with_min_degree_[1]

    num_nodes = len(G.nodes())

    highest_betweenness = get_first_n_highest_betweenness_nodes(G, 1)[0]
    highest_closeness = get_first_n_highest_closeness_nodes(G, 1)[0]
    highest_eigenvector = get_first_n_highest_eigenvector_nodes(G, 1)[0]
    lowest_betweenness = get_first_n_highest_betweenness_nodes(G, num_nodes)[-1]
    lowest_closeness = get_first_n_highest_closeness_nodes(G, num_nodes)[-1]
    lowest_eigenvector = get_first_n_highest_eigenvector_nodes(G, num_nodes)[-1]

    communities = find_communities(G)
    num_communities = len(communities)

    print("The node with highest degree: {}".format(max_node))
    print("The degree of the node with the highest degree: {}".format(max_degree))
    print()
    print("The node with lowest degree: {}".format(min_node))
    print("The degree of the node with the lowest degree: {}".format(min_degree))
    print()
    print("The node with highest Betweenness Centrality: {}".format(highest_betweenness))
    print("The node with lowest Betweenness Centrality: {}".format(lowest_betweenness))
    print()
    print("The node with highest Closeness Centrality: {}".format(highest_closeness))
    print("The node with lowest Closeness Centrality: {}".format(lowest_closeness))
    print()
    print("The node with highest Eigenvector Centrality: {}".format(highest_eigenvector))
    print("The node with lowest Eigenvector Centrality: {}".format(lowest_eigenvector))
    print()
    print("The number of communities in the graph: {}".format(num_communities))
    print()

    ax1 = draw_communities(G)
    print("The graph showing the communities:")
    plt.show()
    print()

    ax2 = draw_community_influencers(G)
    print("The graph showing the influencer nodes (red for incluencers, green for the rest):")
    plt.show()
    print()


