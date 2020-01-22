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

def get_path_length(board):
    path_length = 0
    for k in board:
        if board[k] == 'V':
            path_length = path_length + 1
    return path_length

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
            if board.get((x,y),None) == 'S':
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

def is_valid(position, board):
    tile = board.get((position[0], position[1]),None)
    if (tile != None and tile != '#' and tile != 'V'):
        return True

    return False

def find_path(position, board, min_path_length):
    if board.get((position[0],position[1]), None) == 'X':
        print(get_path_length(board))
        display_board(board)
        min_path_length = min(min_path_length, get_path_length(board))
        return min_path_length

    board[(position[0],position[1])] = 'V'
    # South
    if (is_valid((position[0] - 1, position[1]), board)):
        min_path_length = find_path((position[0] - 1, position[1]), board, min_path_length)

    # East
    if (is_valid((position[0], position[1] + 1), board)):
        min_path_length = find_path((position[0], position[1] + 1), board, min_path_length)

    # North
    if (is_valid((position[0] + 1, position[1]), board)):
        min_path_length = find_path((position[0] + 1, position[1]), board, min_path_length)

    # West
    if (is_valid((position[0], position[1] - 1), board)):
        min_path_length = find_path((position[0], position[1] - 1), board, min_path_length)

    # Unvisit the position
    board[(position[0],position[1])] = '.'
    return min_path_length

board = load_maze('./maze.txt')
display_board(board)
print('shortest {}'.format(find_path(get_start_position(board), board, sys.maxsize)))
display_board(board)
