import time

with open('input-15.txt', 'r') as f:
    points = [[int(x) for x in line.strip()] for line in f.readlines()]

def new_val(points, x, y, dx, dy):
    old_val = points[y][x]
    n = old_val + dx + dy
    if n > 9:
        n = n % 9
    return n

def build_big_grid(points):
    orig_width = len(points[0])
    orig_height = len(points)
    new_width = orig_width * 5
    new_height = orig_width * 5
    new_points = [[0 for x in range(new_width)] for y in range(new_height)]
    for dx in range(5):
        for dy in range(5):
            for x in range(orig_width):
                for y in range(orig_height):
                    new_points[(dy * orig_height) + y][(dx * orig_width) + x] = new_val(points, x, y, dx, dy)
    return new_points

points = build_big_grid(points)

width = len(points[0])
height = len(points)
num_points = width * height

def index(x, y):
    return y * width + x

def min_node(dist, q):
    min_val = None
    min_node = None
    for x, y in q:
        d = dist[index(x, y)]
        if min_val is None or (d is not None and d < min_val):
            min_val = d
            min_node = (x, y)
    
    return min_node

def neighbours(x, y):
    if x > 0:
        yield x-1, y
    if x < width-1:
        yield x+1, y
    if y > 0:
        yield x, y-1
    if y < height-1:
        yield x, y+1

def dijkstra(graph):
    q = set()

    dist = [None] * num_points
    prev = [None] * num_points

    for x in range(width):
        for y in range(height):
            q.add((x, y))
    dist[0] = 0

    while q:
        u = min_node(dist, q)
        q.remove(u)

        for v in neighbours(u[0], u[1]):
            if v not in q:
                continue

            alt = dist[index(*u)] + graph[v[1]][v[0]]
            if dist[index(*v)] is None or alt < dist[index(*v)]:
                dist[index(*v)] = alt
                prev[index(*v)] = u
    
    return dist, prev

def p1():
    dist, prev = dijkstra(points)
    print(dist[index(width-1, height-1)])
    #print(dist)
    #print(prev)
p1()