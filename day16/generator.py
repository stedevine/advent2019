'''
def get_positive_numbers(output_digit, phase_length):
    numbers = []
    for d in range(0, phase_length):
        m = (d % (4 * (output_digit + 1)))
        if (m <= output_digit and d+output_digit < phase_length):
            #print("+ {}".format(d+output_digit))
            numbers.append(d+output_digit)
    return numbers
'''
'''
def some_numbers(output_digit, phase_length):
    num = 0
    while True:
        m = (d % (4 * (output_digit + 1)))
        if (m <= output_digit and d+output_digit < phase_length):
            num  = d+output_digit
            yield num
'''

def some_numbers():
    num = 0
    while True:
        num = num**2
        yield num

for i in some_numbers():
    if i > 100:
        print('break')
        break
    print(i)

while True:
    i = next(some_numbers())
    if i > 100:
        print('break')
        break
    print(i)
