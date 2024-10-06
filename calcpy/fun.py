from functools import partial
import math
import operator

from .math import nan
from .op import all_ as _all, any_ as _any, never as _never, odd as _odd, lt as _lt, le as _le, gt as _gt, ge as _ge
from .op import allpairwise  # noqa: F401
from .sequence import perm
from .setlike import eq as _eq, ne as _ne


class permcaller:
    """Callable that swaps position parameters according to cyclc notation.

    Args:
        callable: Callable object.
        cycle: List of indices to swap.

    Results:
        callable

    Examples:
        >>> executor = permcaller(range, cycle=[0, 1])
        >>> executor(3, 2, 6)
        range(2, 3, 6)

        >>> executor = permcaller(range, cycle=[1, 2])
        >>> executor(3, 2, 6)
        range(3, 6, 2)
    """
    def __init__(self, f, cycle=()):
        self.f = f
        self.cycle = cycle

    def __call__(self, *args, **kwargs):
        args = perm(list(args), self.cycle)
        return self.f(*args, **kwargs)


class swapcaller(permcaller):
    """Callable that swaps positional arguments in a pair.

    Args:
        callable: Callable object.
        i (int): Index of the argument to swap.
        j (int): Index of another argument to swap.

    Results:
        callable

    Examples:
        >>> executor = swapcaller(range)
        >>> executor(3, 2, 6)
        range(2, 3, 6)

        >>> executor = swapcaller(range, 1, 2)
        >>> executor(3, 2, 6)
        range(3, 6, 2)
    """
    def __init__(self, f, i=0, j=1):
        super().__init__(f, cycle=[i, j])


def call(f, *args, **kwargs):
    """Call a callable with positional arguments and keyword arguments.

    Args:
        f: Callable object.
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Returns:
        Result of the callable.

    Examples:
        >>> call(range, 2, 3, 6)
        range(2, 3, 6)
    """
    return f(*args, **kwargs)


def merge_args(f):
    """Merge all positional arguments of a function to a single tuple argument

    Args:
        f: Callable object

    Returns:
        Result of the callable

    Examples:
        >>> merge_args(print)([0, 1.0, "Hello"])
        0 1.0 Hello
    """
    def fun(args, **kwargs):
        return f(*args, **kwargs)
    return fun


def demerge_args(f):
    """Replace a single tuple/list argument to many positional arguments.

    Args:
        f: Callable object

    Returns:
        Result of the callable

    Examples:
        >>> demerge_args(all)(True, True, True)
        True
    """
    def fun(*args, **kwargs):
        return f(args, **kwargs)
    return fun


def fillerr(value=None):
    """Decorator that returns a default value if an error occurs.

    Args:
        value: Default value to return if an error occur.

    Returns:
        A callable object.

    Examples:
        >>> @fillerr()
        ... def f(x):
        ...     return 1/x
        >>> f(0)  # Return None, print nothing.
        >>> f(1)
        1.0
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception:
                return value
        return wrapper
    return decorator


def fillwhen(check, value):
    """Decorator that returns a default value if a condition is met.

    Args:
        check: Callable object that checks the condition.
        value: Default value to return if the condition is met.

    Returns:
        A callable object.

    Examples:
        >>> from math import isnan, nan
        >>> @fillwhen(isnan, 0)
        ... def f(x):
        ...     return x
        >>> f(nan)
        0
        >>> f(1)
        1
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if check(result):
                return value
            else:
                return result
        return wrapper
    return decorator


def fillnone(value=nan):
    """Decorator that returns a default value if the result is None.

    Args:
        value: Default value to return if the result is None.

    Returns:
        A callable object.

    Examples:
        >>> @fillnone(-1)
        ... def f(x):
        ...     return x
        >>> f(None)
        -1
        >>> f(nan)
        nan
        >>> f(False)
        False
        >>> f(0)
        0
    """
    def isnone(arg):
        return arg is None

    def decorator(f):
        return fillwhen(isnone, value)(f)
    return decorator


def fillnan(value=0):
    """Decorator that returns a default value if the result is nan.

    Args:
        value: Default value to return if the result is nan.

    Returns:
        A callable object.

    Examples:
        >>> @fillnan(-1)
        ... def f(x):
        ...     return x
        >>> f(None)  # return None, print nothing.
        >>> f(nan)
        -1
        >>> f(False)
        False
        >>> f(0)
        0
    """
    from .math import isnan

    def decorator(f):
        return fillwhen(isnan, value)(f)
    return decorator


def combine(how, *funs):
    """Combine multiple callables into a single callable, using a combining function.

    Args:
        how: Callable object that combines multiple results.
        *funs: Callable objects.

    Returns:
        A callable object.

    Examples:
        >>> from operator import itemgetter
        >>> combine(max, itemgetter(1), itemgetter(2))([3, 4, 5])
        5
        >>> combine(min, itemgetter(1), itemgetter(2))([3, 4, 5])
        4
    """
    def f(*args, **kwargs):
        results = [fun(*args, **kwargs) for fun in funs]
        result = how(*results)
        return result
    return f


def create_combiner(how, name=None):
    combined = partial(combine, how)
    name = name or how.__name__
    combined.__doc__ = f"""
        Combine multiple callables into a single callable, using `{name}`.

        Args:
            *funs: Callable objects.

        Returns:
            A callable object.
        """
    return combined


# Shorthand functions
abs_ = create_combiner(operator.abs)
add = create_combiner(operator.add)
all_ = create_combiner(_all)
and_ = create_combiner(operator.and_)
any_ = create_combiner(_any)
bin_ = create_combiner(bin)
bool_ = create_combiner(bool)
ceil = create_combiner(math.ceil)
concat = create_combiner(operator.concat)
contains = create_combiner(operator.contains)
countOf = create_combiner(operator.countOf)
dict_ = create_combiner(dict)
divmod_ = create_combiner(divmod)
eq = create_combiner(_eq)
float_ = create_combiner(float)
floor = create_combiner(math.floor)
floordiv = create_combiner(operator.floordiv)
format_ = create_combiner(format)
ge = create_combiner(_ge)
getitem = create_combiner(operator.getitem)
gt = create_combiner(_gt)
hex_ = create_combiner(oct)
index = create_combiner(operator.index)
indexOf = create_combiner(operator.indexOf)
int_ = create_combiner(int)
inv = create_combiner(operator.inv)
is_ = create_combiner(operator.is_)
is_not = create_combiner(operator.is_not)
isinstance_ = create_combiner(isinstance)
le = create_combiner(_le)
len_ = create_combiner(len)
list_ = create_combiner(list)
lshift = create_combiner(operator.lshift)
lt = create_combiner(_lt)
matmul = create_combiner(operator.matmul)
max_ = create_combiner(max)
min_ = create_combiner(min)
mod = create_combiner(operator.mod)
mul = create_combiner(operator.mul)
ne = create_combiner(_ne)
neg = create_combiner(operator.neg)
never = create_combiner(_never)
not_ = create_combiner(operator.not_)
oct_ = create_combiner(oct)
odd = create_combiner(_odd)
or_ = create_combiner(operator.or_)
ord_ = create_combiner(ord)
pos = create_combiner(operator.pos)
pow_ = create_combiner(operator.pow)
range_ = create_combiner(range)
round_ = create_combiner(round)
rshift = create_combiner(operator.rshift)
set_ = create_combiner(set)
setitem = create_combiner(operator.setitem)
sorted_ = create_combiner(sorted)
str_ = create_combiner(str)
sub = create_combiner(operator.sub)
sum_ = create_combiner(sum)
truediv = create_combiner(operator.truediv)
truth = create_combiner(operator.truth)
tuple_ = create_combiner(tuple)
type_ = create_combiner(type)
xor = create_combiner(operator.xor)
zip_ = create_combiner(zip)
zip_.__doc__ += """
        Examples:
            >>> list_(zip_(list, list, list))((1, 2, 3))
            [(1, 1, 1), (2, 2, 2), (3, 3, 3)]
        """
