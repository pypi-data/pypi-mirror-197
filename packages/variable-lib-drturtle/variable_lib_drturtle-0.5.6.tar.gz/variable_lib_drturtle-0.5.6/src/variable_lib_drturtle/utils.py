G = 6.674 * (10**-11)  # constant G
import numpy as np
import matplotlib.pyplot as plt


def sct(x, y, x_axis, y_axis, title, **kwargs):
    plt.scatter(x, y, **kwargs)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)
    return plt


def quiver(
    x: np.ndarray,
    y: np.ndarray,
    u,
    v,
    x_axis: str = "x",
    y_axis: str = "y",
    title="x vs y",
    **kwargs
):
    plt.quiver(x, y, u, v, **kwargs)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)
    return plt
