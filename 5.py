with open('input-5.txt', 'r') as f:
#with open('test-input-5.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]

def print_grid(grid):
    height = len(grid[0])
    for i in range(height):
        print(''.join(str(x[i]) for x in grid))

class Segment:
    def __init__(self, startx, starty, endx, endy):
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.width = self.endx - self.startx
        self.height = self.endy - self.starty
    
    @property
    def straight(self):
        return self.width == 0 or self.height == 0
    
    def points(self):
        xdir = 1
        ydir = 1
        width = self.width
        height = self.height
        if width < 0:
            xdir = -1
            width = -width
        if height < 0:
            ydir = -1
            height = -height
        
        if width == 0:
            for y in range(height+1):
                yield (self.startx, self.starty + (ydir * y))
        elif height == 0:
            for x in range(width+1):
                yield (self.startx + (xdir * x), self.starty)
        else:
            for i in range(width+1):
                yield (self.startx + (xdir * i), self.starty + (ydir * i))

segments = []
maxx = 0
maxy = 0
for line in lines:
    start, end = line.split(' -> ')
    startx, starty = [int(i) for i in start.split(',')]
    endx, endy = [int(i) for i in end.split(',')]
    segments.append(Segment(startx, starty, endx, endy))
    if startx > maxx:
        maxx = startx
    elif endx > maxx:
        maxx = endx
    if starty > maxy:
        maxy = starty
    elif endy > maxy:
        maxy = endy

grid = []
for x in range(maxx+1):
    col = []
    for y in range(maxy+1):
        col.append(0)
    grid.append(col)

#segments = [seg for seg in segments if seg.straight]
#breakpoint()

for seg in segments:
    for x, y in seg.points():
        grid[x][y] += 1
#print_grid(grid)

count = 0
for col in grid:
    for cell in col:
        if cell >= 2:
            count += 1

print(str(count))