import math
def get_line_of_sight(start_point, end_point):
    path = []
    # Total distance to see in each direction
    delta_x = end_point[0] - start_point[0]
    delta_y = end_point[1] - start_point[1]
    # Number of points between start and end
    number_of_points = math.gcd(delta_x, delta_y)
    # x and y distance between each point
    step_size_x = int(delta_x / number_of_points)
    step_size_y = int(delta_y / number_of_points)

    x = start_point[0]
    y = start_point[1]
    for step in range(0, number_of_points + 1):
        path.append((x,y))
        x = x + step_size_x
        y = y + step_size_y

    return path

def get_board(filename):
    board= []
    with open(filename) as file:
        for line in file:
            row = [c for c in line.strip()]
            board.append(row)

    return board

def get_asteroids(board):
    asteroids = []
    height = len(board)
    width = len(board[0])
    for y in range(0,height):
        for x in range(0,width):
            if board[y][x] == '#':
                asteroids.append((x,y))

    return asteroids

def is_visible(path, board):
    # Check all the positions on the path for asteroids
    # Not counting the origin or the target
    for position in path[1:-1]:
        if board[position[1]][position[0]] == '#':
            return False
    return True


# Given an asteroid (position)
# For every point on the board for which there is another asteroid
# Get the line of site
# If line of site is all . - can see asteroid, otherwise blocked


def get_max_number_visible_asteroids(asteroids,board):
    max_count = 0
    for i in range(0, len(asteroids)):
        source = asteroids[i]
        targets = asteroids.copy()
        del targets[i]
        count = 0
        for asteroid in targets:
            line_of_sight = get_line_of_sight(source, asteroid)
            if (is_visible(line_of_sight, board)):
                count = count + 1
        #print('# {} count {}'.format(source,count))
        max_count = max(count,max_count)
    return max_count

board = get_board('./test1.txt')
print(get_max_number_visible_asteroids(get_asteroids(board),board))
board = get_board('./test2.txt')
print(get_max_number_visible_asteroids(get_asteroids(board),board))
board = get_board('./test3.txt')
print(get_max_number_visible_asteroids(get_asteroids(board),board))
board = get_board('./test4.txt')
print(get_max_number_visible_asteroids(get_asteroids(board),board))
board = get_board('./input.txt')
print(get_max_number_visible_asteroids(get_asteroids(board),board))
