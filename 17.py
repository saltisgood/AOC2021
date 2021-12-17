import re

with open('input-17.txt', 'r') as f:
    text = f.read().strip()

#text = 'target area: x=20..30, y=-10..-5'
REGEX = re.compile(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)')
match = REGEX.match(text)
assert match

x_start, x_end, y_start, y_end = (int(x) for x in match.groups())
print(f'{x_start}, {x_end}, {y_start}, {y_end}')

vel_vals = (-200, 200)

def in_axis_box(pos, start, end):
    return pos >= start and pos <= end

def in_box(x_pos, y_pos):
    return in_axis_box(x_pos, x_start, x_end) and in_axis_box(y_pos, y_start, y_end)

def past_y_box(pos, start):
    return pos < start

def past_box(x_pos, y_pos):
    return x_pos > x_end or past_y_box(y_pos, y_start)

def simulate_y(y_vel):
    y_pos = 0
    max_y = 0
    while True:
        y_pos += y_vel
        y_vel -= 1
        if y_pos > max_y:
            max_y = y_pos
        if in_axis_box(y_pos, y_start, y_end):
            return max_y
        elif past_y_box(y_pos, y_start):
            return None

def simulate(x_vel, y_vel):
    x_pos = y_pos = 0
    while True:
        x_pos += x_vel
        y_pos += y_vel
        if x_vel > 0:
            x_vel -= 1
        y_vel -= 1
        if in_box(x_pos, y_pos):
            return True
        elif past_box(x_pos, y_pos):
            return False

def p1():
    top_y = -10100000
    y_vel = 0
    #breakpoint()
    for vel_val in range(vel_vals[0], vel_vals[1]):
        y = simulate_y(vel_val)
        if y is not None and y > top_y:
            top_y = y
            y_vel = vel_val
    print(top_y)
    print(y_vel)
#p1()

def p2():
    found = set()
    for x_vel in range(vel_vals[0], vel_vals[1]):
        for y_vel in range(vel_vals[0], vel_vals[1]):
            if simulate(x_vel, y_vel):
                found.add((x_vel, y_vel))
    print(len(found))
p2()
