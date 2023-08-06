from typing import Tuple

import numpy as np
from numba import jit

JIT_FUNCTIONS = True


class conditional_decorator:
    def __init__(self, dec, condition):
        self.decorator = dec
        self.condition = condition

    def __call__(self, func):
        if not self.condition:
            # Return the function unchanged, not decorated.
            return func
        return self.decorator(func)


@conditional_decorator(jit, JIT_FUNCTIONS)
def _glass_wool_side(
    x: np.ndarray, ival: int, mu: float, m2: float, maxstd2: float, k: int
) -> float:
    sgn = 1 if ival == 0 else -1
    while k > 1:
        xval = x[ival]
        z2min = np.square(xval - mu) * (k - 1.0) / m2
        if z2min < maxstd2:
            break
        ival += sgn
        k -= 1
        delta = xval - mu
        mu -= delta / k
        m2 -= delta * (xval - mu)
    return x[ival]


@conditional_decorator(jit, JIT_FUNCTIONS)
def _glass_wool(
    x_in: np.ndarray, maxstd_lower: float, maxstd_upper: float, side: str = "both"
) -> np.ndarray:
    x = np.sort(x_in)
    k = len(x)
    imax = k - 1
    while np.isnan(x[imax]):
        imax -= 1
    k = imax + 1
    imin = 0
    mu = np.nanmean(x)
    m2 = np.nansum(np.square(x - mu))
    maxstd2_lower = maxstd_lower**2
    maxstd2_upper = maxstd_upper**2

    if side == 'lower':
        xival = _glass_wool_side(x, imin, mu, m2, maxstd2_lower, k)
        x[x < xival] = np.nan
        return x
    elif side == 'upper':
        xival = _glass_wool_side(x, imax, mu, m2, maxstd2_upper, k)
        x[x > xival] = np.nan
        return x

    while k > 1:
        xmin = x[imin]
        xmax = x[imax]
        z2min = np.square(xmin - mu) * (k - 1.0) / m2
        z2max = np.square(xmax - mu) * (k - 1.0) / m2
        if z2min < maxstd2_lower and z2max < maxstd2_upper:
            break
        if z2min < maxstd2_lower:
            xdel = xmax
            imax -= 1
        elif z2max < maxstd2_upper:
            xdel = xmin
            imin += 1
        elif z2min < z2max:
            xdel = xmax
            imax -= 1
        else:
            xdel = xmin
            imin += 1
        k -= 1
        delta = xdel - mu
        mu -= delta / k
        m2 -= delta * (xdel - mu)

    x[(x < x[imin]) | (x > x[imax])] = np.nan
    return x


def glasswool(
    x_in: np.ndarray, maxstd: float | Tuple[float, float], side: str = "both"
) -> np.ndarray:
    """Iteratively remove outliers from data.

    Iteratively removes outliers from normally distributed input data until there are no more outliers more than
    `maxstd` standard deviations from the mean.
    The returned array has the same length - outliers are set to ``np.nan``.

    !!! tip "Drop nans after calling glass_wool"
        Use ``x[~np.isnan(x)]`` to remove outliers (``np.nan``) from the returned array.


    Parameters
    ----------
    x_in
        The input data.
    maxstd
        The maximum number of standard deviations allowed for an outlier. If a float is given, the same maximum
        standard deviation is used for the upper and lower sides of the distribution. If a tuple is given and side
        is "both", the first value is used for the lower side and the second value is used for the upper side.
    side
        The side(s) on which to remove outliers. Options are "lower", "upper", or "both" (default).

    Returns
    -------
    numpy.ndarray
        A copy of the input data with outliers set to ``np.nan``.

    Examples
    --------
    Cut values at plus and minus 2 standard deviations from the mean:

    >>> import numpy as np
    >>> from babeldata.common import glass_wool
    >>> x = np.array([1., 442., 443., 444., 445., 446., 447., 448., 449., 900.])
    >>> glass_wool(x, 2.0)
    array([ nan, 442., 443., 444., 445., 446., 447., 448., 449.,  nan])

    Only cut upper outliers:

    >>> glasswool(x, 2.0, side='upper')
    array([  1., 442., 443., 444., 445., 446., 447., 448., 449.,  nan])

    Only cut lower outliers:

    >>> glasswool(x, 2.0, side='lower')
    array([ nan, 442., 443., 444., 445., 446., 447., 448., 449., 900.])

    Use asymmetric upper and lower limits:

    >>> glasswool(x, (2.0, 4.0), 'both')
    array([ nan, 442., 443., 444., 445., 446., 447., 448., 449., 900.])

    Notes
    -----
        - The input data must be a 1D numpy.ndarray.
        - The function is optimized with the @jit decorator for improved performance.
    """

    # Handle inputs
    if not isinstance(x_in, np.ndarray):
        raise ValueError("x_in must be a numpy.ndarray")
    if len(x_in) == 0:
        return x_in
    if isinstance(maxstd, float):
        maxstd_upper = maxstd_lower = maxstd
    elif isinstance(maxstd, tuple) and side == "both":
        if len(maxstd) != 2:
            raise ValueError("maxstd must be a float or a tuple of length 2")
        maxstd_lower, maxstd_upper = maxstd
    else:
        raise ValueError("maxstd must be a float or a tuple if side is 'both'")

    # Call the jitted function
    return _glass_wool(x_in, maxstd_lower, maxstd_upper, side)


if __name__ == '__main__':
    x = np.random.randn(100)
    x[4] = np.nan
    glasswool(x, 2.0, side='both')
