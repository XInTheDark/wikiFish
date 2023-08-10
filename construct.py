from fetch_links import fetch_links
import os

adj = {}  # adjacency list
visited = set()
nodes = 0

# constants
limit = 1<<8
# adjust limit to get more links per generation. This does not slow down the generation at all.
# However, the actual path-finding algorithm (time complexity O(N)) will be slower.
# So use this variable to create a balance between quantity and speed.

nodes_limit = 1<<10

def construct(start, depth=5, save=True):
    """Constrct a tree of links, starting from a given link, using DFS.

    @param start: The link to start from.
    @param depth: The maximum depth of the tree to construct.
    """
    global visited
    # Initialize the set of visited links
    visited = set()
    
    dfs(start, depth)

    # save as filename: adj/ adj_{start}_{depth}.txt
    if save:
        # create dir adj if it doesn't exist
        if not os.path.exists('adj'):
            os.mkdir('adj')
        filename = 'adj_{}_{}.txt'.format(start.split('/')[-1], depth)
        with open(os.path.join('adj', filename), 'w') as f:
            f.write(str(adj))

# DFS
def dfs(article, d):
    """DFS from a given article."""
    global adj, nodes, visited, limit, nodes_limit

    if d <= 0 or nodes >= nodes_limit or article in visited:
        return

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
        
        
if __name__ == '__main__':
    construct('https://en.wikipedia.org/wiki/Artificial_intelligence')
    print(adj)
    print(len(adj))
    print(nodes)
    