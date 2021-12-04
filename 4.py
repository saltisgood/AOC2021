with open('input-4.txt', 'r') as f:
    lines = [l.strip() for l in f.readlines()]

class Cell:
    def __init__(self, val):
        self.val = val
        self.found = False

class Board:
    def __init__(self, lines):
        self.rows = []
        self.cols = []
        for l in lines:
            self.rows.append([Cell(x) for x in l.split(' ') if x])
        
        for i in range(5):
            self.cols.append([])
            for row in self.rows:
                self.cols[i].append(row[i])
    
    def check(self, nos):
        i = 0
        for no in nos:
            for row in self.rows:
                for cell in row:
                    if cell.val == no:
                        cell.found = True
        
            for row in self.rows:
                if self.check_row(row):
                    return i
            for col in self.cols:
                if self.check_row(col):
                    return i
            
            i += 1
        return None

    def check_row(self, row):
        for cell in row:
            if not cell.found:
                return False
        return True
    
    def score(self, last_num):
        sum = 0
        for row in self.rows:
            for cell in row:
                if not cell.found:
                    sum += int(cell.val)
        return sum * last_num

def p1(lines):
    drawn_nos = lines[0].split(',')

    lines = lines[2:]
    boards = []
    while lines:
        boards.append(Board(lines[:5]))
        lines = lines[6:]

    best_board = None
    best_score = 1000
    for board in boards:
        score = board.check(drawn_nos)
        if score and score < best_score:
            best_board = board
            best_score = score
    
    score = best_board.score(int(drawn_nos[best_score]))
    return score

def p2(lines):
    drawn_nos = lines[0].split(',')

    lines = lines[2:]
    boards = []
    while lines:
        boards.append(Board(lines[:5]))
        lines = lines[6:]

    worst_board = None
    worst_score = 0
    for board in boards:
        score = board.check(drawn_nos)
        if score and score > worst_score:
            worst_board = board
            worst_score = score
    
    score = worst_board.score(int(drawn_nos[worst_score]))
    return score

print(p1(lines))
print(p2(lines))