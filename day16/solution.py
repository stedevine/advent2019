import math
import sys

def get_pattern_digit(phase_digit_position, element):
    # Pattern for 0th element : 0 1 0 -1
    # Pattern for 1st element : 0 0 1 1 0 0 -1 -1

    #phase phase_digit_position is the offset into the pattern

    # Element gives length of pattern: 0 -> 4. 1->8


    # When applying the pattern, skip the very first value exactly once.
    # If element = 16 and lenght of pattern = 10 offset is 7
    pattern_length = len(zero_pattern) * (element + 1)
    offset = phase_digit_position % pattern_length + 1
    # Result depends on where in the pattern the offset is:
    # First 1/4 : 0
    # Second 1/4 : 1
    # Third 1/4 : 0
    # Last 1/4 : -1
    sector = float(offset)/pattern_length
    if sector <= 0.25:
        return 0
    if sector <= 0.5:
        return 1
    if sector <= 0.75:
        return 0

    return -1

def get_output_value_2(input, phase_number):
    sum = 0
    for position in range(0,len(input)):
        sum += input[position] * get_pattern_digit()

def build_pattern(position, zero_pattern):
    return sum([[p]*(position+1) for p in zero_pattern],[])

def get_output_value(input, pattern):
    sum = 0
    for position in range(0,len(input)):
        sum += input[position] * pattern[ (position+1) % len(pattern) ]
    return abs(sum) % 10

def get_next_phase(input, zero_pattern):
    phase = []
    for position in range(0,len(input)):
        #sys.stdout.write("\r Position {}".format(position))
        pattern = build_pattern(position, zero_pattern)
        phase.append(get_output_value(input, pattern))
    #sys.stdout.flush()
    return phase

def eight_digits_100_phases(input):
    phase = [int(x) for x in input]
    for i in range(0,100):
        phase = get_next_phase(phase, zero_pattern)

    return ''.join([str(d) for d in phase[:8]])

zero_pattern = [0, 1, 0, -1]

# Part 1
def tests():
    input = '12345678'
    print('Initial tests:')
    phase = [int(x) for x in input]
    for i in range(0,4):
        phase = get_next_phase(phase, zero_pattern)
        print(''.join([str(d) for d in phase]))

    print('100 phase tests:')
    print(eight_digits_100_phases('80871224585914546619083218645595'))
    print(eight_digits_100_phases('19617804207202209144916044189917'))
    print(eight_digits_100_phases('69317163492948606335995924319873'))

def problem_1():
    problem_input = '59713137269801099632654181286233935219811755500455380934770765569131734596763695509279561685788856471420060118738307712184666979727705799202164390635688439701763288535574113283975613430058332890215685102656193056939765590473237031584326028162831872694742473094498692690926378560215065112055277042957192884484736885085776095601258138827407479864966595805684283736114104361200511149403415264005242802552220930514486188661282691447267079869746222193563352374541269431531666903127492467446100184447658357579189070698707540721959527692466414290626633017164810627099243281653139996025661993610763947987942741831185002756364249992028050315704531567916821944'
    print('problem 1 : {}'.format(eight_digits_100_phases(problem_input)))

problem_1()

# Part 2
def apply_phases(input, number_of_phases):
    phase = [int(x) for x in input]
    for i in range(0, number_of_phases):
        print('phase {}'.format(i))
        phase = get_next_phase(phase, zero_pattern)

    return phase


def get_message_from_offset(phase):
    # First 7 digits are the message offset
    message_offset_digits = [int(d) for d in phase[:7]]
    message_offset = 0
    mul = 1
    for d in range(len(message_offset_digits)-1,-1,-1):
        message_offset += message_offset_digits[d] * mul
        mul *= 10

    print(message_offset)
    message_offset = message_offset % len(phase)
    print(message_offset)
    phase = apply_phases(phase * 10000,100)
    #print(len(phase))
    #print(phase)
    #print(phase[message_offset])
    print(phase[message_offset-1:message_offset+8])

#print(apply_phases('03036732577212944063491565474664',10000))
#print(get_message_from_offset('03036732577212944063491565474664'))
