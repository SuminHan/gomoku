import numpy as np
import random
import os.path

sz = 19
dictionary = {} # dictionary[my_id] = (parents, [child_list], win, total)
# Load
if os.path.isfile('my_file.npy'):
    dictionary = np.load('my_file.npy').item()

if not dictionary:
    for i in range(0, sz*sz):
        dictionary[i] = [-1, [], 0, 0]

board = np.zeros((sz, sz), dtype='int')

def is_in(y, x):
    return 0 <= y < sz and 0 <= x < sz

def is_golden_possible(target, board, dir, color):
    x, y = target
    dx, dy = dir
    if is_in(board, x + dx * 3, y + dy * 3)\
        and board[x + dx][y + dy] == color\
        and board[x + dx * 2][y + dy * 2] == color\
        and board[x + dx * 3][y + dy * 3] < 0:
        return True
    if is_in(board, x + dx * 4, y + dy * 4)\
        and board[x + dx][y + dy] < 0\
        and board[x + dx * 2][y + dy * 2] == color\
        and board[x + dx * 3][y + dy * 3] == color\
        and board[x + dx * 4][y + dy * 4] == ' ':
        return True
    if is_in(board, x + dx * 4, y + dy * 4)\
        and board[x + dx][y + dy] == color\
        and board[x + dx * 2][y + dy * 2] < 0\
        and board[x + dx * 3][y + dy * 3] == color\
        and board[x + dx * 4][y + dy * 4] < 0:
        return True
    return False

def march( y, x, dy, dx, length):
    '''
    go as far as posible in direction dy, dx for length
    '''
    yf = y + length * dy
    xf = x + length * dx

    while not is_in(yf, xf):
        yf -= dy
        xf -= dx

    return yf, xf

def possible_moves(color):
    '''
    return a list of possible coordinates at the boundary of existing stones off-set by 3 units
    '''
    taken = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    cord = {}
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != ' ':
                taken.append((i, j))

    for direction in directions:
        dy, dx = direction
        for coord in taken:
            y, x = coord
            for length in [1, 2, 3, 4]:
                move = march(y, x, dy, dx, length)
                if move not in taken and move not in cord:
                    is_golden = False
                    for odirection in directions:
                        if is_golden_possible(move, board, direction, color) \
                            and is_golden_possible(move, board, odirection, color):
                            is_golden = True
                            break
                    if not is_golden:
                        cord[move] = False

    return cord

def is_empty():
    return board == [[-1] * sz] * sz


def next_move(player):
    return (int(sz * random.random()), int(sz * random.random()))

def start_game():
    board[::] = -1

    player = True
    (xi, yi) = next_move(player)
    parent = yi*sz + xi
    last = -1
    while True:
        player = not player
        (x, y) = next_move(player)

        last = new_idx = len(dictionary)
        dictionary[new_idx] = [parent, [], 0, 0]
        print(last)
        dictionary[parent][1].append(new_idx)
        parent = new_idx
        break

        #game may over now...
    while last > 0:
        dictionary[last][2] += 1
        dictionary[last][3] += 1
        last = dictionary[last][0]
        break



start_game()

print(is_empty())

# Save
dictionary = {}
np.save('my_file.npy', dictionary)
