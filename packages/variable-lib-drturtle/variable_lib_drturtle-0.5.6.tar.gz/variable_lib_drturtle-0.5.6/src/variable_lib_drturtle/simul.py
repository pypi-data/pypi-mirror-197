from variable_lib_drturtle.resource import *

class Entity:
    def __init__(self, name, mass, pos=[0,0], vel=[0,0]):
        self.name = name

        self.mass = Variable(mass, "Mass (kg)")
        self.pos = NDVariable(pos, "Position (m)")
        self.vel = NDVariable(vel, "Velocity (m/s)")

    def simulate(self, dt: float, *forces):
        a = sum(forces) / self.mass
        self.vel += a * dt
        self.pos += self.vel.value * dt
        return a


class Simulation:
    def __init__(self, t_i=0):
        self.time = NDVariable(t_i, "Time (s)")

    def run(self, dt):
        self.time += dt
