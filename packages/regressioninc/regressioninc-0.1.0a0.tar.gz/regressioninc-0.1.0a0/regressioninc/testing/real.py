"""
Functions for generating and visualising real-valued testing data
"""
from loguru import logger
from typing import Optional, Dict, Tuple
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def generate_linear(coef: np.ndarray, n_samples: int, intercept: float = 0):
    """Generate real-valued linear testing data"""
    n_features = coef.size
    if n_samples < n_features:
        raise ValueError(f"{n_samples=} must be >= {n_features=}")

    # generate the data
    shape = (n_samples, n_features)
    X = np.random.uniform(-20, 20, size=shape)
    y = np.matmul(X, coef) + intercept
    return X, y


def add_gaussian_noise(
    data: np.ndarray, loc: float = 0, scale: float = 3
) -> np.ndarray:
    """
    Add gaussian noise to an array

    Parameters
    ----------
    data : np.ndarray
        The data to add the noise to
    loc : float, optional
        The location (mean) of the gaussian, by default 0. Usually this should#
        be left as 0.
    scale : float, optional
        The scale (or standard deviation) of the noise, by default 3

    Returns
    -------
    np.ndarray
        Data with noise added
    """
    data = data + np.random.normal(loc=loc, scale=scale, size=data.shape)
    return data


def add_outliers(
    y: np.ndarray,
    outlier_percent: float = 5,
    outlier_mult=3,
) -> np.ndarray:
    """Add outliers to a 1-D observations array"""
    if outlier_percent == 0:
        logger.debug("No outliers being added, function call is redundant")
        return y

    n_samples = y.size
    n_outliers = int((outlier_percent / 100) * n_samples)
    max_y = np.max(y)
    outliers = np.random.uniform(max_y, max_y * outlier_mult, size=n_outliers)
    # signs = np.random.randint(0, 2, size=n_outliers) * 2 - 1
    signs = np.ones_like(outliers)
    outliers = outliers * signs
    # add to observations
    logger.debug(f"Adding {n_outliers=} to observations")
    outlier_indices = np.random.randint(0, n_samples, size=n_outliers)
    y[outlier_indices] = y[outlier_indices] + outliers
    return y


def linear_real_with_leverage():
    pass


def linear_real_with_outliers_and_leverage():
    pass


def plot_1d(
    X: np.ndarray,
    y: np.ndarray,
    coefs: Optional[Dict[str, Tuple[np.ndarray, float]]] = None,
) -> matplotlib.figure.Figure:
    if (Xdim := np.squeeze(X).ndim) != 1:
        raise ValueError(f"{Xdim=} != 1")
    if (ydim := np.squeeze(y).ndim) != 1:
        raise ValueError(f"{ydim=} != 1")

    fig = plt.figure()
    plt.scatter(X, y, label="Observations")
    # plot the parameters
    for label, (coef, intercept) in coefs.items():
        y_pred = X * coef + intercept
        plt.plot(X, y_pred, label=label)
    plt.legend()
    plt.grid()
    return fig


def get_X_plane(X: np.ndarray) -> np.ndarray:
    mins = np.min(X, axis=0)
    maxs = np.max(X, axis=0)
    return np.array(
        [
            [mins[0], mins[1]],
            [mins[0], maxs[1]],
            [maxs[0], maxs[1]],
            [maxs[0], mins[1]],
            [mins[0], mins[1]],
        ]
    )


def plot_2d(
    X: np.ndarray,
    y: np.ndarray,
    coefs: Optional[Dict[str, Tuple[np.ndarray, float]]] = None,
) -> matplotlib.figure.Figure:
    if (Xdim := np.squeeze(X).ndim) != 2:
        raise ValueError(f"{Xdim=} != 2")
    if (ydim := np.squeeze(y).ndim) != 1:
        raise ValueError(f"{ydim=} != 1")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(X[:, 0], X[:, 1], y, label="Observations")
    # plot the planes
    X_plane = get_X_plane(X)
    labels = list(coefs.keys())
    colors = matplotlib.cm.get_cmap("Set2", len(labels)).colors
    for label, color in zip(labels, colors):
        coef, intercept = coefs[label]
        y_pred = np.matmul(X_plane, coef) + intercept
        verts = [list(zip(X_plane[:, 0], X_plane[:, 1], y_pred))]
        poly = Poly3DCollection(verts, facecolors=color, edgecolors=color)
        poly._facecolors2d = poly._facecolor3d
        poly._edgecolors2d = poly._edgecolor3d
        poly.set_label(label)
        poly.set_alpha(0.6)
        ax.add_collection3d(poly)
    plt.grid()
    plt.legend()
    return fig
