import sys

def load_maze(maze):
    with open(maze) as file:
        board = {}
        y = 0
        for line in file:
            x = 0
            for c in line.strip():
                board[(x,y)] = c
                x = x + 1
            y = y - 1
        return board

def display_board(board):
    max_x, min_x, max_y, min_y = get_range(board)
    for y in range(max_y,min_y -1 , -1):
        line = ''
        for x in range(min_x, max_x + 1):
            line += board.get((x,y),' ')
        print(line)
    print()

def get_range(board):
    max_x, max_y = -sys.maxsize - 1, -sys.maxsize - 1
    min_x, min_y = sys.maxsize, sys.maxsize
    for key in board:
        max_x = max(max_x, key[0])
        min_x = min(min_x, key[0])
        max_y = max(max_y, key[1])
        min_y = min(min_y, key[1])

    return max_x, min_x, max_y, min_y

def get_start_position(board):
    max_x, min_x, max_y, min_y = get_range(board)
    for y in range(max_y,min_y -1 , -1):
        for x in range(min_x, max_x + 1):
            if board[(x,y)] == 'S':
                return (x,y)

def get_neighbors(position):
    neighbors = []
    if board.get((position[0] + 1, position[1]),None) == '.':
        neighbors.append((position[0] + 1, position[1]))
    if board.get((position[0] - 1, position[1]),None) == '.':
        neighbors.append((position[0] - 1, position[1]))
    if board.get((position[0], position[1] + 1),None) == '.':
        neighbors.append((position[0], position[1] + 1))
    if board.get((position[0], position[1] - 1),None) == '.':
        neighbors.append((position[0], position[1] -1))

    return neighbors

def solve_maze(board):
    start_position = get_start_position(board)
    points = []
    points.insert(0,start_position)
    for i in range(0,100):
        p = points.pop()
        neighbors = get_neighbors(p)
        print(neighbors)
        if len(neighbors) == 0:
            board[points[0]] = 'V'
        else:
            points.insert(0,neighbors[0])






board = load_maze('./simple_maze.txt')
display_board(board)
solve_maze(board)
display_board(board)
