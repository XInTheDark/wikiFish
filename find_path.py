import construct
def find_path(start, end):
    """Find the shortest path between two articles."""
    adj = construct.get_adj(start, 5)
    
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
    start = input('Start > ')
    end = input('End > ')
    path = find_path(start, end)
    print(path)