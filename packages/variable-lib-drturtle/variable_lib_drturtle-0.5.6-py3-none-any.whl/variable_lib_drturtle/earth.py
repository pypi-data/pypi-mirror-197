from variable_lib_drturtle.forces import Gfield_vector
from variable_lib_drturtle.utils import quiver
from variable_lib_drturtle.variables import Variable
import matplotlib.pyplot as plt
import numpy as np

EARTH_MASS = Variable(6e24, "Mass of Earth (kg)")
EARTH_POS = np.array([0, 0]) #initial position of earth (m)
EARTH_RADIUS = Variable(6_378e3, "Radius of Earth (m)")


def plot_earth(initial=EARTH_POS, mag=4):
    x = np.linspace(-mag * EARTH_RADIUS, mag * EARTH_RADIUS, mag*2+1)
    y = np.linspace(-mag * EARTH_RADIUS, mag * EARTH_RADIUS, mag*2+1)
    X, Y = np.meshgrid(x, y)

    # calculate magntitude of gravity arrows

    # Gfield_vector applies Gfield over a vectorfield (X, Y)
    u, v = Gfield_vector(EARTH_MASS, initial, EARTH_RADIUS, X, Y)

    plt.plot(
        EARTH_RADIUS * np.cos(np.linspace(0,np.pi*2,361)),
        EARTH_RADIUS * np.sin(np.linspace(0,np.pi*2,361))
    )
    # plot gravity field
    quiver(X, Y, u, v)
    # make plot look right
    plt.axis('equal')

    return X, Y, u, v
