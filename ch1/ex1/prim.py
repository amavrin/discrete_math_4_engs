import random

import yaml


def read_graph(file):
    with open(file, 'r') as f:
        graph = yaml.safe_load(f)
    return graph

def check_graph_symmetric(graph):
    for node1 in graph['nodes']:
        for node2 in graph['nodes']:
            try:
                assert (node1 in graph['edges'][node2]) == (node2 in graph['edges'][node1])
            except:
                print(f"assertion failed for {node1} and {node2}")
            if node1 not in graph['edges'][node2]:
                continue
            try:
                assert graph['edges'][node2][node1] == graph['edges'][node1][node2]
            except:
                print(f"edges not equal for {node1} and {node2}")

def find_neighs(connected, graph):
    neighs = dict()
    for node in connected:
        peers = list(graph['edges'][node])
        for peer in peers:
            if peer in connected:
                continue
            weight = graph['edges'][node][peer]
            neighs[(node, peer)] = weight
    return neighs

def find_minimal(graph):
    connected = []
    minimal = []
    total_weight = 0
    seed = random.choice(graph['nodes'])
    connected.append(seed)
    current = seed
    while len(connected) < len(graph['nodes']):
        paths = find_neighs(connected, graph)
        sorted_paths = dict(sorted(paths.items(), key=lambda item: item[1]))

        edge = list(sorted_paths.items())[0]
        connected.append(edge[0][1])
        minimal.append(edge[0])
        total_weight += edge[1]
    return total_weight, minimal


graph = read_graph("graph.yaml")
check_graph_symmetric(graph)
weight, minimal = find_minimal(graph)
print(weight, minimal)
