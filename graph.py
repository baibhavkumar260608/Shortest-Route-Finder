import osmnx as ox

CITY = "Kolkata, India"

G = ox.graph_from_place(CITY, network_type="drive")

# Convert graph to GeoDataFrames
nodes, edges = ox.graph_to_gdfs(G)

graph = {}

for node in G.nodes:
    graph[node] = []

for u, v, data in G.edges(data=True):
    graph[u].append((v, data.get("length", 1)))

print(f"Nodes : {len(graph)}")

edge_count = sum(len(graph[node]) for node in graph)

print(f"Edges : {edge_count}")