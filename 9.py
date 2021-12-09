with open('input-9.txt', 'r') as f:
    lines = f.readlines()

grid = []
for line in lines:
    grid.append([int(x) for x in line.strip()])

def get_adjacents(x, y):
    adjacents = []
    if y > 0:
        adjacents.append((y-1, x))
    if x > 0:
        adjacents.append((y, x-1))
    if y < len(grid)-1:
        adjacents.append((y+1, x))
    if x < len(grid[0])-1:
        adjacents.append((y, x+1))
    return adjacents 

lows = set()
for y in range(len(grid)):
    for x in range(len(grid[0])):
        val = grid[y][x]
        adjvals = [grid[y][x] for y, x in get_adjacents(x, y)]
        if val < min(adjvals):
            lows.add((x, y))

def build_basin(basin, x, y):
    adjacents = get_adjacents(x, y)
    val = grid[y][x]
    for adjy, adjx in adjacents:
        adjval = grid[adjy][adjx]
        if adjval < val or adjval == 9 or (adjx, adjy) in basin:
            continue
        basin.add((adjx, adjy))
        build_basin(basin, adjx, adjy)

def p2():
    basin_sizes = []
    for x, y in lows:
        basin = set()
        basin.add((x, y))
        build_basin(basin, x, y)
        basin_sizes.append(len(basin))

    big_basins = [x for x in sorted(basin_sizes)][-3:]
    print(big_basins)
p2()
