from fetch_links import *
import os
import time
import atexit
from utils import *

adj = {}  # adjacency list
visited = set()
nodes = 0
prev_nodes = 0

# constants
limit = 1<<10
# adjust limit to get more links per generation. This does not slow down the generation at all.
# However, the actual path-finding algorithm (time complexity O(N)) will be slower.
# So use this variable to create a balance between quantity and speed.

nodes_limit = 1<<20
SAVE = True

FILENAME = ''

# BFS only
q = []

def construct(start, depth=5, algo='bfs'):
    """Constrct a tree of links, starting from a given link, using DFS.

    @param start: The link to start from.
    @param depth: The maximum depth of the tree to construct.
    """
    global visited, FILENAME
    # Initialize the set of visited links
    visited = set()

    FILENAME = 'adj_{}_{}_{}.txt'.format(start, depth, time.strftime('%d-%m-%y_%H_%M'))
    
    # construct the tree
    print(f"Using algorithm {algo}")
    if algo.lower() == 'dfs':
        dfs(start, depth)
    elif algo.lower() == 'bfs':
        bfs(start, depth)
    else:
        raise ValueError('Invalid algorithm (dfs or bfs)')

    # --- Completed ---

    # save as filename: adj/ adj_{start}_{depth}_{time (dd-mm-yy_hh_mm)}.txt
    if SAVE:
        # delete the old file
        if os.path.exists(FILENAME):
            os.remove(FILENAME)

        FILENAME = 'adj_{}_{}_{}.txt'.format(start, depth, time.strftime('%d-%m-%y_%H_%M'))
        save_adj(str(adj), FILENAME)
        

# DFS
def dfs(article, d):
    """DFS from a given article."""
    global adj, nodes, visited, limit, nodes_limit, prev_nodes

    if d <= 0 or nodes >= nodes_limit or article in visited:
        return
    
    # Save every time the number of nodes doubles
    if SAVE and nodes >= prev_nodes * 2:
        print("Nodes: {}".format(nodes))
        save_adj(str(adj), FILENAME)
        prev_nodes = nodes

    # Fetch the links
    links = fetch_links(article, limit=limit)

    # Add the article to the visited set
    visited.add(article)

    # Add the links to the adjacency list
    adj[article] = links

    # DFS from each link
    for link in links:
        dfs(link, d - 1)
        nodes += 1


# BFS
def bfs(start, depth):
    global visited, adj, nodes, nodes_limit, prev_nodes, q

    visited = set()
    q = [(start, 0)]
    while len(q) > 0:
        article, d = q.pop(0)
        visited.add(article)
        if d > depth:
            break

        if article not in adj:
            adj[article] = []
        links = fetch_links(article)

        for link in links:
            if link not in visited:
                adj[article].append(link)
                q.append((link, d + 1))
                nodes += 1
                
        if SAVE and nodes >= prev_nodes * 2:
            print('Nodes: {}'.format(nodes))
            save_adj(str(adj), FILENAME)
            prev_nodes = nodes

        if nodes >= nodes_limit:
            break


def get_adj(start, depth):
    # try to load from file
    filename = 'adj_{}_{}.txt'.format(start, depth)
    try:
        with open(os.path.join('adj', filename), 'r') as f:
            return eval(f.read())
    except FileNotFoundError:
        construct(start, depth, save=True)
        return adj


@atexit.register
def on_exit():
    global adj, FILENAME
    if SAVE:
        save_adj(str(adj), FILENAME)
        print('Saved to {}'.format(FILENAME))
        print('Total nodes: {}'.format(nodes))

        if len(q) > 0:
            # save queue
            save_adj(str(q), 'q_{}.txt'.format(FILENAME))


if __name__ == '__main__':
    start = input('> ')
    depth = int(input('Depth > '))
    nodes_limit = input('Nodes limit > ')
    nodes_limit = int(nodes_limit) if nodes_limit != '' else 1<<20

    start = Shorten(start)

    construct(start, depth)
    print(len(adj))
    print(nodes)
    