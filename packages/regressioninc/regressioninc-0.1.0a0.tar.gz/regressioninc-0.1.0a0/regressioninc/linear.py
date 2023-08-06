"""
Regressors for estimating parameters for linear problems

These are built on numpy as numpy.linalg.lstsq does allow and support
complex-valued inputs. However, it does not output residuals for complex-valued
variables, therefore these are calculated out explicitly.
"""
from loguru import logger
from typing import Optional
import numpy as np
import numpy.linalg as linalg
import statsmodels.api as sm

from regressioninc.base import Regressor, sum_square_residuals


def add_intercept(X: np.ndarray) -> np.ndarray:
    """Add an intercept to the regressors

    Parameters
    ----------
    X : np.ndarray
        The regressors

    Returns
    -------
    np.ndarray
        The regressors with an extra column of ones to represent to allow
        solving for the intercept term

    Examples
    --------
    >>> import numpy as np
    >>> from regressioninc.linear import add_intercept
    >>> X = np.array([[2,3], [4,5]])
    >>> X
    array([[2, 3],
           [4, 5]])

    Now add the intercept

    >>> X = add_intercept(X)
    >>> X
    array([[2, 3, 1],
           [4, 5, 1]])
    """
    n_samples = X.shape[0]
    return np.hstack((X, np.ones(shape=(n_samples, 1), dtype=X.dtype)))


def complex_to_glr(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Convert complex-valued linear problem to a real-valued generalised linear
    regression

    Parameters
    ----------
    X : np.ndarray
        The regressors
    y : np.ndarray
        The observations

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        X, y converted to real-valued generalised linear regression

    Examples
    --------
    >>> from regressioninc.linear import add_intercept, complex_to_glr
    >>> X = np.array([3 + 4j, 2 + 8j, 6 + 4j]).reshape(3,1)
    >>> X = add_intercept(X)
    >>> y = np.array([-2 - 4j, -1 - 3j, 5 + 6j])
    >>> X_glr, y_glr = complex_to_glr(X, y)
    >>> X_glr
    array([[ 3., -4.,  1., -0.],
           [ 4.,  3.,  0.,  1.],
           [ 2., -8.,  1., -0.],
           [ 8.,  2.,  0.,  1.],
           [ 6., -4.,  1., -0.],
           [ 4.,  6.,  0.,  1.]])
    >>> y_glr
    array([-2., -4., -1., -3.,  5.,  6.])
    """
    n_samples, n_regressors = X.shape
    # the obesrvations
    y_glr = np.empty(shape=(n_samples * 2), dtype=float)
    y_glr[0::2] = y.real
    y_glr[1::2] = y.imag
    # the regressors
    X_glr = np.empty(shape=(n_samples * 2, n_regressors * 2), dtype=float)
    X_glr[0::2, 0::2] = X.real
    X_glr[0::2, 1::2] = -X.imag
    X_glr[1::2, 0::2] = X.imag
    X_glr[1::2, 1::2] = X.real
    return X_glr, y_glr


def glr_coef_to_complex(coef: np.ndarray) -> np.ndarray:
    """
    Transform coefficients from real to complex-values for complex-valued
    problems that were posed

    Parameters
    ----------
    coef : np.ndarray
        Coefficients array

    Returns
    -------
    np.ndarray
        The complex-valued coefficients

    Examples
    --------
    Let's generate a complex-valued linear problem, pose it as a linear problem
    and then convert the returned coefficients back to complex

    Generate the linear problem and add an intercept column to the regressors

    >>> import numpy as np
    >>> np.set_printoptions(precision=3, suppress=True)
    >>> from regressioninc.testing.complex import ComplexGrid, generate_linear_grid
    >>> from regressioninc.linear import add_intercept, LeastSquares
    >>> from regressioninc.linear import complex_to_glr, glr_coef_to_complex
    >>> coef = np.array([3 + 2j])
    >>> grid = ComplexGrid(r1=-1, r2=1, nr=3, i1=4, i2=6, ni=3)
    >>> X, y = generate_linear_grid(coef, [grid], intercept=10)
    >>> X = add_intercept(X)

    Convert the complex-valued problem to a real-valued problem

    >>> X_glr, y_glr = complex_to_glr(X, y)

    Solve the real-valued linear problem

    >>> model = LeastSquares()
    >>> model.fit(X_glr, y_glr)
    LeastSquares...

    Look at the real-valued coefficients

    >>> model.coef
    array([ 3.,  2., 10.,  0.])

    Convert the coefficients back to the complex domain

    >>> glr_coef_to_complex(model.coef)
    array([ 3.+2.j, 10.+0.j])
    """
    return coef[0::2] + 1j * coef[1::2]


# def leverage_weights(X: np.ndarray) -> np.ndarray:
#     """Get weights to weight down leverage"""
#     n = X.shape[0]
#     q, r = linalg.qr(X)
#     pdiag = np.empty(shape=(n), dtype="float")
#     for i in range(0, n):
#         pdiag[i] = np.absolute(np.sum(q[i, :] * np.conjugate(q[i, :]))).real
#     del q, r
#     pdiag = pdiag / np.max(pdiag)
#     leverageScale = mad0(pdiag)
#     return get_weights(pdiag / leverageScale, "huber")


class LinearRegressor(Regressor):
    """Base class for LinearRegression"""

    coef: Optional[np.ndarray] = None
    """The coefficients"""
    residuals: Optional[np.ndarray] = None
    """The square residuals"""
    rank: Optional[int] = None
    """The rank of the predictors"""
    singular: Optional[np.ndarray] = None
    """The singular values of the predictors"""

    def fit(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Fit the linear model"""
        raise NotImplementedError("fit is not implemented in the base class")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict using the linear model

        Parameters
        ----------
        X : np.ndarray
            The predictors

        Returns
        -------
        np.ndarray
            The predicted observations

        Raises
        ------
        ValueError
            If the coefficients are None. This is most likely the case if the
            model has not been fitted first.
        """
        if self.coef is None:
            raise ValueError(f"{self.coef=}, fit the model first")
        return np.matmul(X, self.coef)

    def fit_predict(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Fit and predict on predictors X and observations y

        Parameters
        ----------
        X : np.ndarray
            The predictors to use for the fit and predict
        y : np.ndarray
            The observations for the fit

        Returns
        -------
        np.ndarray
            The predicted observations
        """
        self.fit(X, y)
        return self.predict(X)


class LeastSquares(LinearRegressor):
    """Standard linear regression"""

    def fit(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Fit the linear problem using least squares regression

        Parameters
        ----------
        X : np.ndarray
            The predictors
        y : np.ndarray
            The observations

        Returns
        -------
        np.ndarray
            The coefficients
        """
        result = linalg.lstsq(X, y, rcond=None)
        self.coef, _residuals, self.rank, self.singular = result
        self.residuals = sum_square_residuals(X, y, self.coef)
        return self


class WeightedLeastSquares(LinearRegressor):
    r"""
    Transform X and y using the weights to perform a weighted least squares

    .. math::
        \sqrt{weights} y = \sqrt{weights} X coef ,

    is equivalent to,

    .. math::
        X^H weights y = X^H weights X coef ,

    where :math:`X^H` is the hermitian transpose of X.

    In this method, both the observations y and the predictors X are multipled
    by the square root of the weights and then returned.
    """

    def fit(self, X: np.ndarray, y: np.ndarray, weights: np.ndarray) -> np.ndarray:
        """
        Apply weights to observations and predictors and find the coefficients
        of the linear model

        Parameters
        ----------
        X : np.ndarray
            The predictors
        y : np.ndarray
            The observations
        weights : np.ndarray
            The weights to apply to the samples

        Returns
        -------
        np.ndarray
            The coefficients for the model

        Raises
        ------
        ValueError
            If the size of weights does not match the size of the observations
            y
        """
        if weights.size != y.size:
            raise ValueError(f"{weights.size=} != {y.size=}")
        weights_sqrt = np.sqrt(weights)
        y = weights_sqrt * y
        X = X * weights_sqrt[..., np.newaxis]
        result = linalg.lstsq(X, y, rcond=None)
        self.coef, _residuals, self.rank, self.singular = result
        self.residuals = sum_square_residuals(X, y, self.coef)
        return self.coef


class M_estimate(LinearRegressor):

    n_iter: int = 50
    early_stopping: float = 0.00001

    def fit(self, X: np.ndarray, y: np.ndarray):
        model = WeightedLeastSquares()
        weigher = sm.robust.norms.TrimmedMean()
        weights = np.ones_like(y)
        prev_resids = None
        iteration = 0
        while iteration < self.n_iter:
            model.fit(X, y, weights=weights)
            logger.debug(f"{iteration=}: {model.residuals=}")
            abs_resids = np.absolute(y - model.predict(X))

            # check residuals, calculate scale, and next set of weights
            if np.sum(abs_resids) < self.early_stopping:
                break
            scale = sm.robust.scale.mad(abs_resids)
            if scale == 0.0:
                logger.warning(f"{scale=} suggesting near perfect fit last iteration")
                break
            weights = weigher.weights(abs_resids / (scale)).astype(abs_resids.dtype)
            iteration = iteration + 1

            # early stopping if no change in residuals
            if prev_resids is None:
                prev_resids = abs_resids
                continue
            delta_resids = linalg.norm(abs_resids - prev_resids)
            delta_resids /= linalg.norm(abs_resids)
            if delta_resids < self.early_stopping:
                break
            prev_resids = abs_resids

        self._set_attributes(model)
        return self.coef

    def _set_attributes(self, model: LinearRegressor) -> None:
        """Set parameters from another model"""
        self.coef = model.coef
        self.residuals = model.residuals
        self.rank = model.rank
        self.singular = model.singular


class MM_estimate(LinearRegressor):
    def fit(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Two stage M estimate"""


class ComplexAsGLR(LinearRegressor):
    def fit(self, X, y, model):
        X_glr, y_glr = complex_to_glr(X, y)
        model.fit(X_glr, y_glr)
        self.coef = glr_coef_to_complex(model.coef)
        self.residuals = sum_square_residuals(X, y, self.coef)
        self.rank = model.rank
        self.singular = model.singular
        return self
