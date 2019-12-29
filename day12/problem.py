from itertools import combinations
import math
class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

def update_moon_velocities(m1, m2):
    dvx1, dvx2 = get_velocity_delta(m1.x, m2.x)
    m1.vx = m1.vx + dvx1
    m2.vx = m2.vx + dvx2

    dvy1, dvy2 = get_velocity_delta(m1.y, m2.y)
    m1.vy = m1.vy + dvy1
    m2.vy = m2.vy + dvy2

    dvz1, dvz2 = get_velocity_delta(m1.z, m2.z)
    m1.vz = m1.vz + dvz1
    m2.vz = m2.vz + dvz2

def get_velocity_delta(pos1, pos2):
        if (pos1 == pos2):
            return (0,0)
        if (pos1 < pos2):
            return (1,-1)
        return (-1,1)

def do_step(moons):
    for moon in moons:
        moon.x = moon.x + moon.vx
        moon.y = moon.y + moon.vy
        moon.z = moon.z + moon.vz

def get_energy(moons):
    total = 0
    for moon in moons:
        pot = abs(moon.x) + abs(moon.y) + abs(moon.z)
        kin = abs(moon.vx) + abs(moon.vy) + abs(moon.vz)
        total = total + (pot * kin)

    return total

def problem1():
    moons = [ Moon(-13,-13,-13), Moon(5,-8,3), Moon(-6,-10,-3), Moon(0,5,-5)]
    #moons = [ Moon(-1,0,2), Moon(2,-10,-7), Moon(4,-8,8), Moon(3,5,-1)]
    for i in range(0,1000):
        for pair in combinations(moons,2):
            update_moon_velocities(pair[0],pair[1])
        do_step(moons)

    print(get_energy(moons))

problem1()


def check_moonal_x(moons,original_moons):
    for i in range(0, len(moons)):
        if (moons[i].x != original_moons[i].x or \
            moons[i].vx != original_moons[i].vx):
            return False
    return True

def check_moonal_y(moons,original_moons):
    for i in range(0, len(moons)):
        if (moons[i].y != original_moons[i].y or \
            moons[i].vy != original_moons[i].vy):
            return False
    return True

def check_moonal_z(moons,original_moons):
    for i in range(0, len(moons)):
        if (moons[i].z != original_moons[i].z or \
            moons[i].vz!= original_moons[i].vz):
            return False
    return True

def get_lowest_common_multiple(x,y,z):
    xs = set()
    ys = set()
    zs = set()
    multiplier = 0
    common = set()
    while (len(common) == 0):
        multiplier = multiplier + 1
        if (multiplier % 1000 == 0):
            print(multiplier)
        xs.add(multiplier * x)
        ys.add(multiplier * y)
        zs.add(multiplier * z)
        #print('{} {}'.format(multiplier, xs))
        common = xs.intersection(ys).intersection(zs)

    return common.pop()

def get_lcm(x,y):
    return int(x * y / math.gcd(x,y))

def problem2():

    # Test 1
    #moons =          [ Moon(-1,0,2), Moon(2,-10,-7), Moon(4,-8,8), Moon(3,5,-1)]
    #original_moons = [ Moon(-1,0,2), Moon(2,-10,-7), Moon(4,-8,8), Moon(3,5,-1)]

    # Test 2
    #moons =          [ Moon(-8,-10,0), Moon(5,5,10), Moon(2,-7,3), Moon(9,-8,-3)]
    #original_moons = [ Moon(-8,-10,0), Moon(5,5,10), Moon(2,-7,3), Moon(9,-8,-3)]

    # Puzzle input
    moons = [ Moon(-13,-13,-13), Moon(5,-8,3), Moon(-6,-10,-3), Moon(0,5,-5)]
    original_moons = [ Moon(-13,-13,-13), Moon(5,-8,3), Moon(-6,-10,-3), Moon(0,5,-5)]

    # Get each orbital plane period for all moons
    x_period = 0
    y_period = 0
    z_period = 0
    steps = 0
    while (x_period == 0 or y_period == 0 or z_period == 0):
        for pair in combinations(moons,2):
            update_moon_velocities(pair[0],pair[1])
        do_step(moons)
        steps = steps + 1
        all_x = check_moonal_x(original_moons,moons)
        all_y = check_moonal_y(original_moons,moons)
        all_z = check_moonal_z(original_moons,moons)

        if (all_x and x_period == 0):
            x_period = steps
            print('moonal X match at {}'.format(x_period))
        if (all_y and y_period == 0):
            y_period = steps
            print('moonal Y match at {}'.format(y_period))
        if (all_z and z_period == 0):
            z_period = steps
            print('moonal Z match at {}'.format(z_period))

    print('x {}'.format(x_period))
    print('y {}'.format(y_period))
    print('z {}'.format(z_period))

    # The lowest common multiple of these periods is the number of steps required
    # for the entire system to return to the initial state.
    print(get_lcm(get_lcm(x_period,y_period),z_period))

problem2()
