def get_total_orbital_distance(orbits):
    # Each moon orbits exactly one planet
    # Build a dictionary of these relationships
    moon_to_planet = get_moon_to_planet(orbits)

    # For each moon in the dictionay find the number of 'steps' back to the COM
    distance = 0
    for moon in moon_to_planet:
        distance = distance + get_distance_to_COM(moon, moon_to_planet)
    return distance

def get_moon_to_planet(orbits):
    moon_to_planet = {}
    for orbit in orbits:
        planet, moon = orbit.split(')')
        moon_to_planet[moon] = planet

    return moon_to_planet

def get_distance_to_COM(moon, moon_to_planet):
    distance = 1
    while(moon_to_planet[moon] != 'COM'):
        distance = distance + 1
        moon = moon_to_planet[moon]
    return distance

def get_total_hops(orbits):
    # Find the path back to the COM for both moons
    # The shortest path from one to the other involves finding the first common moon in their paths
    # Then the total number of hops is (YOU -> common moon) + (SAN -> common moon) - 2 (because we actually care about the distances
    # to the objects the moons are orbits, not the moons themselves.)
    you_path = get_path_from_moon_to_COM(orbits,'YOU')
    san_path = get_path_from_moon_to_COM(orbits,'SAN')
    for moon in san_path:
        if (you_path.get(moon, None) != None):
            print('common moon {}'.format(moon))
            return you_path[moon] + san_path[moon] - 2

def get_path_from_moon_to_COM(orbits, start_moon):
    moon_to_planet = get_moon_to_planet(orbits)
    moon = start_moon
    path = {}
    hops = 0
    while(moon_to_planet.get(moon, None) != None):
        path[moon] = hops
        hops = hops + 1
        moon = moon_to_planet[moon]
    return path

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
print('test 1 solution {}'.format(get_total_orbital_distance(test_input)))
test_input_2 = [
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
'K)L',
'K)YOU',
'I)SAN']
print('test 2 solution {}'.format(get_total_hops(test_input_2)))

with open ('./input.txt') as file:
    content = file.readlines()
    problem_input = [x.strip() for x in content]
    print('solution 1: {}'.format(get_total_orbital_distance(problem_input)))
    print('solution 2: {}'.format(get_total_hops(problem_input)))
