from copy import copy
from collections import defaultdict
import functools
import six

import numpy as np
import pandas as pd

from .matcher import _get_matcher


def _unique_sequence(values, matcher=None, dissemble=True):
    if dissemble:
        values = matcher.disassemble(values)
    results = []
    for value in values:
        for result in results:
            if matcher(result, value):
                break
        else:
            results.append(value)
    results = matcher.assemble(results)
    return results


def unique(values, matcher=None):
    """Drop duplications with original order kept.

    Parameters:
        values: iterable
        matcher: matcher

    Results:
        unique values

    Example:
        >>> unique([1, 2, 2, 3, 2, 1, 2])
        [1, 2, 3]
        >>> unique((1, 2, 2, 3, 2, 1, 2))
        (1, 2, 3)
        >>> unique('Hello')
        'Helo'
    """
    if len(values) == 0 or isinstance(values, dict):
        return values
    if isinstance(values, (six.string_types, list, tuple, set, np.ndarray, pd.Series, pd.DataFrame)):
        matcher = _get_matcher(values, matcher)
        return _unique_sequence(values, matcher=matcher)
    return pd.unique(values)


def count_unique(values, matcher=None):
    """Count the number of distinct elements.

    Parameters:
        values: iterable
        matcher: matcher

    Results:
        number of distinct elements

    Examples:
        >>> count_unique([1, 2, 2, 3, 2, 1, 2])
        3
        >>> count_unique('Hello')
        4
    """
    result = len(unique(values, matcher=matcher))
    return result


def eq(*args, matcher=None):
    """Check whether all parameters are the same.

    Parameters:
        *args: iterable
        matcher: matcher

    Results:
        bool

    Examples:
        >>> eq({"a": 1}, {"a": 1}, {"a": 1})
        True
        >>> eq(1, 1, 2, 2)
        False
    """
    distinct_count = count_unique(args, matcher=matcher)
    return distinct_count <= 1


def ne(*args, matcher=None):
    """Check whether all parameters are distinct.

    Parameters:
        *args: iterable
        matcher: matcher

    Results:
        bool

    Examples:
        >>> ne([1, 2], [1, 3], [2, 3])
        True
        >>> ne([1, 2], [1, 3], [1, 3])
        False
    """
    original_count = len(args)
    distinct_count = count_unique(args, matcher=matcher)
    return original_count == distinct_count


def same(values, matcher=None):
    """Check whether all elements are the same.

    Parameters:
        values: iterable
        matcher: matcher

    Results:
        bool

    Examples:
        >>> same([{"a": 1}, {"a": 1}, {"a": 1}])
        True
        >>> same([1, 1, 2, 2])
        False
    """
    return eq(*values, matcher=matcher)


def distinct(values, matcher=None):
    """Check whether all elements are distinct.

    Parameters:
        values: iterable
        matcher: matcher

    Results:
        bool

    Examples:
        >>> distinct([[1, 2], [1, 3], [2, 3]])
        True
        >>> distinct([[1, 2], [1, 3], [1, 3]])
        False
    """
    return ne(*values, matcher=matcher)


def _concat(*args, matcher, assemble=True):
    results = []
    for arg in args:
        results += matcher.disassemble(arg)
    if assemble:
        return matcher.assemble(results)
    return results


def concat(*args, matcher=None):
    """Concat multiple parameters.

    Parameters:
        *args: iterable
        matcher: matcher

    Examples:
        >>> concat([1, 2, 3], [], [4, 5], [5])
        [1, 2, 3, 4, 5, 5]
        >>> concat((1, 2, 3), (), (4, 5), (5,))
        (1, 2, 3, 4, 5, 5)

        >>> import pandas as pd
        >>> s = pd.Series([0, 1])
        >>> concat(s, s)
        0    0
        1    1
        0    0
        1    1
        dtype: int64
    """
    if len(args) == 0:
        raise ValueError()
    matcher = _get_matcher(args[0], matcher=matcher)
    return _concat(*args, matcher=matcher)


def union(*args, matcher=None):
    """Union of multiple parameters.

    This function can merge multiple `dict`s into one `dict`. If two `dict`s
    `d1` and `d2` have the same key `k`, `union(d1, d2)` will use the value of
    `d1[k]` rather than `d2[k]`, which differs from `d1 | d2` who takes `d2[k]`.

    Parameters:
        *args: iterable
        matcher: matcher

    Examples:
        >>> union([1, 2, 3], [3, 2], [2, 4], [])
        [1, 2, 3, 4]
        >>> union((1, 2, 3), (3, 2), (2, 4), ())
        (1, 2, 3, 4)

        The following example considers a list and moves some of its elements to the front.

        >>> a = [1, 2, 3, 4, 5]  # the list
        >>> f = [3, 4]  # some elements that need to appear first
        >>> union(f, a)
        [3, 4, 1, 2, 5]

        Union of multiple `dict`'s:

        >>> union({'a': 1, 'b': 2}, {'c': 13, 'a': 11}, {})
        {'a': 1, 'b': 2, 'c': 13}

        Use a matcher:

        >>> from calcpy.matcher import from_callable
        >>> matcher = from_callable(len)  # compare the length of each element
        >>> union(["alpha", "beta"], ["gamma", "delta"], ["pi", "omega"], matcher=matcher)
        ['alpha', 'beta', 'pi']
    """
    matcher = _get_matcher(args[0], matcher=matcher)
    concated = _concat(*args, matcher=matcher, assemble=False)
    return _unique_sequence(concated, matcher=matcher, dissemble=False)


def _wrapper2(fun, matcher):
    def f(loper, roper):
        loper = matcher.disassemble(loper)
        roper = matcher.disassemble(roper)
        results = fun(loper, roper, matcher)
        return matcher.assemble(results)
    return f


def _wrapper(fun):
    """Extend binary function to multi-ary function."""
    def f(*args, matcher=None):
        if len(args) == 0:
            return args
        matcher = _get_matcher(args[0], matcher=matcher)
        return functools.reduce(_wrapper2(fun, matcher), args)
    return f


def _wrapper_1dict(fun):
    """Support the case when the first parameter is a dict."""
    def f(*args, matcher=None):
        op = _wrapper(fun)
        if len(args) >= 1 and isinstance(args[0], (dict, defaultdict)):
            arg = args[0]
            arglist = list(arg)
            params = list(args)
            params[0] = arglist
            keys = op(*params, matcher=matcher)
            results = copy(arg)
            for key in arglist:
                if key not in keys:
                    results.pop(key)
            return results
        return op(*args, matcher=matcher)
    return f


def _intersect2(loper, roper, matcher):
    results = []
    for l in loper:  # noqa: E741
        for r in roper:
            if matcher(l, r):
                results.append(l)
                break
    return results


def _exclude2(loper, roper, matcher):
    results = []
    for l in loper:  # noqa: E741
        for r in roper:
            if matcher(l, r):
                break
        else:
            results.append(l)
    return results


def _symmetricdiff2(loper, roper, matcher):
    return concat(_exclude2(loper, roper, matcher=matcher), _exclude2(roper, loper, matcher=matcher))


intersect = _wrapper_1dict(_intersect2)
intersect.__doc__ = \
    """Intersect of multiple parameters.

    The first argument can be a `dict`, while the following positions can not
    be a `dict`. If the first argument is a `dict`, it means to limit the keys
    of the first arugment within the list specified by the intersection of
    follow-up position arguments (if any).

    Parameters:
        *args: iterable
        matcher: matcher

    Examples:
        >>> intersect('abcd', 'edc')
        'cd'

        The case when the first argument is a `dict`.

        >>> intersect({'a': 1, 'b': 2, 'c': 3})
        {'a': 1, 'b': 2, 'c': 3}
        >>> intersect({'a': 1, 'b': 2, 'c': 3}, ['a', 'c'])
        {'a': 1, 'c': 3}
    """

exclude = _wrapper_1dict(_exclude2)
exclude.__doc__ = \
    """Exclude follow-up parameters from the first one.

    The first argument can be a `dict`, while the following positions can not
    be a `dict`. If the first argument is a `dict`, it means to exclude all
    elements in the follow-up arguments out of the key of the first position
    argument.

    Parameters:
        *args: iterable
        matcher: matcher

    Examples:
        >>> exclude('abcd', 'cat', 'bed')
        ''

        The case when the first argument is a `dict`.

        >>> exclude({'a': 1, 'b': 2, 'c': 3})
        {'a': 1, 'b': 2, 'c': 3}
        >>> exclude({'a': 1, 'b': 2, 'c': 3}, ['b'])
        {'a': 1, 'c': 3}
    """

symmetricdiff = _wrapper(_symmetricdiff2)
symmetricdiff.__doc__ = \
    """Pick elements that appear in odd number of parameters.

    Parameters:
        *args: iterable
        matcher: matcher

    Examples:
        >>> symmetricdiff([1, 2, 3], [2, 3, 4], [3, 4])
        [1, 3]
        >>> symmetricdiff('hello', 'he', 'okay')
        'llkay'
    """
