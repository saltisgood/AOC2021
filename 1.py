with open('input-1.txt', 'r') as f:
    lines = f.readlines()

prev = 9999999
increases = 0
for line in lines:
    current = int(line)
    if current > prev:
        increases += 1
    prev = current

print(increases)

num = len(lines)
increases = 0
prev = 9999999
for i in range(0, num - 2):
    current = sum(int(x) for x in lines[i:i+3])
    if current > prev:
        increases += 1
    prev = current
print(increases)