import math

def get_digits(candidate):
    digits = []
    for i in range (6, 0, -1):
        digits.append(int(candidate % math.pow(10, i) / math.pow(10, i-1)))
    return digits

# Check each digit from left to right and check that they don't decrease
def digits_dont_decrease(candidate):
    # It's a six digit number and cannot start with 0
    previous_digit = 0
    for digit in get_digits(candidate):
        if (digit < previous_digit):
            return False
        previous_digit = digit
    return True

def has_pair(candidate):
    previous_digit = 0
    for digit in get_digits(candidate):
        if (digit == previous_digit):
            return True
        previous_digit = digit
    return False

# Collect any adjecent digits in a dictionary
# For the key, start with 0 and increment it every time we see a different value for the digit.
# (every time a chain of identical numbers is broken).
# Otherwise we would count 112311 into {1:4} and return False
# even though there is a valid pair of digits.
# However, there is an additional criteria in that the digits must not decrease
# so we will never see that input if we call this in conjuction with digits_dont_decrease
# (But let's make it correct anyway)
def has_exact_pair(candidate):
    group = {}
    key = 0
    previous_digit = 0
    for digit in get_digits(candidate):
        if (digit == previous_digit):
            group[key] = group.get(key,1) + 1
        else:
            key = key + 1
        previous_digit = digit

    for k in group:
        # exactly a pair
        if group[k] == 2:
            return True

    return False

# For a 6 digit number, how many in a given range match the following criteria
# 1) The digits from left to right do not decrease e.g. 123456 (and not 123454)
# 2) Two adjecent digits are identical : 111111, 112233
def is_valid(candidate):
    return (digits_dont_decrease(candidate) and has_pair(candidate))

# Additional criterion for problem 2
# The two adjecent numbers can't be part of a larger group.
# This means there must be one pair of numbers:
#   111122 is ok (1111 doesn't count but 22 does)
#   222333 is invalid
#   444444 is invalid
def is_valid_2(candidate):
    return (digits_dont_decrease(candidate) and has_exact_pair(i))

# Tests
print(is_valid(345679))
print(is_valid(111111))
print(is_valid(223450))
print(is_valid(123789))
print(is_valid(122789))

print(has_exact_pair(123444))
print(has_exact_pair(112311))

# Problem input
solution_1 = 0
solution_2 = 0
for i in range(254032, 789861):
    if (is_valid(i)):
        solution_1 = solution_1 + 1
    if (is_valid_2(i)):
        solution_2 = solution_2 + 1

print('solution 1 {}'.format(solution_1))
print('solution 2 {}'.format(solution_2))
