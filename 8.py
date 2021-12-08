inputs = []

with open('input-8.txt', 'r') as f:
    for line in f.readlines():
        digits, output = line.split('|')
        digits = digits.strip()
        output = output.strip()
        inputs.append((digits.split(' '), output.split(' ')))

#print(inputs)

def p1():
    unique_digits = 0

    for _, output in inputs:
        for digit in output:
            if len(digit) in [2, 3, 4, 7]: # 1, 7, 4, 8
                unique_digits += 1

    #print(unique_digits)

p1()

def get_n(digits, n):
    m = {1: 2, 4: 4, 7: 3, 8: 7}
    n = m[n]
    for digit in digits:
        if len(digit) == n:
            return digit

def get_ns(digits, n):
    return [digit for digit in digits if len(digit) == n]

def do_check(digits, one, seven, four, eight):
    top = seven ^ one
    d_690 = get_ns(digits, 6)
    d_235 = get_ns(digits, 5)
    for zero in d_690:
        mid = eight ^ set(zero)
        top_left = four ^ (one | mid)
        if len(top_left) > 1:
            continue
        almost_three = seven | mid
        for three in d_235:
            three = set(three)
            bottom = three ^ almost_three
            if len(bottom) == 1:
                break
        bottom_left = eight ^ (four | top | bottom)
        nine = eight ^ bottom_left
        six = [set(x) for x in d_690 if x != zero and set(x) != nine][0]
        top_right = eight ^ six
        bottom_right = one ^ top_right
        two = eight ^ (top_left | bottom_right)
        five = eight ^ (bottom_left | top_right)
        return two, three, five, six, nine, set(zero)

def p2():
    sums = 0
    for digits, output in inputs:
        one = set(get_n(digits, 1))
        seven = set(get_n(digits, 7))
        four = set(get_n(digits, 4))
        eight = set(get_n(digits, 8))
        two, three, five, six, nine, zero = do_check(digits, one, seven, four, eight)
        mapping = [
            (zero, 0),
            (one, 1),
            (two, 2),
            (three, 3),
            (four, 4),
            (five, 5),
            (six, 6),
            (seven, 7),
            (eight, 8),
            (nine, 9)
                ]

        result = []
        for o in output:
            o = set(o)
            for st, num in mapping:
                if o == st:
                    result.append(num)
                    break
        result = int(''.join(str(x) for x in result))
        sums += result

    print(sums)

p2()
