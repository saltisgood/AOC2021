
flashes = 0

class Octodad:
    def __init__(self, value: int):
        self.value = value
        self.flashed = False
    
    def inc(self):
        self.value += 1
    
    def flash(self):
        self.flashed = True
        global flashes
        flashes += 1
    
    def end_step(self):
        if self.flashed:
            self.value = 0
            self.flashed = False
        assert(self.value <= 9)
    
    def __str__(self):
        return str(self.value)

with open('input-11.txt', 'r') as f:
    grid = [[Octodad(int(x)) for x in line.strip()] for line in f.readlines()]

octos = []
for line in grid:
    for o in line:
        octos.append(o)

def print_grid(step, g):
    print('After step: ' + str(step))
    for line in g:
        print(''.join(str(o) for o in line))

def inc_step(grid, octos):
    for octo in octos:
        octo.inc()

def get_adj(grid, x, y):
    adj = []
    if x > 0:
        if y > 0:
            adj.append((y-1, x-1))
        adj.append((y, x-1))
        if y < len(grid)-1:
            adj.append((y+1, x-1))
    if y > 0:
        adj.append((y-1, x))
    if y < len(grid)-1:
        adj.append((y+1, x))
    if x < len(grid[0])-1:
        if y > 0:
            adj.append((y-1, x+1))
        adj.append((y, x+1))
        if y < len(grid)-1:
            adj.append((y+1, x+1))
    return adj

def do_flash(grid, x, y):
    octo = grid[y][x]
    if octo.value > 9 and not octo.flashed:
        octo.flash()
        adj = get_adj(grid, x, y)
        for y2, x2 in adj:
            o = grid[y2][x2]
            if not o.flashed:
                o.inc()
                do_flash(grid, x2, y2)
    
def flash_step(grid, octos):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            do_flash(grid, x, y)

def end_step(grid, octos):
    for octo in octos:
        octo.end_step()

def p1(grid, octos):
    #breakpoint()
    for i in range(100):
        inc_step(grid, octos)
        flash_step(grid, octos)
        end_step(grid, octos)
        print_grid(i+1, grid)
        #breakpoint()
    print(flashes)
#p1(grid, octos)

def p2(grid, octos):
    global flashes
    flashes = 0
    i = 1
    while True:
        flashes = 0
        inc_step(grid, octos)
        flash_step(grid, octos)
        end_step(grid, octos)
        if flashes == 100:
            print(i)
            break
        i += 1
p2(grid, octos)