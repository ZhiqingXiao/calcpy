"""Extensions to numpy and pandas."""

import numpy as np
import pandas as pd
from pandas.core.generic import NDFrame


def overall_equal(loper, roper):
    """Check whether two operands are exactly equal as a whole.

    It behaves like `np.array_equal` for `np.ndarray`, and
    `loper.equals(roper)` for `pd.Series` and `pd.DataFrame`.

    Parameters:
        loper: number or `np.ndarray` or `pd.Series` or `pd.DataFrame`
        roper: number or `np.ndarray` or `pd.Series` or `pd.DataFrame`

    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({"A": 1, "B": 2}, index=[0])
        >>> overall_equal(df, df+0)
        True
        >>> overall_equal(df, df+1)
        False
        >>> overall_equal(df, df.iloc[:, 0])
        False
        >>> overall_equal(df["A"], df["B"]-1)
        True
    """
    if not isinstance(loper, type(roper)):
        return False
    if isinstance(loper, NDFrame):
        return loper.equals(roper)
    if isinstance(loper, np.ndarray):
        return np.array_equal(loper, roper)
    return loper == roper


def shape(arg):
    """Get the shape of an argument.

    Parameters:
        arg: Any object

    Returns:
        tuple

    Examples:
        >>> shape(1)
        ()
        >>> shape(np.array([1, 2, 3]))
        (3,)
        >>> shape(pd.Series([1, 2, 3]))
        (3,)
        >>> shape(pd.DataFrame({"A": 1, "B": 2}, index=[0]))
        (1, 2)
    """
    return getattr(arg, "shape", ())


def ndim(arg):
    """Get the number of dimensions of an argument.

    Parameters:
        arg: Any object.

    Returns:
        int

    Examples:
        >>> ndim(1)
        0
        >>> ndim(np.array([1, 2, 3]))
        1
        >>> ndim(pd.Series([1, 2, 3]))
        1
        >>> ndim(pd.DataFrame({"A": 1, "B": 2}, index=[0]))
        2
    """
    return getattr(arg, "ndim", 0)


def size(arg):
    """Get the size of an argument.

    Parameters:
        arg: Any object.

    Returns:
        int

    Examples:
        >>> size(1)
        1
        >>> size(np.array([1, 2, 3]))
        3
        >>> size(pd.Series([1, 2, 3]))
        3
        >>> size(pd.DataFrame({"A": 1, "B": 2}, index=[0]))
        2
    """
    return getattr(arg, "size", 1)


def full_like(template, fill_value, **kwargs):
    """Create a np.array or pd.Series or pd.DataFrame with the same shape as template.

    Parameters:
        template: np.ndarray or pd.Series or pd.DataFrame
        fill_value: Any object
        **kwargs: Keyword arguments for np.full_alike, pd.Series, or pd.DataFrame.

    Returns:
        np.ndarray or pd.Series or pd.DataFrame

    Examples:
        >>> full_like(np.array([1, 2, 3]), 0)
        array([0, 0, 0])
        >>> full_like(pd.Series([1, 2, 3]), 0)
        0    0
        1    0
        2    0
        dtype: int64
        >>> full_like(pd.DataFrame({"A": 1, "B": 2}, index=[0]), 0)
              A  B
        0     0  0
    """
    if isinstance(template, np.ndarray):
        return np.full_like(template, fill_value, **kwargs)
    if isinstance(template, pd.Series):
        return pd.Series(fill_value, index=template.index, **kwargs)
    if isinstance(template, pd.DataFrame):
        return pd.DataFrame(fill_value, index=template.index, columns=template.columns, **kwargs)
    raise ValueError("Parameter template needs to be np.ndarry or pd.Series or pd.DataFrame.")
