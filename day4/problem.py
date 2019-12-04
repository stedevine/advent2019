import math
def digits_dont_decrease(candidate):
    #  6 digit number
    last_value = 0
    for i in range (6, 0, -1):
        digit = int(candidate % math.pow(10,i) / math.pow(10,i-1))
        if (digit < last_value):
            return False
        last_value = digit

    return True

def has_double(candidate):
    #  6 digit number
    last_value = 0
    for i in range (6, 0, -1):
        digit = int(candidate % math.pow(10,i) / math.pow(10,i-1))
        if (digit == last_value):
            return True
        last_value = digit

    return False

def has_correct_group_legth(candidate):
    group = {}
    last_value = 0
    for i in range (6, 0, -1):
        digit = int(candidate % math.pow(10,i) / math.pow(10,i-1))
        if (digit == last_value):
            group[digit] = group.get(digit,1) + 1
        last_value = digit

    #print(group)
    for key in group:
        if group[key] == 2:
            return True

    return False

def is_valid(candidate):
    return (digits_dont_decrease(candidate) and has_double(candidate))

def is_valid_2(candidate):
    return (digits_dont_decrease(candidate)  and has_correct_group_legth(i))


# Tests
print(is_valid(345679))
print(is_valid(111111))
print(is_valid(223450))
print(is_valid(123789))
print(is_valid(122789))

#
print(has_correct_group_legth(123444))

count = 0
for i in range(254032, 789861):
    if (is_valid(i)):
        count = count + 1

print(count)

count = 0
for i in range(254032, 789861):
    if (is_valid_2(i)):
        count = count + 1

print(count)
