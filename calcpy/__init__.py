import functools

import numpy as np
import pandas as pd

from .matcher import _get_matcher


def unique(values, matcher=None, **kwargs):
    """ Drop duplications with original order kept """
    if len(values) == 0:
        return values
    if isinstance(values, (list, tuple, set, np.ndarray, pd.Series, pd.DataFrame)):
        matcher = _get_matcher(values, matcher)
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
    return pd.unique(values, **kwargs)


def count_unique(args, matcher=None, **kwargs):
    """ Count the number of distinct elements. """
    result = len(unique(args, matcher=matcher, **kwargs))
    return result


def eq(*args, matcher=None, **kwargs):
    """ Check whether all parameters are the same. """
    distinct_count = count_unique(args, matcher=matcher, **kwargs)
    return distinct_count <= 1


def ne(*args, matcher=None, **kwargs):
    """ Check whether all parameters are distinct. """
    original_count = len(args)
    distinct_count = count_unique(args, matcher=matcher, **kwargs)
    return original_count == distinct_count


def concat(*args, matcher=None):
    """ Concat multiple parameters. """
    if len(args) == 0:
        raise ValueError()
    matcher = _get_matcher(args[0], matcher=matcher)
    results = []
    for arg in args:
        results += matcher.disassemble(arg)
    result = matcher.assemble(results)
    return result


def union(*args, matcher=None, **kwargs):
    """ Union of multiple parameters. """
    return unique(concat(*args), matcher=matcher, **kwargs)


def _wrapper2(fun, matcher):
    def f(loper, roper):
        loper = matcher.disassemble(loper)
        roper = matcher.disassemble(roper)
        results = fun(loper, roper, matcher)
        return matcher.assemble(results)
    return f


def _wrapper(fun):
    def f(*args, matcher=None):
        if len(args) == 0:
            return args
        matcher = _get_matcher(args[0], matcher=matcher)
        return functools.reduce(_wrapper2(fun, matcher), args)
    return f


def _intersect2(loper, roper, matcher):
    results = []
    for l in loper:
        for r in roper:
            if matcher(l, r):
                results.append(l)
                break
    return results


def _exclude2(loper, roper, matcher):
    results = []
    for l in loper:
        for r in roper:
            if matcher(l, r):
                break
        else:
            results.append(l)
    return results


def _xor2(loper, roper, matcher):
    return concat(_exclude2(loper, roper, matcher=matcher), _exclude2(roper, loper, matcher=matcher))


intersect = _wrapper(_intersect2)
""" Intersect of multiple parameters. """

exclude = _wrapper(_exclude2)
""" Exclude follow-up parameters from the first one. """

xor = _wrapper(_xor2)
""" Pick elements that appear in odd number of parameters. """
