with open('input-12.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]

class Node:
    def __init__(self, name):
        self.name = name
        self.links = []
    
    @property
    def is_start(self): return self.name == 'start'

    @property
    def is_end(self): return self.name == 'end'

    @property
    def is_big(self): return self.name.upper() == self.name

start = Node('start')
end = Node('end')
all_nodes = {'start': start, 'end': end}
for line in lines:
    fr, to = line.split('-')
    if fr not in all_nodes:
        all_nodes[fr] = Node(fr)
    if to not in all_nodes:
        all_nodes[to] = Node(to)
    all_nodes[fr].links.append(all_nodes[to])
    all_nodes[to].links.append(all_nodes[fr])

def traverse_p1(node, visited: set):
    if not node.is_big:
        visited.add(node.name)
    paths = []
    for link in node.links:
        if link.is_end:
            paths.append([node.name, link.name])
            continue
        if not link.is_big and link.name in visited:
            continue
        found_paths = traverse_p1(link, visited)
        if found_paths:
            for found_path in found_paths:
                paths.append([node.name] + found_path)
    if not node.is_big: 
        visited.remove(node.name)
    return paths

def has_double(visited):
    return any(visited[n.name] == 2 for n in all_nodes.values() if not n.is_big)

def traverse_p2(node, visited):
    if not node.is_big:
        visited[node.name] += 1
    paths = []
    for link in node.links:
        if link.is_end:
            paths.append([node.name, link.name])
            continue
        if not link.is_big:
            if visited[link.name] >= 2:
                continue
            if visited[link.name] == 1 and has_double(visited):
                continue

        if link.is_start:
            continue
        found_paths = traverse_p2(link, visited)
        if found_paths:
            for found_path in found_paths:
                paths.append([node.name] + found_path)
    if not node.is_big: 
        visited[node.name] -= 1
    return paths

def p1():
    visited = set()
    paths = traverse_p1(start, visited)
    print(len(paths))
    #for path in sorted(paths):
        #print(path)

def p2():
    visited = {n: 0 for n in all_nodes.keys()}
    paths = traverse_p2(start, visited)
    print(len(paths))
    #for path in sorted(paths):
        #print(path)

p1()
p2()