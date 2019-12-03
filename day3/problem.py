def get_co_ords(position, instruction):
    # Get a list of the points of the positions
    # The wire has passed through, starting at the input position
    # given the Right/Left/Up/Down instruction
    points = []
    direction = instruction[0]
    magnitude = int(instruction[1:])
    for i in range(1, magnitude + 1):
        if direction == 'R':
            points.append((position[0],position[1]+i))
        elif direction == 'L':
            points.append((position[0],position[1]-i))
        elif direction == 'U':
            points.append((position[0]+i,position[1]))
        else: # D
            points.append((position[0]-i,position[1]))

    return points

def get_wire_states(initial_state, instruction):
    # wire_state is the point and the distance travelled to reach that point:
    # (x,y, distance)
    wire_states = []
    direction = instruction[0]

    magnitude = int(instruction[1:])
    for i in range(1, magnitude + 1):
        if direction == 'R':
            wire_states.append((initial_state[0], initial_state[1]+i, initial_state[2]+i))
        elif direction == 'L':
            wire_states.append((initial_state[0], initial_state[1]-i, initial_state[2]+i))
        elif direction == 'U':
            wire_states.append((initial_state[0]+i, initial_state[1], initial_state[2]+i))
        else: # D
            wire_states.append((initial_state[0]-i, initial_state[1], initial_state[2]+i))

    return wire_states

def get_shortest_for_common_points(wire_states_1, wire_states_2):
    distances = []
    wire_1_points = list(map(lambda x: (x[0],x[1]), wire_states_1))
    wire_2_points = list(map(lambda x: (x[0],x[1]), wire_states_2))
    common_points = (set(wire_1_points) & set(wire_2_points))
    for common_point in common_points:
        # Get the first time each wire entered the location where they cross
        wire_cross_state_1 = wire_states_1[wire_1_points.index(common_point)]
        wire_cross_state_2 = wire_states_2[wire_2_points.index(common_point)]
        distances.append(wire_cross_state_1[2] + wire_cross_state_2[2])

    distances.sort()
    return distances[1]

def process_wire(wire):
    # Build up a list of the points the wire passes through
    # Start at (0,0)
    points = [(0,0)]
    for instruction in wire:
        # Start at the last co-ordinate
        position = points[-1]
        points = points + get_co_ords(position, instruction)

    return points

def get_all_wire_states(wire):
    wire_states = [(0,0,0)]
    for instruction in wire:
        # Start at last state
        wire_state = wire_states[-1]
        wire_states = wire_states + get_wire_states(wire_state, instruction)

    return wire_states

def manhattan_distance(point):
    return abs(point[0]) + abs(point[1])

def solve_problem1(wire1, wire2):
    # Given two wires what is the Manhattan distance from
    # where they start to the closest point where they cross?
    # Get a list of the points that each wire passes through
    w1 = process_wire(wire1)
    w2 = process_wire(wire2)
    # Get the common points (positions where the wires cross)
    crosses = (set(w1) & set(w2))
    # Put them in a list and sort the points by Manhattan distance
    l = list(crosses)
    l.sort(key=manhattan_distance)
    # Return the smallest value (ignoring (0,0))
    return manhattan_distance(l[1])

def solve_problem2(wire1, wire2):
    # Given two wires what is the fewest combined steps the
    # wires take to reach an intersection?
    distances = []
    wire_states_1 = get_all_wire_states(wire1)
    wire_states_2 = get_all_wire_states(wire2)
    wire_1_points = list(map(lambda x: (x[0],x[1]), wire_states_1))
    wire_2_points = list(map(lambda x: (x[0],x[1]), wire_states_2))
    common_points = (set(wire_1_points) & set(wire_2_points))
    for common_point in common_points:
        # Get the first time each wire entered the location where they cross
        wire_cross_state_1 = wire_states_1[wire_1_points.index(common_point)]
        wire_cross_state_2 = wire_states_2[wire_2_points.index(common_point)]
        distances.append(wire_cross_state_1[2] + wire_cross_state_2[2])

    distances.sort()
    # return the shortest distance (except for where the wires cross at the origin)
    return distances[1]
    #print(get_shortest_for_common_points(get_all_wire_states(wire1), get_all_wire_states(wire2)))

# Test input
wire1 = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
wire2 = ['U62','R66','U55','R34','D71','R55','D58','R83']
print('Test Problem 1 solution {}'.format(solve_problem1(wire1, wire2)))
print('Test Problem 2 solution {}'.format(solve_problem2(wire1, wire2)))

# Problem input
with open('./wire1.txt') as file:
    wire1 = file.read().strip().split(',')

with open('./wire2.txt') as file:
    wire2 = file.read().strip().split(',')

print('Full Problem 1 solution {}'.format(solve_problem1(wire1, wire2)))
print('Full Problem 2 solution {}'.format(solve_problem2(wire1, wire2)))
