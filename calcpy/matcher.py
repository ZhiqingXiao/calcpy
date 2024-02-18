import operator

import numpy as np
import pandas as pd


class Matcher:
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


class NumpyArrayMatcher(SimpleMatcher):
    def __init__(self, matcher=None):
        self.matcher = matcher or np.array_equal
        self.assemble = np.concatenate

    def disassemble(self, values):
        count = len(values)
        results = [values[i:i+1] for i in range(count)]
        return results


def pd_frame_equal(loper, roper):
    return loper.equals(roper)


class PandasFrameMatcher:
    def __init__(self, method="object", axis=0, matcher=None, **kwargs):
        self.method = method
        self.kwargs = kwargs
        self.transpose = axis in [1, "columns"]
        if matcher is None:
            if method in ["object", "series"]:
                matcher = pd_frame_equal
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
    if isinstance(arg, np.ndarray):
        return NumpyArrayMatcher(matcher=matcher)
    if isinstance(arg, (pd.Series, pd.DataFrame)):
        return PandasFrameMatcher(matcher=matcher)
    raise NotImplementedError()
