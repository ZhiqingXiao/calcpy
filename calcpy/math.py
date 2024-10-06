try:
    from math import tau
except ImportError:
    from math import pi
    tau = 2 * pi

try:
    from math import inf
except ImportError:
    inf = float('inf')

try:
    from math import nan
except ImportError:
    nan = float('nan')


def isnan(value):
    """Check if a value is NaN.

    Support all types.

    Args:
        value: Any value.

    Returns:
        True if the value is NaN, False otherwise.

    Example:
        >>> isnan(None)
        False
        >>> isnan(float('nan'))
        True
        >>> isnan(1)
        False
        >>> isnan("a")
        False
    """
    from .fun import fillerr
    import numpy as np
    checker = fillerr(False)(np.isnan)
    return checker(value)
