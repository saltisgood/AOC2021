with open('input-7.txt', 'r') as f:
    poses = [int(x) for x in f.readline().split(',')]

def get_distance(pos):
    return sum(abs(pos - x) for x in poses)

dists = [get_distance(i) for i in range(max(poses))]
print(min(dists))

fuels = [0]
for d in range(1, max(dists)+1):
    fuels.append(fuels[-1]+d)

def get_fuel(pos):
    return sum(fuels[abs(pos - x)] for x in poses)

min_fuels = [get_fuel(i) for i in range(max(poses))]
print(min(min_fuels))
