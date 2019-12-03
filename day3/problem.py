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

def process_wire(wire):
    # Build up a list of the points the wire passes through
    # Start at (0,0)
    points = [(0,0)]
    for instruction in wire:
        # Start at the last co-ordinate
        position = points[-1]
        points = points + get_co_ords(position, instruction)

    return co_ords

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

# Test input
wire1 = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
wire2 = ['U62','R66','U55','R34','D71','R55','D58','R83']
print('Test solution {}'.format(solve_problem1(wire1, wire2)))

# Problem input
with open('./wire1.txt') as file:
    wire1 = file.read().strip().split(',')

with open('./wire2.txt') as file:
    wire2 = file.read().strip().split(',')

print('Problem 1 solution {}'.format(solve_problem1(wire1, wire2)))
