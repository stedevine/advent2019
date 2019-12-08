def get_total_orbital_distance(orbits):
    # Each moon orbits exactly one planet
    # Build a dictionary of these relationships
    distance = 0
    moon_to_planet = {}
    for orbit in orbits:
        print(orbit)
        planet, moon = orbit.split(')')
        moon_to_planet[moon] = planet

    # For each moon in the dictionay find the number of 'steps' back to the COM
    for moon in moon_to_planet:
        distance = distance + get_distance_to_COM(moon, moon_to_planet)
    return distance

def get_distance_to_COM(moon, moon_to_planet):
    distance = 1
    while(moon_to_planet[moon] != 'COM'):
        distance = distance + 1
        moon = moon_to_planet[moon]
    return distance


test_input = [
'COM)B',
'B)C',
'C)D',
'D)E',
'E)F',
'B)G',
'G)H',
'D)I',
'E)J',
'J)K',
'K)L']
print(get_total_orbital_distance(test_input))
with open ('./input.txt') as file:
    content = file.readlines()
    problem_input = [x.strip() for x in content]
    print(get_total_orbital_distance(problem_input))
