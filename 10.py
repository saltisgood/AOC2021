with open('input-10.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]

points_map = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

points_map_p2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

opens = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}
closes = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}

def p1():
    points = 0

    stack = []
    for line in lines:
        line_stack = stack[:]
        invalid = None
        for c in line:
            if c in opens:
                line_stack.append(c)
            else:
                expect = line_stack.pop()
                if closes[c] != expect:
                    invalid = c
                    break
                
        if invalid:
            points += points_map[invalid]
        else:
            stack = line_stack

    print(points)
p1()

def p2():
    points = []

    for line in lines:
        line_stack = []
        invalid = None
        for c in line:
            if c in opens:
                line_stack.append(c)
            else:
                expect = line_stack.pop()
                if closes[c] != expect:
                    invalid = c
                    break
                
        if not invalid:
            line_points = 0
            for c in reversed(line_stack):
                tag = opens[c]
                line_points = line_points * 5 + points_map_p2[tag]
            points.append(line_points)                    

    points = sorted(points)
    print(points[int(len(points)/2)])
p2()
