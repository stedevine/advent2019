from enum import Flag, auto

class ReadState(Flag):
    use_phase = auto()
    use_input = auto()
    need_input = auto()

def process_tape(tape, position, phase_setting, input, read_state):
    # -1 : use phase, 0 : use input 1: need more input
    #read_state = -1
    #position = 0
    while True:
        instruction = tape[position]
        # The rightmost 2 digits are the opcode
        # We can ignore the leading 0
        op_code = instruction % 100
        #print('position {} opcode {}'.format(position, op_code))
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
                if read_state == ReadState.use_phase:
                    tape[param_1] = phase_setting
                    read_state = ReadState.use_input
                elif read_state == ReadState.use_input:
                    tape[param_1] = input
                    read_state = ReadState.need_input
                else:
                    #print('need more input, output is {}'.format(output))
                    return (position,output)
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
            #print('halt {}'.format(output))
            return (None, output)

    return None


# Use the same computer with the same rules.
# The first time the program asks for input use the phase
# The next time the program asks for input use the input
# The third time the program asks - you will have to wait for input
# This comes from the output of the next program
def feedback_loop(program, phase):
    program_a = program.copy()
    program_b = program.copy()
    program_c = program.copy()
    program_d = program.copy()
    program_e = program.copy()

    position_a = 0
    position_b = 0
    position_c = 0
    position_d = 0
    position_e = 0

    output = 0
    position_a, output = process_tape(program_a, position_a, phase[0], output, ReadState.use_phase)
    position_b, output = process_tape(program_b, position_b, phase[1], output, ReadState.use_phase)
    position_c, output = process_tape(program_c, position_c, phase[2], output, ReadState.use_phase)
    position_d, output = process_tape(program_d, position_d, phase[3], output, ReadState.use_phase)
    position_e, output = process_tape(program_e, position_e, phase[4], output, ReadState.use_phase)
    # position_e will be set to None when the program halts
    while(position_e):
        position_a, output = process_tape(program_a, position_a, phase[0], output, ReadState.use_input)
        position_b, output = process_tape(program_b, position_b, phase[1], output, ReadState.use_input)
        position_c, output = process_tape(program_c, position_c, phase[2], output, ReadState.use_input)
        position_d, output = process_tape(program_d, position_d, phase[3], output, ReadState.use_input)
        position_e, output = process_tape(program_e, position_e, phase[4], output, ReadState.use_input)
        if not position_e:
            return output

# Generate the valid phases
# List of 5 digits of the value 5->9, no value may be used more than once
def phase_list_generator():
    phases = []
    for a in range(5,10):
      for b in range(5,10):
        for c in range(5,10):
          for d in range(5,10):
              for e in range(5,10):
                  phase = [a,b,c,d,e]
                  # No value may be used more than once
                  if (len(set(phase)) == 5):
                      phases.append([a,b,c,d,e])
    return phases

def get_max_output(program):
    max_ouput = 0
    for phase_list in phase_list_generator():
        output = feedback_loop(program, phase_list)
        max_ouput = max(output, max_ouput)
    return max_ouput


program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
print('test 1 : {}'.format(feedback_loop(program, [9,8,7,6,5])))

program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
print('test 2 : {}'.format(feedback_loop(program, [9,7,8,5,6])))

puzzle_input = [3,8,1001,8,10,8,105,1,0,0,21,34,43,60,81,94,175,256,337,418,99999,3,9,101,2,9,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,102,4,9,9,1001,9,4,9,102,3,9,9,4,9,99,3,9,102,4,9,9,1001,9,2,9,1002,9,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99]
print('solution 2 : {}'.format(get_max_output(puzzle_input)))
