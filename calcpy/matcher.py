import operator
from operator import methodcaller
import six

import numpy as np
import pandas as pd

from .op import attrgetter, itemgetter
from .nppd import overall_equal


class Matcher(object):
    def __init__(self, matcher=None):
        self.matcher = matcher or operator.eq

    def disassemble(self, values):
        return list(values)

    def __call__(self, loper, roper):
        return self.matcher(loper, roper)


class SimpleMatcher(Matcher):
    def __init__(self, matcher=None, assemble=None):
        self.matcher = matcher or operator.eq
        self.assemble = assemble


class DictMatcher(Matcher):
    def disassemble(self, values):
        if hasattr(values, "items"):
            return values.items()  # Python 3
        return values.iteritems()  # Python 2

    def __call__(self, loper, roper):
        return self.matcher(loper[0], roper[0])

    def assemble(self, args):
        return {key: value for key, value in args}


class NumpyArrayMatcher(SimpleMatcher):
    def __init__(self, matcher=None):
        self.matcher = matcher or np.array_equal
        self.assemble = np.concatenate

    def disassemble(self, values):
        count = len(values)
        results = [values[i:i+1] for i in range(count)]
        return results


class PandasFrameMatcher:
    """Matcher class for pd.DataFrame."""
    def __init__(self, method="object", axis=0, matcher=None, **kwargs):
        """Constructor

        Args:
            method (str): can be `"object"`, `"series"`, `"index"`.
                `"object"` means comparing the whole `pd.DataFrame` object.
                `"series"` means comparing the whole `pd.Series`, which is equivalent
                to a row (when axis=1) or a column (when axis=0).
                `"index"` means comparing the index value (when axis=0) or
                column value (when axis=1) only.
                `"value"` means comparing the values of some columns (when axis=0) or
                rows (when axis=1)
            axis (int or str): can be 0 ("index") or 1 ("column")
            matcher (callable): a binary function
            **kwargs : keyword arguments as of `pd.DataFrame.drop_duplicates()`.
                Only used when `method="value"`.
        """
        self.method = method
        self.kwargs = kwargs
        self.transpose = axis in [1, "columns"]
        if matcher is None:
            if method in ["object", "series"]:
                matcher = overall_equal
            elif method in ["index"]:
                matcher = operator.eq
        self.matcher = matcher

    def disassemble(self, values):
        if self.transpose:
            values = values.T
        count = len(values)
        results = [values.iloc[i:i+1] for i in range(count)]
        return results

    def __call__(self, loper, roper):
        if self.method == "object":
            return self.matcher(loper, roper)
        if self.method == "index":
            return self.matcher(loper.index[0], roper.index[0])
        if self.method == "value":
            concated = pd.concat([loper, roper])
            uniqued = concated.drop_duplicates(**self.kwargs)
            return len(uniqued) < len(concated)
        if self.method == "series":
            return self.matcher(loper, roper)

    def assemble(self, args):
        results = pd.concat(args)
        if self.transpose:
            results = results.T
        return results


def _get_matcher(arg, matcher=None):
    if isinstance(matcher, Matcher):
        return matcher
    if isinstance(arg, (list, tuple, set)):
        return SimpleMatcher(matcher=matcher, assemble=type(arg))
    if isinstance(arg, dict):
        return DictMatcher(matcher=matcher)
    if isinstance(arg, six.string_types):
        return SimpleMatcher(matcher=matcher, assemble="".join)
    if isinstance(arg, np.ndarray):
        return NumpyArrayMatcher(matcher=matcher)
    if isinstance(arg, (pd.Series, pd.DataFrame)):
        return PandasFrameMatcher(matcher=matcher)
    raise NotImplementedError()


def from_callable(callable, *args, **kwargs):
    """Convert a callable to a binary comparison function.

    Args:
        callable (callable): A unary function that returns something can be compared by `__eq___`.
        *args: Arguments for `callable`.
        **kwargs: Keyword arguments for `callable`.

    Returns:
        callable: A binary function that checks whether its two arguments are equal.

    Examples:
        >>> matcher = from_callable(len)
        >>> matcher("Hello", "World")
        True
        >>> matcher("Hello", "Python")
        False
    """
    def matcher(loper, roper):
        lresult = callable(loper, *args, **kwargs)
        rresult = callable(roper, *args, **kwargs)
        return lresult == rresult
    return matcher


def from_attrgetter(attr, default=None):
    """Convert an attribute name to a matcher.

    Alias of from_callable(attrgetter(attr, default))

    Args:
        attr (str): Attribute name
        default: Default value if the attribute does not exist.

    Returns:
        A matcher that checks whether its two arguments are equal.

    Examples:
        >>> import numpy as np
        >>> matcher = from_attrgetter("shape")
        >>> matcher(np.array([1, 2, 3]), np.array([4, 5, 6]))
        True
    """
    callable = attrgetter(attr, default=default)
    return from_callable(callable)


def from_dict(mapper, default=None):
    """Convert a dict to a matcher.

    Alias of from_callable(mapper.__getitem__)

    Args:
        mapper (dict): A dict that maps arguments to values.
        default: Default value if the argument does not exist.

    Returns:
        A matcher that checks whether its two arguments are equal.

    Examples:
        >>> matcher = from_dict({'a': 1, 'b': 2, 'c': 1})
        >>> matcher('a', 'b')
        False
        >>> matcher('a', 'c')
        True
    """
    def fun(arg):
        return mapper.get(arg, default)
    return from_callable(fun)


def from_itemgetter(item, default=None):
    """Convert an itemgetter to a matcher.

    Alias of from_callable(itemgetter(item, default))

    Args:
        item (str): Item name
        default: Default value if the item does not exist.

    Returns:
        A matcher that checks whether its two arguments are equal.

    Examples:
        >>> matcher = from_itemgetter("Sex")
        >>> matcher({'Name': 'Peter', 'Sex': 'M'}, {'Name': 'John', 'Sex': 'M'})
        True
        >>> matcher({'Name': 'Marry', 'Sex': 'S'}, {'Name': 'Tom', 'Sex': 'M'})
        False
    """
    callable = itemgetter(item, default=default)
    return from_callable(callable)


def from_methodcaller(name, *args, **kwargs):
    """Convert a method name to a matcher.

    Alias of from_callable(methodcaller(name, *args, **kwargs))

    Args:
        name (str): Method name
        *args: Arguments for `methodcaller`.
        **kwargs: Keyword arguments for `methodcaller`.

    Returns:
        A matcher that checks whether its two arguments are equal.

    Examples:
        >>> matcher = from_methodcaller("upper")
        >>> matcher("Hello", "hello")
        True
    """
    callable = methodcaller(name, *args, **kwargs)
    return from_callable(callable)
