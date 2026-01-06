import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
bayesian_network = nx.DiGraph()

# Add nodes and edges to represent the Bayesian Network
# Nodes: S (Steep Mountain), C (Snow Cover), W (Weather), A (Avalanche)
bayesian_network.add_edges_from([
    ('S', 'A'),  # S -> A
    ('C', 'A'),  # C -> A
    ('W', 'C')   # W -> C
])

# Draw the Bayesian Network
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(bayesian_network)  # Layout for the graph
nx.draw(
    bayesian_network, 
    pos, 
    with_labels=True, 
    node_color="skyblue", 
    node_size=2000, 
    font_size=12, 
    font_weight="bold", 
    arrowsize=20
)

plt.title("Bayesian Network for Avalanche Probability", fontsize=14)
plt.show()