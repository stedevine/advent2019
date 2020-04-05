import math

def get_pattern_digit(pattern_offset, output_digit):
    # base pattern = 0,1,0,-1
    sector_length = (output_digit + 1)
    #print(" sector length {}".format(sector_length))
    pattern_length = 4 * (output_digit + 1)
    #print(" pattern length {}".format(pattern_length))
    wrapped_offset = pattern_offset % pattern_length
    #section = float(wrapped_offset)/pattern_length
    if wrapped_offset < sector_length:
        return 0
    if wrapped_offset < 2 * sector_length:
        return 1
    if wrapped_offset < 3 * sector_length:
        return 0

    return -1

def get_next_phase(phase):
    next_phase = []
    for output_digit in range(0, len(phase)):
        sum = 0
        for phase_offset in range(0, len(phase)):
            sum += phase[phase_offset] * get_pattern_digit(phase_offset + 1, output_digit)
        next_phase.append(abs(sum) % 10)
        sum = 0
    return next_phase

def get_first_eight_after_100_phases(phase):
    phase = [int(d) for d in phase]
    for phase_number in range(0,100):
        phase = get_next_phase(phase)

    return ''.join(str(d) for d in phase[:8])

def simple_tests():
    print("simple tests:")
    input = "12345678"
    phase = [int(d) for d in input]
    for i in range(0,4):
        phase = get_next_phase(phase)
        print(''.join(str(d) for d in phase))

def complex_tests():
    print("complex tests:")
    print(get_first_eight_after_100_phases("80871224585914546619083218645595"))
    print(get_first_eight_after_100_phases("19617804207202209144916044189917"))
    print(get_first_eight_after_100_phases("69317163492948606335995924319873"))

problem_input = '59713137269801099632654181286233935219811755500455380934770765569131734596763695509279561685788856471420060118738307712184666979727705799202164390635688439701763288535574113283975613430058332890215685102656193056939765590473237031584326028162831872694742473094498692690926378560215065112055277042957192884484736885085776095601258138827407479864966595805684283736114104361200511149403415264005242802552220930514486188661282691447267079869746222193563352374541269431531666903127492467446100184447658357579189070698707540721959527692466414290626633017164810627099243281653139996025661993610763947987942741831185002756364249992028050315704531567916821944'
print(get_first_eight_after_100_phases(problem_input))
