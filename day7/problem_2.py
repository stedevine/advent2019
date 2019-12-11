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

def process_tape(tape, position, phase_setting, input, read_state):
    # -1 : use phase, 0 : use input 1: need more input
    #read_state = -1
    #position = 0
    while True:
        instruction = tape[position]
        # The rightmost 2 digits are the opcode
        # We can ignore the leading 0
        op_code = instruction % 100
        print('position {} opcode {}'.format(position, op_code))
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
                if read_state == -1:
                    tape[param_1] = phase_setting
                    read_state = read_state + 1
                elif read_state == 0:
                    tape[param_1] = input
                    read_state = read_state + 1
                else:
                    print('need more input, output is {}'.format(output))
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
            print('halt {}'.format(output))
            return (None, output)

    return None


# Use the same computer with the same rules.
# The first time the program asks for input use the phase
# The next time the program asks for input use the input
# The third time the program asks - you will have to wait for input
# This comes from the output of the next program
def feed3(program, phase):
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
    read_state = -1
    position_a, output = process_tape(program_a, position_a, phase[0], output, read_state)
    position_b, output = process_tape(program_b, position_b, phase[1], output, read_state)
    position_c, output = process_tape(program_c, position_c, phase[2], output, read_state)
    position_d, output = process_tape(program_d, position_d, phase[3], output, read_state)
    position_e, output = process_tape(program_e, position_e, phase[4], output, read_state)
    read_state = 0
    while(True):
        position_a, output = process_tape(program_a, position_a, phase[0], output, read_state)
        position_b, output = process_tape(program_b, position_b, phase[1], output, read_state)
        position_c, output = process_tape(program_c, position_c, phase[2], output, read_state)
        position_d, output = process_tape(program_d, position_d, phase[3], output, read_state)
        position_e, output = process_tape(program_e, position_e, phase[4], output, read_state)

def feedback_two(program, phase_settings):
    # Initialize amp a
    program_a = program.copy()
    position, output = amplify(program_a, 0, 0)
    # Initialize the other amps (a->e)
    amps = [
        (program_a, position, phase_settings[0]), # amp a
        (program.copy(), 0, phase_settings[1]), # amp b
        (program.copy(), 0, phase_settings[2]), # amp c
        (program.copy(), 0, phase_settings[3]), # amp d
        (program.copy(), 0, phase_settings[4]), # amp e
    ]


    while(True):
        for i in range (0, 5):
            print('amp {}'.format(i))
            amp = amps[i]
            current_program = amps[i][0]
            current_position = amps[i][1]
            input = amps[i][2]
            #print(current_program)
            position, output = amplify(current_program, current_position, input)
            amps[i] = (current_program, position, output)
            #print('amp input {} output {}'.format(input, output))

    print('*')
    '''
    while (True):
        for i in [1,2,3,4,0]:
            amp = amps[i]
            input = amp[2]
            position, output = amplify(amp[0], amp[1], input)
            amps[i] = (amp[0], position, output)
            print('amp input {} output {}'.format(input, output))
    '''

'''
def feedback(program, phase_list):
    # Set up - use input 0, then phase for each amp
    program_a = program.copy()
    position_a = 0
    input = 0
    (position_a, output) = amplify(program_a, position_a, [phase_list[0],0])
    print('amp a input {} output {}'.format(input, output))

    program_b = program.copy()
    position_b = 0
    input = phase_list[1]
    (position_b, output) = amplify(program_b, position_b, [input])
    print('amp b input {} output {}'.format(input, output))


    program_c = program.copy()
    position_c = 0
    input = phase_list[2]
    (position_c, output) = amplify(program_c, position_c, [input])
    print('amp c input {} output {}'.format(input, output))

    program_d = program.copy()
    position_d = 0
    input = phase_list[3]
    (position_d, output) = amplify(program_d, position_d, [input])
    print('amp d input {} output {}'.format(input, output))

    program_e = program.copy()
    position_e = 0
    input = phase_list[4]
    (position_e, output) = amplify(program_e, position_e, input)
    print('amp e input {} output {}'.format(input, output))

    input = phase_list[0]
    (position_a, output) = amplify(program_a, position_a, input)
    print('amp a input {} output {}'.format(input, output))


    # Start using output
    while(True):
        (position_b, output) = amplify(program_b, position_b, output)
        (position_c, output) = amplify(program_c, position_c, output)
        (position_d, output) = amplify(program_d, position_d, output)
        (position_e, output) = amplify(program_e, position_e, output)
        (position_a, output) = amplify(program_a, position_a, output)


    return None
'''
program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#print(feedback(program, [9,8,7,6,5]))

#print(feed3(program, [9,8,7,6,5]))

program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
print(feed3(program, [9,7,8,5,6]))
