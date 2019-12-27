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

'''
<x=-13, y=-13, z=-13>
<x=5, y=-8, z=3>
<x=-6, y=-10, z=-3>
<x=0, y=5, z=-5>
'''

moons = [ Moon(-13,-13,-13), Moon(5,-8,3), Moon(-6,-10,-3), Moon(0,5,-5)]
for i in range (0,1000):
    for pair in combinations(moons,2):
        update_moon_velocities(pair[0],pair[1])
    do_step(moons)

for moon in moons:
    print(vars(moon))

print(get_energy(moons))
