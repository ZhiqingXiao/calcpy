"""Extension of Python operators and functions."""
from copy import copy as shallowcopy, deepcopy
import functools
import operator

from .matcher import _get_matcher
from ._it import pairwise
from ._seq import count_unique


def _resolve_attr(obj, attr, default):
    """Auxiliary function for attrgetter."""
    for name in attr.split("."):
        if hasattr(obj, name):
            obj = getattr(obj, name)
        else:
            return default
    return obj


def attrgetter(*attrs, default=None):
    """Return a callable object that fetches the given attribute(s) from its operand.

    Fully compatible with Python's built-in ``operator.attrgetter``,
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

    See also:
        https://docs.python.org/3/library/operator.html#operator.attrgetter
    """
    if len(attrs) == 1:
        attr = attrs[0]

        def g(obj):
            return _resolve_attr(obj, attr, default)
    else:

        def g(obj):
            return tuple(_resolve_attr(obj, attr, default) for attr in attrs)
    return g


def _resolve_item(obj, item, default):
    """Auxiliary function for itemgetter."""
    if not isinstance(item, list):
        item = [item]
    for i in item:
        try:
            obj = obj[i]
        except (IndexError, KeyError):
            return default
    return obj


def itemgetter(*items, default=None):
    """Return a callable object that fetches the given item(s) from its operand.

    Fully compatible with Python's builtin ``operator.itemgetter``,
    and furthermore support multi-level item and a default value when a item is not found.

    Examples:
        Get multiple items with default values.

        >>> person = {'name': {'first': 'Zhiqing', 'last': 'Xiao'}, 'city': 'Beijing'}
        >>> g = itemgetter(['name', 'first'], ['name', 'middle'], ['name', 'last'], default='')
        >>> g(person)
        ('Zhiqing', '', 'Xiao')
        >>> itemgetter(4, default=0)([1, 2, 3])
        0

    See also:
        https://docs.python.org/3/library/operator.html#operator.itemgetter
    """
    if len(items) == 1:
        item = items[0]

        def g(obj):
            return _resolve_item(obj, item, default)
    else:

        def g(obj):
            return tuple(_resolve_item(obj, item, default) for item in items)
    return g


def methodcaller(name, *args, **kwargs):
    """methodcaller

    Fully compatible with Python's built-in ``operator.methodcaller``.

    Support ``pandas`` accessor.

    Can be decorated by ``calcpy.fillerr`` when needed to resolve the case where method name is not found.

    Examples:
        >>> import pandas as pd
        >>> s = pd.Series(["a", "b"])
        >>> methodcaller("str.upper")(s)
        0    A
        1    B
        dtype: object

    See also:
        https://docs.python.org/3/library/operator.html#operator.methodcaller
    """
    def caller(obj, *args_, **kwargs_):
        return attrgetter(name)(obj)(*args, *args_, **kwargs, **kwargs_)
    return caller


def arggetter(*keys, default=None):
    """Return a callable object that fetches the nth positional argument from its operand.

    Parameters:
        *keys (int | str, for each positional parameter):
            If it is an ``int`` (can be negative), it is the index of the positional argument to be fetched.
            If it is a ``str``, it is the name of keyword argument to be fetched.
        default: Default value to return when the argument is not found.

    Returns:
        callable:

    Examples:
        Get the first positional argument.

        >>> getter = arggetter(0)
        >>> getter("a", "b", "c", key="value")
        'a'

        Get the positional arguments and keyword arguments.

        >>> getter = arggetter(-1, 0, 1, "key", default="default")
        >>> getter("a", "b", "c", key="value")
        ('c', 'a', 'b', 'value')

        Get the positional arguments and keyword arguments with default values.

        >>> getter = arggetter(-1, 0, 1, 5, "key", "other", default="default")
        >>> getter("a", "b", "c", key="value")
        ('c', 'a', 'b', 'default', 'value', 'default')
    """
    def getter(*args, **kwargs):
        results = []
        for key in keys:
            if isinstance(key, str):
                result = kwargs.get(key, default)
            else:
                count = len(args)
                if -count <= key < count:
                    result = args[key]
                else:
                    result = default
            results.append(result)
        if len(results) == 1:
            # If only one result, return it directly
            return results[0]
        return tuple(results)
    return getter


class constantcreator:
    """Callable that returns the same constant when it is called.

    Parameters:
        value : Constant value to be returned.
        copy : If ``True``, return a new copy of the constant value.

    Returns:
        callable: Callable object that returns ``value``, ignoring its parameters.

    Examples:
        Always return the string ``"value"``.

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

        Return a new copy when ``copy=True``.

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
            copy = arggetter(0)
        self.copy = copy

    def __call__(self, *args, **kwargs):
        return self.copy(self.value)


def all_(iterable, empty=True):
    """Return ``True`` of ``bool(x)`` is ``True`` for all ``x`` in the iterable.

    If the iterable is empty, return what ``empty`` specifies.

    Fully compatible with Python's built-in ``all()``.

    Parameters:
        iterable (iterable):
        empty : Value if ``iterable`` is empty.

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

    See also:
        https://docs.python.org/3/library/functions.html#all
    """
    if not iterable:
        return empty
    return all(iterable)


def any_(iterable, *, empty=False):
    """Return ``True`` if ``bool(x)`` is ``True`` for any ``x`` in the iterable.

    If the iterable is empty, return what ``empty`` specifies.

    Fully compatible with Python's built-in ``any()``.

    Parameters:
        iterable (iterable):
        empty : Value if ``iterable`` is empty.

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

    See also:
        https://docs.python.org/3/library/functions.html#any
    """
    if not iterable:
        return empty
    return any(iterable)


def never(iterable, *, empty=True):
    """Return ``True`` if ``bool(x)`` is ``False`` for all ``x`` in the iterable.

    If the iterable is empty, return what ``empty`` specifies.

    Parameters:
        iterable (iterable):
        empty : Value if ``iterable`` is empty.

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


def odd(iterable, *, empty=False):
    """Return ``True`` if an odd number of items in the iterable are ``True``.

    If the iterable is empty, return what ``empty`` specifies.

    Parameters:
        iterable (iterable):
        empty : Value if ``iterable`` is empty.

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

    return functools.reduce(operator.xor, iterable)


def and_(*args, empty=True):
    """Return ``True`` if all values are ``True``.

    Fully compatible with Python's built-in ``operator.and_``.

    Parameters:
        *args
        empty : Value if ``args`` have no values.

    Returns:
        bool:

    Examples:
        >>> and_()
        True
        >>> and_(True, True)
        True
        >>> and_(True, True, False)
        False

    See also:
        https://docs.python.org/3/library/operator.html#operator.and_
    """
    return all_(args, empty=empty)


def or_(*args, empty=False):
    """Return ``True`` if any values are ``True``.

    Fully compatible with Python's built-in ``operator.or_``.

    Parameters:
        *args
        empty : Value if ``args`` have no values.

    Returns:
        bool:

    Examples:
        >>> or_()
        False
        >>> or_(True, True)
        True
        >>> or_(True, True, False)
        True

    See also:
        https://docs.python.org/3/library/operator.html#operator.or_
    """
    return any_(args, empty=empty)


def xor(*args, empty=False):
    """Return ``True`` if any values are ``True``.

    Fully compatible with Python's built-in ``operator.xor``.

    Parameters:
        *args
        empty : Value if ``args`` have no values.

    Returns:
        bool:

    Examples:
        >>> xor()
        False
        >>> xor(True)
        True
        >>> xor(True, True, False)
        False

    See also:
        https://docs.python.org/3/library/operator.html#operator.xor
    """
    return odd(args, empty=empty)


def _allpairwise_glet(glet_name):
    # glet is short for the collection of ["lt", "le", "gt", "ge"].
    glet = getattr(operator, glet_name)

    def f(*args, key=None):
        if key is not None:
            args = (key(arg) for arg in args)
        iterable = (glet(*p) for p in pairwise(args))
        return all(iterable)
    f.__name__ = glet_name
    f.__doc__ = f"""
    Return ``True`` when all arguments are {glet_name} the next argument.

    Fully compatible with Python's built-in ``operator.{glet_name}``.

    Parameters:
        *args
        key (callable):

    Returns:
        bool:

    Examples:
        >>> {glet_name}()
        True
        >>> {glet_name}(1)
        True
        >>> {glet_name}(1, 1)
        {glet(1, 1)}
        >>> {glet_name}(1, 2)
        {glet(1, 2)}
        >>> {glet_name}(2, 1)
        {glet(2, 1)}
        >>> {glet_name}(1, 1, 2)
        {glet(1, 1) and glet(1, 2)}
        >>> {glet_name}(1, 2, 3)
        {glet(1, 2) and glet(2, 3)}
        >>> {glet_name}(3, 2, 1)
        {glet(3, 2) and glet(2, 1)}

    See also:
        https://docs.python.org/3/library/operator.html#operator.{glet_name}
    """
    return f


lt = _allpairwise_glet("lt")
le = _allpairwise_glet("le")
gt = _allpairwise_glet("gt")
ge = _allpairwise_glet("ge")


def eq(*args, key=None):
    """Check whether all parameters are the same.

    Fully compatible with Python's built-in ``operator.eq``.

    Parameters:
        *args
        key (callable)

    Returns:
        bool:

    Examples:
        >>> eq({"a": 1}, {"a": 1}, {"a": 1})
        True
        >>> eq(1, 1, 2, 2)
        False

    See also:
        https://docs.python.org/3/library/operator.html#operator.eq
    """
    distinct_count = count_unique(args, key=key)
    return distinct_count <= 1


def ne(*args, key=None):
    """Check whether all parameters are distinct.

    Fully compatible with Python's built-in ``operator.ne``.

    Parameters:
        *args
        key (callable)

    Returns:
        bool:

    Examples:
        >>> ne([1, 2], [1, 3], [2, 3])
        True
        >>> ne([1, 2], [1, 3], [1, 3])
        False

    See also:
        https://docs.python.org/3/library/operator.html#operator.ne
    """
    original_count = len(args)
    distinct_count = count_unique(args, key=key)
    return original_count == distinct_count


def same(values, key=None):
    """Check whether all elements are the same.

    Parameters:
        values (iterable)
        key (callable)

    Returns:
        bool:

    Examples:
        >>> same([{"a": 1}, {"a": 1}, {"a": 1}])
        True
        >>> same([1, 1, 2, 2])
        False
    """
    return eq(*values, key=key)


def distinct(values, *, key=None):
    """Check whether all elements are distinct.

    Parameters:
        values (iterable)
        key (callable)

    Returns:
        bool:

    Examples:
        >>> distinct([[1, 2], [1, 3], [2, 3]])
        True
        >>> distinct([[1, 2], [1, 3], [1, 3]])
        False
    """
    return ne(*values, key=key)


def _concat(*args, matcher, assemble=True):
    results = []
    for arg in args:
        results += matcher.disassemble(arg)
    if assemble:
        return matcher.assemble(results)
    return results


def concat(*args, key=None):
    """Concat multiple parameters.

    Parameters:
        *args
        key (callable)

    Examples:
        >>> concat([1, 2, 3], [], [4, 5], [5])
        [1, 2, 3, 4, 5, 5]
        >>> concat((1, 2, 3), (), (4, 5), (5,))
        (1, 2, 3, 4, 5, 5)
        >>> concat({1, 2, 3}, set(), {4, 5}, {5})
        {1, 2, 3, 4, 5}
        >>> concat({1: 'a', 2: 'b'}, {}, {3: 'c', 4: 'd'}, {5: 'e'})
        {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}

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
    matcher = _get_matcher(args[0], key=key)
    return _concat(*args, matcher=matcher)
