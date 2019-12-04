import math

# Check each digit from left to right and check that they don't decrease
def digits_dont_decrease(candidate):
    # It's a six digit number and cannot start with 0
    last_value = 0
    for i in range (6, 0, -1):
        digit = int(candidate % math.pow(10, i) / math.pow(10, i-1))
        if (digit < last_value):
            return False
        last_value = digit

    return True

def has_pair(candidate):
    last_value = 0
    for i in range (6, 0, -1):
        digit = int(candidate % math.pow(10, i) / math.pow(10, i-1))
        if (digit == last_value):
            return True
        last_value = digit

    return False

# Collect any adjecent digits in a dictionary
# Note this would count 112311 into {1:4} and return False
# even though there is a valid pair of digits.
# However, there is an additional criteria in that the digits must not decrease
# so we will never see that input if we call this in conjuction with digits_dont_decrease
def has_exact_pair(candidate):
    group = {}
    last_value = 0
    for i in range (6, 0, -1):
        digit = int(candidate % math.pow(10,i) / math.pow(10,i-1))
        if (digit == last_value):
            group[digit] = group.get(digit,1) + 1
        last_value = digit

    for key in group:
        # exactly a pair
        if group[key] == 2:
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

#
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
