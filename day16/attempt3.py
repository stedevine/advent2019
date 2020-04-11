import sys

def get_next_phase(phase):
    next_phase = []
    for output_digit in range(0, len(phase)):
        positive = 0
        negative = 0
        #pos_gen = get_positive_generator(output_digit, phase_length)
        for index in get_positive_generator(output_digit, len(phase)):
            positive += phase[index]
        for index in get_negative_generator(output_digit, len(phase)):
            negative -= phase[index]
        next_phase.append(abs(positive + negative) % 10)
    return next_phase

def get_positive_generator(output_digit, phase_length):
    for d in range(0, phase_length):
        m = (d % (4 * (output_digit + 1)))
        if (m <= output_digit and d+output_digit < phase_length):
            yield (d+output_digit)

def get_negative_generator(output_digit, phase_length):
    for d in range(0,phase_length):
        m = (d % (4 * (output_digit + 1)))
        if (m <= output_digit and d+output_digit < phase_length):
            if (d+output_digit+(2 * (output_digit + 1))) < phase_length:
                yield (d+output_digit+(2 * (output_digit + 1)))


def eight_digits_100_phases(input):
    phase = [int(x) for x in input]
    for i in range(0,100):
        phase = get_next_phase(phase)

    return ''.join([str(d) for d in phase[:8]])

def tests():
    print("simple tests:")
    input = "12345678"
    phase = [int(d) for d in input]
    phase = phase * 10
    for i in range(0,4):
        phase = get_next_phase(phase)
        print(''.join(str(d) for d in phase))

    print('100 phase tests:')
    print(eight_digits_100_phases('80871224585914546619083218645595'))
    print(eight_digits_100_phases('19617804207202209144916044189917'))
    print(eight_digits_100_phases('69317163492948606335995924319873'))

def problem_1():
    problem_input = '59713137269801099632654181286233935219811755500455380934770765569131734596763695509279561685788856471420060118738307712184666979727705799202164390635688439701763288535574113283975613430058332890215685102656193056939765590473237031584326028162831872694742473094498692690926378560215065112055277042957192884484736885085776095601258138827407479864966595805684283736114104361200511149403415264005242802552220930514486188661282691447267079869746222193563352374541269431531666903127492467446100184447658357579189070698707540721959527692466414290626633017164810627099243281653139996025661993610763947987942741831185002756364249992028050315704531567916821944'
    print('problem 1 : {}'.format(eight_digits_100_phases(problem_input)))

#tests()
#problem_1()
