import random
import yaml
import heapq

def read_graph(file):
    try:
        with open(file, 'r') as f:
            graph = yaml.safe_load(f)
        return graph
    except Exception as e:
        print(f"cannot open {file}:", e)
        return None

def check_graph_symmetric(graph):
    for node1 in graph['nodes']:
        for node2 in graph['nodes']:
            try:
                assert (node1 in graph['edges'][node2]) == (node2 in graph['edges'][node1])
            except:
                print(f"assertion failed for {node1} and {node2}")
                return False
            if node1 not in graph['edges'][node2]:
                continue
            try:
                assert graph['edges'][node2][node1] == graph['edges'][node1][node2]
            except:
                print(f"edges not equal for {node1} and {node2}")
                return False
    return True

def push_neighs(connected, graph, pq):
    for node in connected:
        peers = list(graph['edges'][node])
        for peer in peers:
            if peer in connected:
                continue
            weight = graph['edges'][node][peer]
            edge = (node, peer)
            heapq.heappush(pq, (weight, edge))
def find_minimal(graph):
    pq = []
    connected = []
    minimal = []
    total_weight = 0
    seed = random.choice(graph['nodes'])
    connected.append(seed)
    push_neighs(connected, graph, pq)

    while len(pq):
        least_weight, edge = heapq.heappop(pq)
        peer = edge[1]
        if peer in connected:
            continue
        connected.append(peer)
        minimal.append(edge)
        total_weight += least_weight
        push_neighs(connected, graph, pq)
    return total_weight, minimal


graph = read_graph("graph.yaml")
if graph is None:
    exit(1)
check_graph_symmetric(graph)
weight, minimal = find_minimal(graph)
assert(weight == 14)
