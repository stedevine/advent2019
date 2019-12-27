from itertools import combinations
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

def slight_return(original_moons, moons):
    for i in range(0, len(moons)):
        if (moons[i].x != original_moons[i].x or \
            moons[i].y != original_moons[i].y or \
            moons[i].z != original_moons[i].z or \
            moons[i].vx != original_moons[i].vx or \
            moons[i].vy != original_moons[i].vy or \
            moons[i].vz != original_moons[i].vz):
                return False
    return True

def check_moonal_pair(moon1,moon2):
    return (moon1.x == moon2.x and \
            moon1.y == moon2.y and \
            moon1.z == moon2.z and \
            moon1.vx == moon2.vx and \
            moon1.vy == moon2.vy and \
            moon1.vz == moon2.vz)

def problem2():
    #moons = [ Moon(-8,-10,0), Moon(5,5,10), Moon(2,-7,3), Moon(9,-8,-3)]
    #original_moons = [ Moon(-8,-10,0), Moon(5,5,10), Moon(2,-7,3), Moon(9,-8,-3)]
    #moons = [ Moon(-13,-13,-13), Moon(5,-8,3), Moon(-6,-10,-3), Moon(0,5,-5)]
    #original_moons = [ Moon(-13,-13,-13), Moon(5,-8,3), Moon(-6,-10,-3), Moon(0,5,-5)]

    #moons = [ Moon(-13,-13,-13), Moon(5,-8,3), Moon(-6,-10,-3), Moon(0,5,-5)]
    #original_moons = [ Moon(-13,-13,-13), Moon(5,-8,3), Moon(-6,-10,-3), Moon(0,5,-5)]


    moons = [ Moon(-1,0,2), Moon(2,-10,-7), Moon(4,-8,8), Moon(3,5,-1)]
    original_moons = [ Moon(-1,0,2), Moon(2,-10,-7), Moon(4,-8,8), Moon(3,5,-1)]

    i = 0
    while(True):
        i = i + 1
        for pair in combinations(moons,2):
            update_moon_velocities(pair[0],pair[1])
        do_step(moons)

        for j in range(0,len(moons)):
            if check_moonal_pair(moons[j],original_moons[j]):
                print('moonal match at {}'.format(i))

        if (slight_return(original_moons,moons)):
            print('total match at {}'.format(i))
            break

    for moon in moons:
        print(vars(moon))

#problem2()
# Get the period of each orbit?
'''
moons = [ Moon(-1,0,2), Moon(2,-10,-7), Moon(4,-8,8), Moon(3,5,-1)]
original_moons = [ Moon(-1,0,2), Moon(2,-10,-7), Moon(4,-8,8), Moon(3,5,-1)]
i = 0
while(True):
    i = i + 1
    for pair in combinations(moons,2):
        update_moon_velocities(pair[0],pair[1])
    do_step(moons)
    if (slight_return(original_moons,moons)):
        print(i)
        break

for moon in moons:
    print(vars(moon))

'''
