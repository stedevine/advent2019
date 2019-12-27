def get_param(tape, tape_position, param_mode, relative_base):
    return tape[get_tape_position(tape, tape_position, param_mode, relative_base)]

def get_tape_position(tape, tape_position, param_mode, relative_base):
    # position mode
    if param_mode == 0:
        return tape[tape_position]
    # immediate mode
    if param_mode == 1:
        return tape_position
    # relative mode
    return tape[tape_position] + relative_base

def get_param_modes(instruction):
    return (int((instruction % 1000) / 100),\
            int((instruction % 10000) / 1000), \
            int((instruction % 100000) / 10000))

def process_tape(tape):
    robot = Hullbot()
    input = 0
    outputs = []                # For each input the program will produce 2 outputs for the robot
    tape_position = 0
    relative_base = 0

    while True:
        instruction = tape[tape_position]
        param_mode_1, param_mode_2, param_mode_3 = get_param_modes(instruction)
        # The rightmost 2 digits are the opcode
        # We can ignore the leading 0
        op_code = instruction % 100

        #print('tape_position {} opcode {}'.format(tape_position, op_code))
        #print('{} {} {}'.format(param_mode_1, param_mode_2, param_mode_3))

        if op_code in [1,2,7,8]:
            param_1 = get_param(tape, tape_position + 1, param_mode_1, relative_base)
            param_2 = get_param(tape, tape_position + 2, param_mode_2, relative_base)
            param_3 = get_tape_position(tape, tape_position + 3, param_mode_3, relative_base)
            # Addition operation
            if op_code == 1:
                #print('address {} {} -> {}'.format(param_3, tape[param_3], param_1 + param_2))
                tape[param_3] = param_1 + param_2
            # Multiply operation
            elif op_code == 2:
                tape[param_3] = param_1 * param_2
            # Less than
            elif op_code == 7:
                tape[param_3] = 1 if (param_1 < param_2) else 0
            # Equal
            elif op_code == 8:
                tape[param_3] = 1 if (param_1 == param_2) else 0
            tape_position = tape_position + 4

        elif op_code in [3,4,9]:
            param_1 = get_tape_position(tape, tape_position + 1, param_mode_1, relative_base)
            # Input
            if op_code == 3:
                tape[param_1] = input
            # Output
            elif op_code == 4:
                outputs.append(tape[param_1])
                # When we have collected 2 outputs, send these values to the robot
                # To get the new input.
                if (len(outputs) == 2):
                    input = robot.process_instructions(outputs)
                    outputs = []
            # Set relative base
            else: # op_code == 9
                relative_base = relative_base + tape[param_1]
            tape_position = tape_position + 2

        elif op_code in [5,6]:
            param_1 = get_param(tape, tape_position + 1, param_mode_1, relative_base)
            param_2 = get_param(tape, tape_position + 2, param_mode_2, relative_base)
            # True
            if op_code == 5:
                tape_position = param_2 if param_1 != 0 else tape_position + 3
            # False
            if op_code == 6:
                tape_position = param_2 if param_1 == 0 else tape_position + 3

        elif op_code == 99:
            print('hullbot painted {}'.format(robot.get_squares_visited()))
            return None

    return None

class Hullbot:
    def __init__(self):
        self.position = (0,0)
        self.hull = {}
        self.directions = ['N','E', 'S', 'W']
        self.direction_index = 0  # initially pointing up
        print('initialzed!')

    def process_instructions(self, instructions):
        self.paint(instructions)
        self.move(instructions)
        camera = self.hull.get(self.position,0)
        #print('new position {} camera {} hull {}'.format(self.position, camera, self.hull))
        return camera

    def paint(self, instructions):
        self.hull[self.position] = instructions[0]

    def move(self, instructions):
        direction = self.get_direction(instructions)
        #print('position {} direction {}'.format(self.position, direction))
        if direction == 'N':
            self.position = (self.position[0],      self.position[1] + 1)
        elif direction == 'E':
            self.position = (self.position[0] + 1,  self.position[1])
        elif direction == 'S':
            self.position = (self.position[0],      self.position[1] - 1)
        else:
            # W
            self.position = (self.position[0] - 1,  self.position[1])

    def get_direction(self, instructions):
        if instructions[1] == 1:
            # Turn right
            self.direction_index = (self.direction_index + 1) % 4
        else:
            # Turn left
            if self.direction_index == 0:
                self.direction_index = 3
            else:
                self.direction_index = self.direction_index - 1
        return  self.directions[self.direction_index]

    def get_squares_visited(self):
        return len(self.hull)

'''
#Robot tests
robot = Hullbot()
print(robot.get_direction((0,0)))
print(robot.get_direction((0,0)))
print(robot.get_direction((0,0)))
print(robot.get_direction((0,0)))
print(robot.get_direction((0,1)))
print(robot.get_direction((0,1)))
print(robot.get_direction((0,1)))
print(robot.get_direction((0,1)))

print(robot.process_instructions((1,0)))
print(robot.process_instructions((0,0)))
print(robot.process_instructions((1,0)))
print(robot.process_instructions((1,0)))

print(robot.process_instructions((0,1)))
print(robot.process_instructions((1,0)))
print(robot.process_instructions((1,0)))
'''

tape = [3,8,1005,8,337,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,29,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,102,1,8,51,1,1008,18,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,102,1,8,76,1006,0,55,1,1108,6,10,1,108,15,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,110,2,1101,13,10,1,101,10,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,139,1006,0,74,2,107,14,10,1,3,1,10,2,1104,19,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,177,2,1108,18,10,2,1108,3,10,1,109,7,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,210,1,1101,1,10,1,1007,14,10,2,1104,20,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,244,1,101,3,10,1006,0,31,1006,0,98,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1002,8,1,277,1006,0,96,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,302,1,3,6,10,1006,0,48,2,101,13,10,2,2,9,10,101,1,9,9,1007,9,1073,10,1005,10,15,99,109,659,104,0,104,1,21101,937108976384,0,1,21102,354,1,0,1105,1,458,21102,1,665750077852,1,21101,0,365,0,1105,1,458,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,21478178856,0,1,21101,412,0,0,1105,1,458,21102,3425701031,1,1,21102,1,423,0,1106,0,458,3,10,104,0,104,0,3,10,104,0,104,0,21102,984458351460,1,1,21102,1,446,0,1105,1,458,21101,0,988220908388,1,21101,457,0,0,1105,1,458,99,109,2,22101,0,-1,1,21102,1,40,2,21101,489,0,3,21101,479,0,0,1105,1,522,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,484,485,500,4,0,1001,484,1,484,108,4,484,10,1006,10,516,1102,0,1,484,109,-2,2105,1,0,0,109,4,1201,-1,0,521,1207,-3,0,10,1006,10,539,21102,1,0,-3,21201,-3,0,1,21202,-2,1,2,21101,1,0,3,21101,558,0,0,1105,1,563,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,586,2207,-4,-2,10,1006,10,586,22102,1,-4,-4,1106,0,654,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21102,1,605,0,1106,0,563,21201,1,0,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,624,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,646,22101,0,-1,1,21102,646,1,0,106,0,521,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]
tape = tape + [0] * 1000
process_tape(tape)
