def get_co_ords(position, instruction):
    co_ords = []
    direction = instruction[0]
    magnitude = int(instruction[1:]) + 1
    for i in range(1, magnitude):
        if direction == 'R':
            co_ords.append((position[0],position[1]+i))
        elif direction == 'L':
            co_ords.append((position[0],position[1]-i))
        elif direction == 'U':
            co_ords.append((position[0]+i,position[1]))
        else: # D
            co_ords.append((position[0]-i,position[1]))

    return co_ords

def process_wire(wire):
    co_ords = [(0,0)]
    for instruction in wire:
        position = co_ords[-1]
        co_ords = co_ords + get_co_ords(position, instruction)

    return set(co_ords)

def manhatten_distance(point):
    return abs(point[0]) + abs(point[1])

def solve_problem1(wire1,wire2):
    w1 = process_wire(wire1)
    w2 = process_wire(wire2)
    crosses = (w1 & w2)
    crosses.remove((0,0))
    l = list(crosses)
    l.sort(key=manhatten_distance)
    print(l[0])
    print(manhatten_distance(l[0]))

wire1 = ['R75','D30','R83','U83','L12','D49','R71','U7','L72']
wire2 = ['U62','R66','U55','R34','D71','R55','D58','R83']

with open('./wire1.txt') as file:
    wire1 = file.read().strip().split(',')

with open('./wire2.txt') as file:
    wire2 = file.read().strip().split(',')

solve_problem1(wire1,wire2)
