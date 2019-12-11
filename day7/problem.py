import math
def process_tape(tape, phase_setting, input):
    use_phase_setting = True
    position = 0
    while True:
        instruction = tape[position]
        # The rightmost 2 digits are the opcode
        # We can ignore the leading 0
        op_code = instruction % 100
        # print('position {} opcode {}'.format(position, op_code))
        param_mode_1 = int((instruction % 1000) / 100)
        param_mode_2 = int((instruction % 10000) / 1000)
        param_mode_3 = int((instruction % 100000) / 10000)
        #print('{} {} {}'.format(param_mode_1, param_mode_2, param_mode_3))

        if op_code in [1,2,7,8]:
            param_1 = tape[tape[position + 1]] if param_mode_1 == 0 else tape[position + 1]
            param_2 = tape[tape[position + 2]] if param_mode_2 == 0 else tape[position + 2]
            param_3 = tape[position + 3] if param_mode_3 == 0 else position + 3
            if op_code == 1:
                tape[param_3] = param_1 + param_2
            elif op_code == 2:
                tape[param_3] = param_1 * param_2
            elif op_code == 7:
                tape[param_3] = 1 if (param_1 < param_2) else 0
            elif op_code == 8:
                tape[param_3] = 1 if (param_1 == param_2) else 0

            position = position + 4


        elif op_code in [3,4]:
            param_1 = tape[position + 1] if param_mode_1 == 0 else position + 1
            if op_code == 3:
                # The first input instruction is the phase setting
                # for subsequent input instructions use the 'input' value
                tape[param_1] = phase_setting if use_phase_setting else input
                if use_phase_setting:
                    use_phase_setting = False
            elif op_code == 4:
                output = tape[param_1]
            position = position + 2

        elif op_code in [5,6]:
            param_1 = tape[tape[position + 1]] if param_mode_1 == 0 else tape[position + 1]
            param_2 = tape[tape[position + 2]] if param_mode_2 == 0 else tape[position + 2]
            if op_code == 5:
                position = param_2 if param_1 != 0 else position + 3
            if op_code == 6:
                position = param_2 if param_1 == 0 else position + 3

        elif op_code == 99:
            return output

    return None

# Generate the valid phases
# List of 5 digits of the value 0->4, no value may be used more than once
def phase_list_generator():
    phases = []
    for a in range(0,5):
      for b in range(0,5):
        for c in range(0,5):
          for d in range(0,5):
              for e in range(0,5):
                  phase = [a,b,c,d,e]
                  # No value may be used more than once
                  if (len(set(phase)) == 5):
                      phases.append([a,b,c,d,e])
    return phases



def get_max_output(program):
    max_ouput = 0
    for phase_list in phase_list_generator():
        output = do_five_amps(program, phase_list)
        max_ouput = max(output, max_ouput)
    return max_ouput

def do_five_amps(program, phase_list):
    input_signal = 0
    for amp in (0,1,2,3,4):
        input_signal = process_tape(program.copy(), phase_list[amp], input_signal)

    return input_signal

# Tests
program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
print('test 1 : {}'.format(get_max_output(program)))
program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
print('test 2 : {}'.format(get_max_output(program)))
program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
print('test 3 : {}'.format(get_max_output(program)))

puzzle_input = [3,8,1001,8,10,8,105,1,0,0,21,34,43,60,81,94,175,256,337,418,99999,3,9,101,2,9,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,102,4,9,9,1001,9,4,9,102,3,9,9,4,9,99,3,9,102,4,9,9,1001,9,2,9,1002,9,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99]
print('soluation 1 : {}'.format(get_max_output(puzzle_input)))
