"""Extension of Python operators and functions."""

from copy import copy as shallowcopy, deepcopy
from functools import partial
import operator

from .it import pairwise


def _resolve_attr(obj, attr, default):
    """Auxiliary function for attrgetter. """
    for name in attr.split("."):
        if hasattr(obj, name):
            obj = getattr(obj, name)
        else:
            return default
    return obj


def attrgetter(*items, default=None):
    """Return a callable object that fetches the given attribute(s) from its operand.

    Fully compatible with Python's built-in `operator.attrgetter`,
    and furthermore support default value when a named attr is not found.

    Examples:
        Get attributes with default values.

        >>> from collections import namedtuple
        >>> name = namedtuple('Name', ['first', 'last'])
        >>> name.first = 'Zhiqing'
        >>> name.last = 'Xiao'
        >>> person = namedtuple('Person', ['name', 'city'])
        >>> person.name = name
        >>> person.city = 'Beijing'
        >>> g = attrgetter('name.first', 'name.middle', 'name.last', default='')
        >>> g(person)
        ('Zhiqing', '', 'Xiao')
    """
    if len(items) == 1:
        attr = items[0]

        def g(obj):
            return _resolve_attr(obj, attr, default)
    else:

        def g(obj):
            return tuple(_resolve_attr(obj, attr, default) for attr in items)
    return g


def _resolve_item(obj, item, default):
    """Auxiliary function for itemgetter. """
    if not isinstance(item, list):
        item = [item]
    for i in item:
        try:
            obj = obj[i]
        except KeyError:
            return default
    return obj


def itemgetter(*items, default=None):
    """Return a callable object that fetches the given item(s) from its operand.

    Fully compatible with Python's builtin `operator.itemgetter`,
    and furthermore support multi-level item and a default value when a item is not found.

    Examples:
        Get multiple items with default values.

        >>> person = {'name': {'first': 'Zhiqing', 'last': 'Xiao'}, 'city': 'Beijing'}
        >>> g = itemgetter(['name', 'first'], ['name', 'middle'], ['name', 'last'], default='')
        >>> result = g(person)
        >>> result
        ('Zhiqing', '', 'Xiao')
    """
    if len(items) == 1:
        item = items[0]

        def g(obj):
            return _resolve_item(obj, item, default)
    else:

        def g(obj):
            return tuple(_resolve_item(obj, item, default) for item in items)
    return g


def identity(value, *args, **kwargs):
    """Returns the first positional arguments, and ignore other arguments.

    Examples:
        Return the first position parameter and ignore all other parameters.

        >>> result = identity("value", "other_input", key="other_keyword_input")
        >>> result
        'value'

        The return value is as-is without copying.

        >>> import pandas as pd
        >>> df = pd.DataFrame()
        >>> identity(df) is df
        True
    """
    return value


class constantcreator:
    """Callable that returns the same constant when it is called.

    Examples:
        Always return the string "value".

        >>> creator = constantcreator("value")
        >>> creator()
        'value'

        Create a pd.DataFrame whose elements are all empty lists.

        >>> import pandas as pd
        >>> df = pd.DataFrame(index=range(3), columns=["A"])
        >>> df.map(constantcreator([]))
            A
        0  []
        1  []
        2  []

        Return a new copy when `copy=True`.

        >>> import pandas as pd
        >>> df = pd.DataFrame(index=range(3), columns=["A"])
        >>> constantcreator(df, copy=True)() is df
        False
    """
    def __init__(self, value, copy=False):
        self.value = value
        if copy:
            if copy in ["shallow", shallowcopy]:
                copy = shallowcopy
            else:
                copy = deepcopy
        else:
            copy = identity
        self.copy = copy

    def __call__(self, *args, **kwargs):
        return self.copy(self.value)


def all_(iterable, empty=True):
    """Return True of bool(x) is True for all x in the iterable.

    If the iterable is empty, return what `empty` specifies.

    Args:
        iterable: Iterable object
        empty: the value if the iterable is empty.

    Returns:
        bool

    Examples:
        >>> all_([])
        True
        >>> all_([False])
        False
        >>> all_([True])
        True
        >>> all_([True, False])
        False
        >>> all_([True, True])
        True
    """
    if not iterable:
        return empty
    return all(iterable)


def any_(iterable, empty=False):
    """Return True if bool(x) is True for any x in the iterable.

    If the iterable is empty, return what `empty` specifies.

    Args:
        iterable: Iterable object
        empty: the value if the iterable is empty.

    Returns:
        bool

    Examples:
        >>> any_([])
        False
        >>> any_([False])
        False
        >>> any_([True])
        True
        >>> any_([True, False])
        True
        >>> any_([True, True])
        True
    """
    if not iterable:
        return empty
    return any(iterable)


def never(iterable, empty=True):
    """Return True if bool(x) is False for all x in the iterable.

    If the iterable is empty, return what `empty` specifies.

    Args:
        iterable: Iterable object
        empty: the value if the iterable is empty.

    Returns:
        bool

    Examples:
        >>> never([])
        True
        >>> never([False])
        True
        >>> never([True])
        False
        >>> never([True, False])
        False
        >>> never([True, True])
        False
    """
    if not iterable:
        return True
    return not any(iterable)


def odd(iterable, empty=False):
    """Return True if an odd number of items in the iterable are True.

    If the iterable is empty, return what `empty` specifies.

    Args:
        iterable: Iterable object
        empty: the value if the iterable is empty.

    Returns:
        bool

    Examples:
        >>> odd([])
        False
        >>> odd([False])
        False
        >>> odd([True])
        True
        >>> odd([True, False])
        True
        >>> odd([True, True])
        False
    """
    if not iterable:
        return empty
    import functools
    import operator
    return functools.reduce(operator.xor, iterable)


def and_(*args, empty=True):
    """Return True if all values are True.

    Args:
        *args: values
        empty: The value if there are no values

    Returns:
        bool

    Examples:
        >>> and_()
        True
        >>> and_(True, True)
        True
        >>> and_(True, True, False)
        False
    """
    return all_(args, empty=empty)


def or_(*args, empty=False):
    """Return True if any values are True.

    Args:
        *args: values
        empty: The value if there are no values

    Returns:
        bool

    Examples:
        >>> or_()
        False
        >>> or_(True, True)
        True
        >>> or_(True, True, False)
        True
    """
    return any_(args, empty=empty)


def xor(*args, empty=False):
    """Return True if any values are True.

    Args:
        *args: values
        empty: The value if there are no values

    Returns:
        bool

    Examples:
        >>> xor()
        False
        >>> xor(True)
        True
        >>> xor(True, True, False)
        False
    """
    return odd(args, empty=empty)


def allpairwise(binop, *args, **kwargs):
    """Return True when binary operator returns True for each pair of arguments.

    Args:
        binop: Binary operator
        *args: Arguments
        **kwargs: Keyword arguments

    Returns:
        bool

    Examples:
        >>> import operator
        >>> allpairwise(operator.lt)
        True
        >>> allpairwise(operator.lt, 1)
        True
        >>> allpairwise(operator.lt, 1, 2, 3, 4)
        True
        >>> allpairwise(operator.lt, 1, 2, 2, 4)
        False

    Examples for comparisons:
        >>> lt()
        True
        >>> lt(1)
        True
        >>> lt(1, 2)
        True
        >>> lt(1, 2, 3)
        True
        >>> lt(1, 1)
        False
        >>> lt(1, 1, 2)
        False
        >>> le(1, 1, 2)
        True
        >>> ge(3, 2, 1)
        True
        >>> ge(2, 2, 1)
        True
        >>> gt(2, 2, 1)
        False
        >>> gt(3, 2, 1)
        True
    """
    iterable = (binop(*p, **kwargs) for p in pairwise(args))
    return all_(iterable, empty=True)


"""Comparison functions that supports >=0 arguments. """
lt = partial(allpairwise, operator.lt)
lt.__name__ = "lt"
lt.__doc__ = """
    Return True when all arguments are less than the next argument.

    Args:
        *args: Arguments

    Returns:
        bool

    Examples:
        >>> lt()
        True
        >>> lt(1)
        True
        >>> lt(1, 2)
        True
        >>> lt(1, 2, 3)
        True
        >>> lt(1, 1)
        False
        >>> lt(1, 1, 2)
        False
    """
le = partial(allpairwise, operator.le)
le.__name__ = "le"
le.__doc__ = """
    Return True when all arguments are less than or equal to the next argument.

    Args:
        *args: Arguments

    Returns:
        bool

    Examples:
        >>> le()
        True
        >>> le(1)
        True
        >>> le(1, 2)
        True
        >>> le(1, 2, 3)
        True
        >>> le(1, 1)
        True
        >>> le(1, 1, 2)
        False
    """
ge = partial(allpairwise, operator.ge)
ge.__name__ = "ge"
ge.__doc__ = """
    Return True when all arguments are greater than or equal to the next argument.

    Args:
        *args: Arguments

    Returns:
        bool

    Examples:
        >>> ge()
        True
        >>> ge(1)
        True
        >>> ge(2, 1)
        True
        >>> ge(3, 2, 1)
        True
        >>> ge(1, 1)
        True
        >>> ge(2, 1, 1)
        True
    """
gt = partial(allpairwise, operator.gt)
gt.__name__ = "gt"
gt.__doc__ = """
    Return True when all arguments are greater than the next argument.

    Args:
        *args: Arguments

    Returns:
        bool

    Examples:
        >>> gt()
        True
        >>> gt(1)
        True
        >>> gt(2, 1)
        True
        >>> gt(3, 2, 1)
        True
        >>> gt(1, 1)
        False
        >>> ge(2, 1, 1)
        False
    """
