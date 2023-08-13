import construct
from utils import *
from fetch_links import Shorten, Lengthen

def find_path(start, end, file=None):
    """Find the shortest path between two articles."""
    adj = None
    if file is None:
        adj = construct.get_adj(start, 5)
    else:
        construct.SAVE = False
        adj = load_adj(file)
    
    # BFS - O(V + E)
    visited = set()
    q = [(start, [start])]
    while len(q) > 0:
        article, path = q.pop(0)
        visited.add(article)
        if article == end:
            return path
        try:
            for link in adj[article]:
                if link not in visited:
                    q.append((link, path + [link]))
        except KeyError:
            pass
    
    return None

if __name__ == '__main__':
    file = input('File > ')
    start = input('Start > ')
    end = input('End > ')
    start = Shorten(start)
    end = Shorten(end)

    path = find_path(start, end, file)
    print(path)