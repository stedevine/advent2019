def get_noun_verb_compound(target, tape):
    for noun in range(0,100):
        for verb in range(0,100):
            tape[1] = noun
            tape[2] = verb
            if (get_position_zero_value_after_program_completes(tape) == target):
                return 100 * noun + verb

def get_position_zero_value_after_program_completes(input):
    tape = input.copy()
    position = 0
    while True:
        op_code = tape[position]
        if op_code == 1:
            tape[tape[position + 3]] = tape[tape[position + 1]] + tape[tape[position + 2]]
        elif op_code == 2:
            tape[tape[position + 3]] = tape[tape[position + 1]] * tape[tape[position + 2]]
        elif op_code == 99:
            return tape[0]
        else:
            raise Exception('Unrecognized opcode')
        position = position + 4


problem_input = [1,-1,-1,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,5,23,2,10,23,27,2,27,13,31,1,10,31,35,1,35,9,39,2,39,13,43,1,43,5,47,1,47,6,51,2,6,51,55,1,5,55,59,2,9,59,63,2,6,63,67,1,13,67,71,1,9,71,75,2,13,75,79,1,79,10,83,2,83,9,87,1,5,87,91,2,91,6,95,2,13,95,99,1,99,5,103,1,103,2,107,1,107,10,0,99,2,0,14,0]

# Problem 1
problem_input[1] = 12
problem_input[2] = 2
print(get_position_zero_value_after_program_completes(problem_input))

# Problem 2
print(get_noun_verb_compound(19690720, problem_input))
