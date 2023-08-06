"""
Base class for regression in C

The base class implements some basic functions and the abstract classes for
regressors.
"""
from pydantic import BaseModel
import numpy as np


def htranspose(arr: np.ndarray) -> np.ndarray:
    """
    Hermitian transpose of an array (transpose and complex conjugation)

    Parameters
    ----------
    arr : np.ndarray
        Input array

    Returns
    -------
    np.ndarray
        Hermitian transpose
    """
    return np.conjugate(np.transpose(arr))


def sum_square_residuals(X: np.ndarray, y: np.ndarray, coef: np.ndarray) -> float:
    """
    Calculate sum of square residuals

    Parameters
    ----------
    X : np.ndarray
        The regressors
    y : np.ndarray
        The observations
    coef : np.ndarray
        The estimated coefficients

    Returns
    -------
    float
        The sum of square residuals
    """
    residuals = y - np.matmul(X, coef)
    residuals2 = residuals * htranspose(residuals)
    return np.sum(residuals2.real)


class Regressor(BaseModel):
    """Base class for any regressor"""

    class Config:
        arbitrary_types_allowed: bool = True
