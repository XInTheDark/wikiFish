from fetch_links import fetch_links
import os
import time
import atexit

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

def construct(start, depth=5):
    """Constrct a tree of links, starting from a given link, using DFS.

    @param start: The link to start from.
    @param depth: The maximum depth of the tree to construct.
    """
    global visited, FILENAME
    # Initialize the set of visited links
    visited = set()

    FILENAME = 'adj_{}_{}_{}.txt'.format(start.split('/')[-1], depth, time.strftime('%d-%m-%y_%H_%M'))
    
    dfs(start, depth)

    # Completed

    # save as filename: adj/ adj_{start}_{depth}_{time (dd-mm-yy_hh_mm)}.txt
    if SAVE:
        # delete the old file
        if os.path.exists(FILENAME):
            os.remove(FILENAME)

        FILENAME = 'adj_{}_{}_{}.txt'.format(start.split('/')[-1], depth, time.strftime('%d-%m-%y_%H_%M'))
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
        filename = FILENAME
        save_adj(str(adj), filename)
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
        
def get_adj(start, depth):
    # try to load from file
    filename = 'adj_{}_{}.txt'.format(start.split('/')[-1], depth)
    try:
        with open(os.path.join('adj', filename), 'r') as f:
            return eval(f.read())
    except FileNotFoundError:
        construct(start, depth, save=True)
        return adj
        

def save_adj(s, filename):
    # create dir adj if it doesn't exist
    if not os.path.exists('adj'):
        os.mkdir('adj')
    with open(os.path.join('adj', filename), 'w') as f:
        f.write(s)

@atexit.register
def on_exit():
    global adj, FILENAME
    if SAVE:
        save_adj(str(adj), FILENAME)
        print('Saved to {}'.format(FILENAME))


if __name__ == '__main__':
    start = input('> ')
    depth = int(input('Depth > '))
    construct(start, depth)
    print(len(adj))
    print(nodes)
    