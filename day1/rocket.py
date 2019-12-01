# Formula for calculating the amount of fuel required for a specific mass
def get_fuel_for_mass(mass):
    return int(mass / 3) - 2

# Formula for calculating the amount of fuel required to lift the fuel itself.
def get_fuel_for_fuel(mass):
    total_fuel = 0
    fuel = get_fuel_for_mass(mass)

    while True:
        total_fuel += fuel
        fuel = get_fuel_for_mass(fuel)
        if (fuel < 0):
            break
    return total_fuel


def process_input_file(function):
    with open('./input.txt') as file:
        total_fuel = 0
        for line in file:
            total_fuel += function(int(line.strip()))

        print(total_fuel)

# Problem 1
process_input_file(get_fuel_for_mass)
# Problem 2
process_input_file(get_fuel_for_fuel)
