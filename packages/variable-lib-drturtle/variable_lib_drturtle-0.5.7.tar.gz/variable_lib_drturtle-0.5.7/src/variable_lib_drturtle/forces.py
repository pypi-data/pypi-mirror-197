import numpy as np
import matplotlib.pyplot as plt

k = 9e9  # Coulomb's Constant (Nm^2/C^2)
G = 6.674 * (10**-11)  # constant G


def Gravity(m1: float, m2: float, pos1: np.ndarray, pos2: np.ndarray):
    """Calculate gravitational force between two objects"""

    # setting up radius vector (sun to earth)
    r = pos2 - pos1  # creates the radius vector of sun to earth
    rmag = np.linalg.norm(r)  # normalizes the radius vecotr
    rhat = r / rmag  # unit vector for radius

    # define force object 2 exerts on object 1
    return (G * m1 * m2) / (rmag**2) * rhat


def Gfield(
    obj_m: float, obj_pos: np.ndarray, obj_radius: float, x_pos: float, y_pos: float
) -> tuple:
    """Calculate the gravitational force for two object for use in a quiver plot."""
    r = np.array([x_pos, y_pos]) - obj_pos  # radius vector
    r_mag = np.linalg.norm(r)

    # ensure 2nd object outside obj
    if r_mag <= obj_radius:
        return 0, 0

    r_hat = r / r_mag  # direction of vector
    grav = (-(G * obj_m) / (r_mag**2)) * r_hat
    return grav



def drag_force_2d(velocity, rho, C, A):
    vMag = velocity.magnitude
    vHat = velocity / vMag  # direction of velocity

    Fdrag = (1 / 2) * rho * (vMag**2) * C * A * vHat
    return Fdrag


# function to calculate electric field force
def EField(q1: float, q2: float, pos1: np.ndarray, pos2: np.ndarray):
    """Calculates the electric force on object 1 from object 2"""
    r = pos1 - pos2  # distance between obj 1 and obj 2
    r_mag = np.linalg.norm(r)
    r_hat = r / r_mag

    return k * (q1 * q2) / (r_mag**2) * r_hat


def PointEField(q, pos, x_pos, y_pos):

    # Calculate the distance between the charge and the field point.
    r = np.array([x_pos, y_pos]) - pos
    rmag = np.linalg.norm(r)

    if rmag <= 0:
        return (0, 0)
    else:
        rhat = r / rmag
        # Calculate the electric field's magnitude.
        Emag = (k * q) / (rmag**2) * rhat
        # Return the two components as the function's outputs.
        return Emag


def field_over_linspace(X, Y, func, *args):
    u = np.zeros(X.shape)
    v = np.zeros(Y.shape)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            u[i, j], v[i, j] = func(*args, X[i, j], Y[i, j])

    return u, v

# apply a gravity field with an object
def Gfield_vector(obj_m: float, obj_pos: np.ndarray, obj_radius: float, X, Y):
    return field_over_linspace(X, Y, Gfield, obj_m, obj_pos, obj_radius)
