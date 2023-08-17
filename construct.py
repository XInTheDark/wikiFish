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
limit = 1<<6
# adjust limit to get more links per generation. 
# Increasing this will result in wider, but shallower, trees.

nodes_limit = 1<<20
SAVE = True

FILENAME = ''
FOLDER = ''

# BFS only
q = []

start_time = time.time()

def construct(start, depth=5, algo='bfs'):
    """Constrct a tree of links, starting from a given link, using DFS.

    @param start: The link to start from.
    @param depth: The maximum depth of the tree to construct.
    """
    global visited, FILENAME, FOLDER
    # Initialize the set of visited links
    visited = set()

    FILENAME = 'adj_{}_{}_{}.txt'.format(start, depth, time.strftime('%d-%m-%y_%H_%M'))
    FOLDER = '{}_{}_{}'.format(start, depth, time.strftime('%d-%m-%y_%H_%M'))
    if SAVE:
        # create dir adj if it doesn't exist
        if not os.path.exists('adj'):
            os.mkdir('adj')
        if not os.path.exists(os.path.join('adj', FOLDER)):
            os.mkdir(os.path.join('adj', FOLDER))

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
        save_adj(str(adj), FOLDER, FILENAME)
        print('Saved to {}'.format(FILENAME))
        print('Nodes: {} / Time: {}'.format(nodes, elapsed_time(start_time)))
        

# DFS
def dfs(article, d):
    """DFS from a given article."""
    global adj, nodes, visited, limit, nodes_limit, prev_nodes

    if d <= 0 or nodes >= nodes_limit or article in visited:
        return
    
    # Save every time the number of nodes doubles
    if SAVE and nodes >= prev_nodes * 2:
        print("Nodes: {} / Time: {}".format(nodes, elapsed_time(start_time)))
        save_adj(str(adj), FOLDER, FILENAME)
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
            print('Nodes: {} / Time: {}'.format(nodes, elapsed_time(start_time)))
            save_adj(str(adj), FOLDER, FILENAME)
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
        save_adj(str(adj), FOLDER, FILENAME)
        print('Saved to {}'.format(FILENAME))
        print('Total nodes: {} / Time: {}'.format(nodes, elapsed_time(start_time)))

        if len(q) > 0 and nodes < nodes_limit:
            # save queue
            save_adj(str(q), FOLDER, 'q_{}.txt'.format(FILENAME))
            print('Saved queue to q_{}.txt'.format(FILENAME))
            # save visited
            save_adj(str(visited), FOLDER, 'visited_{}.txt'.format(FILENAME))
            print('Saved visited to visited_{}.txt'.format(FILENAME))


if __name__ == '__main__':
    start = input('> ')
    depth = int(input('Depth > '))
    nodes_limit = input('Nodes limit > ')
    nodes_limit = int(nodes_limit) if nodes_limit != '' else 1<<20

    start = Shorten(start)

    construct(start, depth)
    print(len(adj))
    print(nodes)
    