with open('input-2.txt', 'r') as f:
    lines = f.readlines()

def p1():
    depth = 0
    pos = 0

    for line in lines:
        order, num = line.split()
        if order == 'forward':
            pos += int(num)
        elif order == 'down':
            depth += int(num)
        elif order == 'up':
            depth -= int(num)
        else:
            raise Exception()

    print(depth * pos)

def p2():
    depth = 0
    pos = 0
    aim = 0

    for line in lines:
        order, num = line.split()
        num = int(num)
        if order == 'forward':
            pos += num
            depth += aim * num
        elif order == 'down':
            aim += num
        elif order == 'up':
            aim -= num
        else:
            raise Exception()
    
    print(depth * pos)

p1()
p2()