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
    # part 2 of the puzzle requires the asteriod
    best_asteriod = None
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
        if (count > max_count):
            max_count = count
            best_asteriod = source
    return (max_count,best_asteriod)

'''
print(get_max_number_visible_asteroids(get_asteroids(get_board('./test1.txt'))))
print(get_max_number_visible_asteroids(get_asteroids(get_board('./test2.txt'))))
print(get_max_number_visible_asteroids(get_asteroids(get_board('./test3.txt'))))
print(get_max_number_visible_asteroids(get_asteroids(get_board('./test4.txt'))))
'''
print(get_max_number_visible_asteroids(get_asteroids(get_board('./test6.txt'))))
print(get_max_number_visible_asteroids(get_asteroids(get_board('./input.txt'))))


def angle(origin, target):
    # Angle for right triangle is tan^-1(opposite/adjacent)
    delta_x = float(target[0] - origin[0])
    # increasing y moves a point DOWNWARDS
    delta_y = float(-(target[1] - origin[1]))
    #print('dx {} dy {}'.format(delta_x, delta_y))
    if (delta_x >= 0 and delta_y > 0):
        #print('top right')
        return 0 if delta_x == 0 else math.degrees(math.atan(delta_x/delta_y))
    if (delta_x >= 0 and delta_y <= 0):
        #print('bottom right')
        # angle is -ve
        return 90 if delta_y == 0 else 180 +  math.degrees(math.atan(delta_x/delta_y))
    if (delta_x <= 0 and delta_y <= 0):
        #print('bottom left')
        return 270 if delta_y == 0 else 180 + math.degrees(math.atan(delta_x/delta_y))
    #print('top left')
    # angle is -ve
    return 270 if delta_x == 0 else 360 +  math.degrees(math.atan(delta_x/delta_y))

def vaporize(origin, asteroids):
    targets = asteroids.copy()
    targets.remove(origin)
    # Order the list of asteroids by the angle they make with the origin
    ordered_asteroids = sorted(targets, key = lambda t:(angle(origin,t)))
    # For each asteroid, get the angle of the origin to the target
    angles_targets = list(map(lambda a: (angle(origin,a),a), ordered_asteroids))
    # Group the asteroids by angle
    # Asteroids at the same angle cannot be vaporized with the same shot
    asteroids_by_angle = {}
    for a, target in angles_targets:
        if a in asteroids_by_angle:
            asteroids_by_angle[a].append(target)
        else:
            asteroids_by_angle[a] = [target]

    # Iterate through the dictionary, pop out each value in the list
    count = 0
    vaporized = []
    while count < len(targets):
        for key in asteroids_by_angle:
            if (len(asteroids_by_angle[key])):
                a = asteroids_by_angle[key].pop(0)
                vaporized.append(a)
                count = count + 1
                #print('{} {}'.format(count, a))

    return vaporized


## Problem 2
# Get 200th asteroid
a200 = vaporize((11,13),get_asteroids(get_board('./test6.txt')))[199]
print(a200)
print(a200[0] * 100 + a200[1])

a200 = vaporize((22,25),get_asteroids(get_board('./input.txt')))[199]
print(a200)
print(a200[0] * 100 + a200[1])

#print(asteroids)
# Starting at (8,3) get the angle between the vertical line and the line that connects the origin to the target
'''
origin = (3,3)
print(angle(origin, (3,0)))
print(angle(origin, (4,1)))
print(angle(origin, (5,2)))
print(angle(origin, (6,3)))
print(angle(origin, (5,4)))
print(angle(origin, (4,8)))
print(angle(origin, (3,5)))
print(angle(origin, (2,5)))
print(angle(origin, (1,4)))
print(angle(origin, (1,3)))
print(angle(origin, (1,2)))
print(angle(origin, (2,1)))
'''
