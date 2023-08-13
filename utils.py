import os

def load_adj(filename):
    prefix = ['adj/', '', 'adj/public/', 'adj/test/', '/']
    suffix = ['', '.txt']
    for i in prefix:
        for j in suffix:
            try:
                with open(i + filename + j, 'r') as f:
                    return eval(f.read())
            except FileNotFoundError:
                continue

def save_adj(s, filename):
    # create dir adj if it doesn't exist
    if not os.path.exists('adj'):
        os.mkdir('adj')
    with open(os.path.join('adj', filename), 'w') as f:
        f.write(s)


def get_nodes(filename):
    adj = load_adj(filename)
    l = 0
    for key, value in adj.items():
        l += len(value)
    return l

def from_natural_language(x):
    return x.replace(' ', '_')