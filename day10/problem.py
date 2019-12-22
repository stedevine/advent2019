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

def get_asteroids(board):
    asteroids = []
    height = len(board)
    width = len(board[0])
    for y in range(0,height):
        for x in range(0,width):
            if board[y][x] == '#':
                asteroids.append((x,y))

    return asteroids

def get_board(filename):
    board= []
    with open(filename) as file:
        for line in file:
            row = [c for c in line.strip()]
            board.append(row)

    return board


# Given an asteroid (position)
# For every point on the board for which there is another asteroid
# Get the line of site
# If line of site is all . - can see asteroid, otherwise blocked
def get_max_number_visible_asteroids(asteroids):
    max_count = 0
    for i in range(0, len(asteroids)):
        source = asteroids[i]
        targets = asteroids.copy()
        del targets[i]
        count = 0
        for target in targets:
            line_of_sight = get_line_of_sight(source, target)
            if not (set(line_of_sight[1:-1]) & set(asteroids)):
                count = count + 1
        max_count = max(count,max_count)
    return max_count

'''
print(get_max_number_visible_asteroids(get_asteroids(get_board('./test1.txt'))))
print(get_max_number_visible_asteroids(get_asteroids(get_board('./test2.txt'))))
print(get_max_number_visible_asteroids(get_asteroids(get_board('./test3.txt'))))
print(get_max_number_visible_asteroids(get_asteroids(get_board('./test4.txt'))))
print(get_max_number_visible_asteroids(get_asteroids(get_board('./input.txt'))))
'''

def angle(origin, target):
    # Angle for right triangle is tan^-1(opposite/adjacent)
    # The opposite and adjecent values depend on what quadrant the target is
    # in relative to the origin
    delta_x = target[0] - origin[0]
    print(delta_x)
    # increasing y moves a point DOWNWARDS
    delta_y = -(target[1] - origin[1])
    print(delta_y)
    if (delta_x >= 0 and delta_y >= 0):
        # top right
        return 0 if delta_y == 0 else math.degrees(math.atan(delta_x/delta_y))
    if (delta_x >= 0 and delta_y <= 0):
        # bottom right
        return 90 if delta_x == 0 else 90 + (-1) * math.degrees(math.atan(delta_y/delta_x))
    if (delta_x <= 0 and delta_y <= 0):
        # bottom left
        return 180 if delta_y == 0 else 180 + (-1) * math.degrees(math.atan(delta_x/delta_y))


    return None

## Problem 2
asteroids = get_asteroids(get_board('./test5.txt'))
print(asteroids)
# Starting at (8,3) get the angle between the vertical line and the line that connects the origin to the target
print(angle((2,3), (3,0)))
print(angle((2,3), (4,6)))
print(angle((2,3), (4,0`)))
