# MySNA

A package for SNA (Social Network Analysis) and community detection.

This package was created for the course "DS223 Marketing Analytics", Fall 2022 Semester.

### Features

- Find nodes with highest/lowest degree and the corresponding degrees
- Find the nodes with the highest/lowest betweenness/closeness/eigenvector centralities
- Find the communities in the network
- Find community of a given node
- Draw graph with communities and influencers
- Draw the community of a given node, showing influencers of the community

### Usage

```
import MySNA

G = nx.karate_club_graph()

# Find the first 5 nodes with highest Closeness Centrality
MySNA.get_first_n_highest_closeness_nodes(G, 5)  # returns a list of the first 5 nodes, in decreasing order

# Find communities
MySNA.find_communities(G, label=False)  # returns a dictionary of communities and respective lists of nodes

# Find and draw the community that contains the node '7'
MySNA.draw_community_with_node(G, 7, label=True)  # returns a graph of the community, highlighting the influencers
```

