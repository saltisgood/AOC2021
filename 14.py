from dataclasses import dataclass
from typing import Tuple
import time

with open('input-14.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]

poly = [c for c in lines[0]]
poly = lines[0]


@dataclass
class Template:
    search: Tuple[str, str]
    replace: str

templates = []
for line in lines[2:]:
    x, y = line.split(' -> ')
    templates.append(Template((x[0], x[1]), y))

templates = {}
for line in lines[2:]:
    x, y = line.split(' -> ')
    templates[x] = x[0] + y

def step(poly, templates):
    new_poly = []
    for i in range(len(poly)-1):
        new_poly.append(poly[i])
        try:
            rep = templates[poly[i] + poly[i+1]]
            new_poly.append(rep)
        except KeyError:
            pass
    new_poly.append(poly[-1])
    return new_poly

def step_inplace(poly: list, templates):
    end = len(poly)
    i = 0
    while i < end - 1:
        bit = poly[i] + poly[i+1]
        try:
            rep = templates[bit]
            poly.insert(i+1, rep)
            i += 1
            end += 1
        except KeyError:
            pass
        i += 1

def step_v3(start, pairs, end, templates):
    new_pairs = {x: 0 for x in pairs.keys()}
    new_start = templates[start]
    new_pairs[new_start[1] + start[1]] += 1
    endish = templates[end]
    new_pairs[endish] += 1
    new_end = endish[1] + end[1]

    for pair in pairs:
        rep = templates[pair]
        num = pairs[pair]
        new_pairs[rep] += num
        new_pairs[rep[1] + pair[1]] += num

    return new_start, new_pairs, new_end

def count(poly: list):
    letters = {c for c in poly}
    counts = [poly.count(c) for c in letters]
    return min(counts), max(counts)

def p1(poly):
    #poly = ''.join(poly)
    for _ in range(10):
        print(_)
        print(poly)
        poly = step_v3(poly, templates)
    
    min, max = count(poly)
    print(max-min)
#p1(poly)

def p2(poly):
    start = poly[0:2]
    end = poly[-2:]
    pairs = {x: 0 for x in templates.keys()}

    sub_poly = poly[1:-1]
    for i in range(len(sub_poly)-1):
        pairs[sub_poly[i:i+2]] += 1

    def str_pairs(pairs):
        return [(x, pairs[x]) for x in pairs if pairs[x] > 0]
    
    def get_count(start, pairs, end):
        letters = {}
        for pair in pairs:
            num = pairs[pair]
            x, y = pair
            if x not in letters:
                letters[x] = 0
            if y not in letters:
                letters[y] = 0
            letters[x] += num
            letters[y] += num
        letters[start[1]] += 1
        letters[end[0]] += 1
        for letter in letters:
            letters[letter] /= 2
        letters[start[0]] += 1
        letters[end[1]] += 1
        #print(letters)
        min = None
        max = 0
        for num in letters.values():
            if min is None or num < min:
                min = num
            if num > max:
                max = num
        return min, max
    
    print(str_pairs(pairs))
    print(get_count(start, pairs, end))
    #breakpoint()
    t = time.time()
    for i in range(40):
        t2 = time.time()
        print(f'{i}: (last was {t2-t}s)')
        t = t2
        start, pairs, end = step_v3(start, pairs, end, templates)
        #print(f'start: {start}, pairs: {str_pairs(pairs)}, end: {end}')
        #print(get_count(start, pairs, end))
    
    min, max = get_count(start, pairs, end)
    print(max-min)
p2(poly)
