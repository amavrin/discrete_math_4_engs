import random
import yaml
import heapq
import logging


logging.basicConfig(level=logging.DEBUG)


def read_graph(file):
    try:
        with open(file, 'r') as f:
            graph = yaml.safe_load(f)
        return graph
    except Exception as e:
        logging.info(f"cannot open {file}: {e}")
        return None


def check_graph_symmetric(graph):
    if graph is None:
        return False
    if 'nodes' not in graph:
        logging.info("key 'nodes' not in graph")
        return False
    if 'edges' not in graph:
        logging.info("key 'edges' not in graph")
        return False
    if not graph['nodes']:
        return True
    if not graph['edges']:
        return True
    for node1 in graph['nodes']:
        for node2 in graph['nodes']:
            node1_peers = graph['edges'][node1]
            node2_peers = graph['edges'][node2]
            if (node1 in node2_peers) != (node2 in node1_peers):
                logging.info(f"peers for {node1} {node1_peers} and {node2} {node2_peers} do not match")
                return False
            if node1 not in node2_peers:
                continue
            if node2_peers[node1] != node1_peers[node2]:
                logging.info(f"edge weights are not equal for {node1}-{node2} ({node1_peers[node2]})",
                        f"and {node2}-{node1} ({node2_peers[node1]})")
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


def main(file):
    graph = read_graph(file)
    if not check_graph_symmetric(graph):
        logging.error("graph is invalid or not symmetric")
        exit(1)
    weight, minimal = find_minimal(graph)
    assert(weight == 14)


if __name__ == "__main__":
    main("graph.yaml")