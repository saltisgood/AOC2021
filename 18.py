from dataclasses import dataclass

with open('input-18.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]

@dataclass
class Int:
    value: int

    @property
    def magnitude(self):
        return self.value
    
    def __str__(self):
        return str(self.value)

@dataclass
class Pair:
    left: int # | Pair
    right: int # | Pair
    parent: None # Pair

    @property
    def magnitude(self):
        return 3 * self.left.magnitude + 2 * self.right.magnitude
    
    @property
    def parents(self):
        p = self.parent
        while p is not None:
            yield p
            p = self.parent
    
    def __str__(self):
        return f'[{str(self.left)},{str(self.right)}]'

def get_digits(s):
    digits = ''
    for i in range(len(s)):
        if str.isdigit(s[i]):
            digits = digits + s[i]
        else:
            break
    return digits
    
def parse_line(line):
    pair = Pair(None, None, None)
    i = 1
    while i < len(line) - 1:
        if str.isdigit(line[i]):
            digits = get_digits(line[i:])
            i += len(digits)
            val = int(digits)
            if pair.left is None:
                pair.left = Int(val)
            else:
                pair.right = Int(val)
        elif line[i] == ',':
            i += 1
        elif line[i] == '[':
            if pair.left is None:
                pair.left = Pair(None, None, pair)
                pair = pair.left
            else:
                pair.right = Pair(None, None, pair)
                pair = pair.right
            i += 1
        elif line[i] == ']':
            pair = pair.parent
            i += 1
    
    return pair

def explode(pair: Pair):
    p = pair.parent
    p2 = p
    p = pair.parent.left
    if type(p) is Int:
        p.value += pair.left.value
    else:
        while type(p) is not Int:
            p = p.right
        p.value += pair.left.value
    
    p = pair.parent.right
    if type(p) is Int:
        p.value += pair.right.value
    else:
        while type(p) is not Int:
            p = p.left
        p.value += pair.right.value
    
    p = pair.parent
    if p.left == pair:
        p.left = Int(0)
    else:
        p.right = Int(0)

def split(pair: Pair, left: bool):
    v = pair.left.value if left else pair.right.value
    r = l = int(v / 2)
    r += v % 2
    if left:
        pair.left = Pair(Int(l), Int(r), pair)
    else:
        pair.right = Pair(Int(l), Int(r), pair)

def reduce(pair: Pair):
    def add_to_left(p: Pair, v: int):
        while type(p) is not Int:
            p = p.left
        p.value += v
    
    def add_to_right(p: Pair, v: int):
        while type(p) is not Int:
            p = p.right
        p.value += v

    def check_explode(p: Pair, depth: int):
        if depth > 4:
            if type(p.left) is not Int or type(p.right) is not Int:
                raise Exception()
            assert type(p.left) is Int
            assert type(p.right) is Int
            par = p.parent
            if par.left == p:
                par.left = Int(0)
            else:
                par.right = Int(0)
            return p.left.value, p.right.value
        
        if type(p.left) is Pair:
            expl = check_explode(p.left, depth + 1)
            if expl:
                l, r = expl
                add_to_left(p.right, r)
                return l, 0
        if type(p.right) is Pair:
            expl = check_explode(p.right, depth + 1)
            if expl:
                l, r = expl
                add_to_right(p.left, l)
                return 0, r
    
    def check_split(p: Pair):
        if type(p.left) is Int and p.left.value >= 10:
            split(p, True)
            return True
        if type(p.left) is Pair and check_split(p.left):
            return True
        if type(p.right) is Int and p.right.value >= 10:
            split(p, False)
            return True
        if type(p.right) is Pair and check_split(p.right):
            return True
        return False
    
    if check_explode(pair, 1):
        return True
    return check_split(pair)

def add(left: Pair, right: Pair):
    pair = Pair(left, right, None)
    left.parent = pair
    right.parent = pair
    #print(str(pair))
    while reduce(pair):
        #print(str(pair))
        pass
    return pair

def p1(lines):
    pairs = [parse_line(line) for line in lines]
    result = pairs[0]
    for pair in pairs[1:]:
        print(f'   {result}\n+  {pair}')
        result = add(result, pair)
        print(f'=  {result}\n')
    
    print(str(result))
    print(result.magnitude)

#p1(lines)

def p2(lines):
    best = 0
    for linel in lines:
        for liner in lines:
            if linel == liner:
                continue
            mag = add(parse_line(linel), parse_line(liner)).magnitude
            if mag > best:
                best = mag
    print(best)
p2(lines)
