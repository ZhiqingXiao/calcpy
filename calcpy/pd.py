"""Extensions to pandas."""

import pandas as pd
from pandas.core.generic import NDFrame  # noqa: F401

from .collect import convert_nested_dict_to_nested_list
from .math import inf, nan
from .nppd import ndim
from .setlike import union


def stack(arg, **kwargs):
    """Stack a `pd.NDFrame` with `future_stack` behavior.

    Stack and silence the `FutureWarning` "The prevoius implementation of stack is deprecated".

    Args:
        arg: pd.DataFrame
        **kwargs: Keyword arguments to be passed to `pd.DataFrame.stack`.

    Returns:
        pd.DataFrame

    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({"A": 1, "B": 2}, index=[0])
        >>> stack(df)
        0 A  1
          B  2
        dtype: int64
    """
    dropna = kwargs.pop("dropna", False)
    try:
        result = arg.stack(future_stack=True, **kwargs)
    except Exception:
        result = arg.stack(dropna=False, **kwargs)
    if dropna:
        result = result.dropna()
    return result


def convert_nested_dict_to_dataframe(data, index_cols=None, columns=None):
    """Convert a nested dictionary to a pandas DataFrame.

    Example:
        >>> data = {"A": {"H": 1, "J": 2}, "E": {"D": 3, "T": 4}}
        >>> convert_nested_dict_to_dataframe(data)
           0  1  2
        0  A  H  1
        1  A  J  2
        2  E  D  3
        3  E  T  4
        >>> convert_nested_dict_to_dataframe(data, index_cols=["v", "c"], columns=["x"])
             x
        v c
        A H  1
          J  2
        E D  3
          T  4
    """
    if index_cols is None:
        index_count = 0
        index_cols = []
    elif isinstance(index_cols, int):
        index_count = index_cols
        index_cols = list(range(index_cols))
    elif isinstance(index_cols, (list, tuple)):
        index_count = len(index_cols)
    else:
        raise ValueError()

    if columns is None:
        if index_count == 0:
            column_count = inf
        else:
            column_count = 1
    elif isinstance(columns, int):
        column_count = columns
    elif isinstance(columns, (list, tuple)):
        column_count = len(columns)
    else:
        raise ValueError()
    maxdepth = index_count + column_count - 1
    lst = convert_nested_dict_to_nested_list(data, maxdepth=maxdepth)
    df = pd.DataFrame(lst)
    if index_count > 0:
        df = df.set_index(list(range(index_count)))
        df.index.names = index_cols
    if isinstance(columns, (list, tuple)):
        df.columns = columns
    else:
        df.columns = list(range(df.shape[1]))
    return df


def convert_series_to_nested_dict(arg):
    """Convert a pandas Series or DataFrame to a nested dictionary.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({"A": 1, "B": [2, 3], "C": [4, 5]}).set_index(["A", "B"])["C"]
        >>> convert_series_to_nested_dict(df)
        {1: {2: 4, 3: 5}}
    """
    if not isinstance(arg, (pd.Series, pd.DataFrame)):
        return arg
    keys = sorted(set(arg.index.get_level_values(0)))
    results = {}
    for key in keys:
        arg0 = arg.loc[key]
        results[key] = convert_series_to_nested_dict(arg0)
    return results

