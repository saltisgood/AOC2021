from copy import copy

with open('input-6.txt', 'r') as f:
    fishies = [int(x) for x in f.readline().strip().split(',')]

def dumb(fishies):
    for i in range(1, 257):
        for x in range(len(fishies)):
            if fishies[x] == 0:
                fishies[x] = 6
                fishies.append(8)
            else:
                fishies[x] -= 1
        print(f'Day {i}: {len(fishies)}')#' fishies ({fishies})')
    
    print(len(fishies))

def smart(fishies):
    fish_buckets = [0] * 10
    for fish in fishies:
        fish_buckets[fish] += 1
    
    def fish_count():
        return sum(fish_buckets)
    
    for i in range(1, 257):
        zeros = fish_buckets[0]
        fish_buckets[9] = zeros
        fish_buckets[7] += zeros
        for f in range(len(fish_buckets) - 1):
            fish_buckets[f] = fish_buckets[f+1]
        fish_buckets[9] = 0
        print(f'Day {i}: {fish_count()}')#' fishies ({fish_buckets})')

#dumb(copy(fishies))
smart(fishies)
