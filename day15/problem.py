import random
import sys
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
    input = 1
    repair_bot = RepairBot(input)
    output = None # One output per input
    tape_position = 0
    relative_base = 0
    out_count = 0
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
                out_count = out_count + 1
                output = tape[param_1]
                input = repair_bot.get_next_move(output)
                #sys.stdin.readline()
                if (out_count % 5000) == 0:
                    print('output count {}'.format(out_count))
                    repair_bot.display_maze()
                #print('output {} input {}'.format(output,input))
                if output == 2:
                    print('Found the O2 pump')
                    repair_bot.display_maze()
                    return repair_bot
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
            print('This program is supposed to run forever :(')
            return None

    return None

class RepairBot:
    def __init__(self, input):
        self.position = (0,0)
        self.board = {}
        self.board[self.position] = 'S'
        self.move_direction = input

    def get_next_move(self, result):
        if result == 0: # wall
            self.board[self.get_new_position(self.position, self.move_direction)] = '#'
        elif result == 1: # moved successfully
            self.position = self.get_new_position(self.position, self.move_direction)
            if (self.position != (0,0)):
                self.board[self.position] = '.'
        else: # result = 2
            self.board[self.get_new_position(self.position, self.move_direction)] = 'X'

        # Move in a random direction (there's probably a quicker way to do this.)
        directions = [1,2,3,4]
        directions.remove(self.move_direction)
        self.move_direction = random.sample(directions,1)[0]
        return self.move_direction


    def get_new_position(self, position, direction):
        if direction == 1: # North
            return (position[0], position[1] + 1)
        if direction == 2: # South
            return (position[0], position[1] - 1)
        if direction == 3: # West
            return (position[0] - 1, position[1])
        # East
        return (position[0] + 1, position[1])

    def display_maze(self):
        max_x, max_y = -sys.maxsize - 1, -sys.maxsize - 1
        min_x, min_y = sys.maxsize, sys.maxsize
        for key in self.board:
            max_x = max(max_x, key[0])
            min_x = min(min_x, key[0])
            max_y = max(max_y, key[1])
            min_y = min(min_y, key[1])

        #print('max x min x {}  {}'.format(max_x, min_x))
        #print('max y min y {}  {}'.format(max_y, min_y))
        for y in range(max_y,min_y -1 , -1):
            line = ''
            for x in range(min_x, max_x + 1):
                line += self.board.get((x,y),' ')
            print(line)
        print()

    def get_range(self):
        max_x, max_y = -sys.maxsize - 1, -sys.maxsize - 1
        min_x, min_y = sys.maxsize, sys.maxsize
        for key in self.board:
            max_x = max(max_x, key[0])
            min_x = min(min_x, key[0])
            max_y = max(max_y, key[1])
            min_y = min(min_y, key[1])

        return max_x, min_x, max_y, min_y

    def get_start_position(self):
        max_x, min_x, max_y, min_y = self.get_range()
        for y in range(max_y, min_y -1, -1):
            for x in range(min_x, max_x + 1):
                if self.board.get((x, y), None) == 'S':
                    return(x, y)

    def find_path(self, position, min_path_length):
        if self.board.get((position[0], position[1]), None) == 'X':
            print('path length {}'.format(self.get_path_length()))
            self.display_maze()
            min_path_length = min(min_path_length, self.get_path_length())
            return min_path_length

        self.board[(position[0],position[1])] = 'V'
        # South
        if (self.is_valid((position[0] - 1, position[1]))):
            min_path_length = self.find_path((position[0] - 1, position[1]), min_path_length)

        # East
        if (self.is_valid((position[0], position[1] + 1))):
            min_path_length = self.find_path((position[0], position[1] + 1), min_path_length)

        # North
        if (self.is_valid((position[0] + 1, position[1]))):
            min_path_length = self.find_path((position[0] + 1, position[1]), min_path_length)

        # West
        if (self.is_valid((position[0], position[1] - 1))):
            min_path_length = self.find_path((position[0], position[1] - 1), min_path_length)

        # Unvisit the position
        self.board[(position[0],position[1])] = '.'
        return min_path_length

    def get_path_length(self):
        path_length = 0
        for k in self.board:
            if self.board[k] == 'V':
                path_length = path_length + 1
        return path_length

    def is_valid(self, position):
        tile = self.board.get((position[0], position[1]),None)
        if (tile != None and tile != '#' and tile != 'V'):
            return True

        return False



tape = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1001,1034,0,1039,1002,1036,1,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1106,0,124,1001,1034,0,1039,102,1,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1105,1,124,1001,1034,-1,1039,1008,1036,0,1041,102,1,1035,1040,1002,1038,1,1043,101,0,1037,1042,1105,1,124,1001,1034,1,1039,1008,1036,0,1041,102,1,1035,1040,1001,1038,0,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,33,1032,1006,1032,165,1008,1040,33,1032,1006,1032,165,1101,0,2,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1102,1,1,1044,1105,1,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,42,1044,1106,0,224,1102,0,1,1044,1106,0,224,1006,1044,247,1001,1039,0,1034,1001,1040,0,1035,1001,1041,0,1036,1001,1043,0,1038,102,1,1042,1037,4,1044,1106,0,0,6,28,51,33,63,27,52,11,53,13,96,8,87,11,23,65,43,11,13,9,37,66,68,40,19,41,6,90,28,19,38,86,38,22,7,44,36,23,17,1,16,54,36,74,14,79,2,14,83,10,38,19,62,66,27,56,33,52,47,98,41,39,77,83,48,29,49,15,80,59,9,72,79,55,24,66,50,24,27,56,37,41,13,72,35,13,64,70,5,66,78,37,78,24,43,93,22,41,30,58,14,45,6,27,44,48,40,52,31,12,3,72,7,14,59,35,17,63,34,79,93,17,54,98,35,21,91,25,32,77,10,31,88,17,35,79,96,11,83,15,48,9,19,64,24,65,86,32,71,22,88,55,31,18,88,68,34,40,94,1,71,24,40,44,28,43,4,98,21,80,17,53,2,94,6,43,59,23,66,63,12,30,45,39,93,41,85,43,51,18,99,59,86,40,36,26,94,33,41,28,66,79,81,11,61,46,32,72,71,47,39,22,69,60,36,50,12,44,28,41,79,17,6,74,8,56,39,33,67,23,20,51,12,7,26,57,1,92,80,11,52,19,5,54,13,41,56,37,22,57,43,18,97,27,83,30,3,77,85,66,64,17,99,27,25,95,40,81,97,13,35,46,14,25,63,36,72,87,20,96,29,2,69,90,27,27,91,52,14,14,73,55,4,73,19,85,39,84,23,23,90,40,5,88,53,77,8,92,11,82,66,6,27,84,53,38,93,34,37,58,20,43,25,73,78,30,17,92,54,38,26,67,16,30,28,79,77,26,3,15,82,59,34,34,18,44,34,33,83,35,90,31,58,44,16,18,65,8,70,90,32,46,21,41,54,39,43,93,23,99,11,43,50,98,33,34,53,54,53,16,39,88,53,36,69,85,26,44,38,62,98,6,79,26,35,49,67,22,11,74,35,80,4,50,18,54,4,10,4,58,4,46,20,15,77,73,11,41,58,85,39,87,37,73,36,36,67,28,12,17,34,53,38,89,96,34,39,67,64,33,81,37,74,88,20,84,94,53,39,57,73,13,76,1,35,14,73,29,29,23,73,52,16,85,87,33,48,13,2,93,78,7,17,60,49,13,36,89,40,25,44,55,26,81,37,31,84,31,62,2,66,77,23,88,11,81,9,63,46,19,35,54,17,85,24,1,86,28,72,1,1,61,27,38,81,8,67,82,3,11,77,35,62,83,20,28,61,37,37,92,22,72,76,37,52,17,62,68,38,53,2,57,82,67,25,11,59,3,49,97,1,40,91,75,7,85,98,33,90,1,37,57,14,34,67,65,20,85,10,18,86,20,52,84,24,20,70,10,64,16,64,2,15,85,36,28,7,87,47,44,9,29,54,83,28,37,81,68,18,12,80,26,98,97,25,86,69,39,70,22,23,72,15,56,94,27,14,13,8,50,73,90,24,95,14,41,57,22,67,25,80,46,39,84,80,19,22,63,53,45,62,21,84,36,69,41,44,96,38,92,21,23,64,35,11,75,57,88,6,7,90,10,36,19,68,78,23,62,34,49,4,80,38,2,70,48,39,55,20,22,39,8,90,64,38,39,47,41,63,72,5,10,72,88,35,50,5,66,30,80,74,23,97,39,98,19,17,85,38,34,62,37,25,58,15,93,37,13,71,72,72,4,84,40,92,61,88,9,7,62,59,87,17,36,39,43,21,11,16,58,16,58,20,66,18,83,33,66,62,90,32,74,15,58,62,43,16,66,22,90,2,68,30,54,18,59,22,50,12,60,35,66,77,51,36,64,89,82,21,85,0,0,21,21,1,10,1,0,0,0,0,0,0]
tape = tape + [0] * 1000

r = process_tape(tape)
r.display_maze()
print('shortest {}'.format(r.find_path(r.get_start_position(), sys.maxsize)))
