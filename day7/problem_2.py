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

def amplify(tape, position, inputs):
    #input_consumed = False
    output = None
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

                if len(inputs) > 0:
                    input = inputs.pop()
                    print('consuming input {}'.format(input))
                    tape[param_1] =  input
                    input_consumed = True
                else:
                    print('Need more input')
                    return (position, output)

            elif op_code == 4:
                output = tape[param_1]
                return(position + 2, output)
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
            return(None, output)

        #print(tape)

    return None

def feedback_two(program, phase_settings):
    # Initialize the amps with a copy of the program, position (0) and an input value
    amps = [
        (program.copy(), 0, 0), # amp a
        (program.copy(), 0, phase_settings[1]), # amp b
        (program.copy(), 0, phase_settings[2]), # amp c
        (program.copy(), 0, phase_settings[3]), # amp d
        (program.copy(), 0, phase_settings[4]), # amp e
    ]

    # Initialze
    for i in range (0, 5):
        amp = amps[i]
        input = amp[2]
        position, output = amplify(amp[0], amp[1], input)
        amps[i] = (amp[0], position, output)
        print('amp input {} output {}'.format(input, output))
        #print(amps[i])

    print('*')
    # run amp a with phase setting
    amp = amps[0]
    input = phase_settings[0]
    position, output = amplify(amp[0], amp[1], input)
    print('amp input {} output {}'.format(input, output))

    while (True):
        for i in [1,2,3,4,0]:
            amp = amps[i]
            input = amp[2]
            position, output = amplify(amp[0], amp[1], input)
            amps[i] = (amp[0], position, output)
            print('amp input {} output {}'.format(input, output))


def feedback(program, phase_list):
    # Set up - use input 0, then phase for each amp
    program_a = program.copy()
    position_a = 0
    input = 0
    (position_a, output) = amplify(program_a, position_a, [phase_list[0],0])
    print('amp a input {} output {}'.format(input, output))

    '''
    program_b = program.copy()
    position_b = 0
    input = phase_list[1]
    (position_b, output) = amplify(program_b, position_b, input)
    print('amp b input {} output {}'.format(input, output))


    program_c = program.copy()
    position_c = 0
    input = phase_list[2]
    (position_c, output) = amplify(program_c, position_c, input)
    print('amp c input {} output {}'.format(input, output))

    program_d = program.copy()
    position_d = 0
    input = phase_list[3]
    (position_d, output) = amplify(program_d, position_d, input)
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
    '''

    return None

program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#print(feedback(program, [9,8,7,6,5]))

print(feedback(program, [9,8,7,6,5]))
