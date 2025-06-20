# calcpy: Facility for Python Calculation


`calcpy` is a Python package for calculations.

Main features:

- Extended Python built-in functions, including extended `set` operations, extended `str` operations, extended math functions.
- Argument decorators: Reorganize function arguments.
- Function compositions: Combine multiple callable into one callable.
- Return-value decorations: If the function raises an error or returns invalid values such as `None` and `nan`, fill the values with designated values.
- Unified APIs supporting both Python built-in types and numpy&pandas types.
- Order theory: Implementations of some concepts and algorithms in order theory.


### Documentation

Online Documentation: https://zhiqingxiao.github.io/calcpy/

Third-party AI-generated documentation (not maintained by the author): [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ZhiqingXiao/calcpy)


### Installation

It is recommended to install `calcpy` via pip.

```shell
pip install --upgrade calcpy
```

Python 3.8+ is required. [detail](https://zhiqingxiao.github.io/calcpy/compat.html)

### Features

#### Function Composition

*Function compositions* combines multiple callable into one callable.

Documentation: https://zhiqingxiao.github.io/calcpy/compo.html

- `calcpy.componentize(how)` decorates a callable function so that it becomes a building block of function composition.

Examples:
```python
>>> from calcpy import itemgetter
>>> enable_composition()
>>> max_ = componentize(max)
>>> max_(itemgetter(1), 7, itemgetter(2, default=3))([3, 4, 5])
7
>>> min_ = componentize(min)
>>> min_(itemgetter(1), 7, itemgetter(2, default=3))([3, 4, 5])
4
>>> min_(3, 4, 5)
3
```

``calcpy`` also provides many ready-made components for function compositions. List of APIs: https://zhiqingxiao.github.io/calcpy/compo.html#shorthand-functions-that-support-composition

Examples:
```python
>>> from calcpy import add, enable_composition, itemgetter
>>> enable_composition()
>>> add(itemgetter(1), itemgetter(6, default=3), 10)([3, 4, 5])
19
>>> from calcpy import arggetter
>>> add(arggetter(0), arggetter(1))(3, 4)
7
```

#### Reorganize Arguments of Callable

Documentation: https://zhiqingxiao.github.io/calcpy/fun.html#reorder-arguments

`calcpy` provides several decorators to re-organize parameters of a callable.

- `calcpy.fun.cycleperm(cycle=())` is a decorator that swaps positional arguments of a callable according to a cyclc notation. By default, it does not permutate anything.
- `calcpy.fun.swap(i=0, j=1)` is a decorator that swaps `i`-th positional argument and `j`-th positional argument of a callable. By default, it permutates the first two arguments of the callable.
- `calcpy.fun.dispatch(dispatcher, agg=None, fix_begin=0)` is a decorator that dispatches a callable according to a dispatcher, with parameters to fix first few positional arguments, and an aggregation function to aggregate the final result.
- `calcpy.fun.pack` is a decorator that merges all positional arguments of a function to a single tuple argument.
- `calcpy.fun.unpack` is a decorator that converts a single tuple/list argument to many positional arguments.
- `calcpy.fun.prioritize()` is a decorator that move some positional arguments to the beginning of argument list.

Examples:

```python
>>> from calcpy.fun import swap
>>> @swap()  # the decorator that swaps the first two positional arguments
... def g(a, b):
...    return range(a, b)
>>> g(4, 2)
range(2, 4)
>>> # Equivalent to:
>>> swapper = swap()
>>> swapped_range = swapper(range)
>>> swapped_range(4, 2)
range(2, 4)
```

```python
>>> from calcpy.fun import dispatch
>>> from itertools import pairwise   # For old Python version: from more_itertools import pairwise
>>> @dispatch(pairwise, agg=all)  # the decorator that extends a binop bool checker to arbitrary number of arguments
... def fraceq(a, b):
...     return (a % 1) == (b % 1)
>>> fraceq()  # return True when there are <=1 arugments, since pairwise() returns an empty iterator
True
>>> fraceq(1.1, 2.1)
True
>>> fraceq(1.1, 2.1, 3.1, 4.1)
True
```

#### Extended Set Functions

Set-alike APIs operate objects with original order reserved and optional customized comparison function.

Documentation: https://zhiqingxiao.github.io/calcpy/set.html

- `calcpy.union(*args, key=None)` returns the union of multiple arguments.
- `calcpy.intersect(*args, key=None)` returns intersection of multiple arguments.
- `calcpy.difference(arg, *args, key=None)` removes follow-up arguments from the first.
- `calcpy.symmetric_difference(*args, key=None)` returns the symmetric difference (a.k.a exclusive-or) of multiple arguments.
- `calcpy.isdisjoint(*args, key=None)` checks whether arguments are disjoint.
- `calcpy.ispropersubset(*args, key=None)` checks whether the former parameter is a proper subset of the later parameter.
- `calcpy.ispropersuperset(*args, key=None)` checks whether the former parameter is a proper superset of the later parameter.
- `calcpy.issubset(*args, key=None)` checks whether the former parameter is a subset of the later parameter.
- `calcpy.issuperset(*args, key=None)` checks whether the former parameter is a superset of the later parameter.


Examples:
```Python
>>> from calcpy import union
>>> union([4, 3], [7, 3], [4])
[4, 3, 7]
```

Other functions with similar signatures:

- `calcpy.eq(*args, key=None)` checks whether positional arguments are all equal.
- `calcpy.ne(*args, key=None)` checks whether positional arguments are all distinct.
- `calcpy.concat(*args, key=None)` concatenates multiple arguments.

Functions apply on the only positional argument:

- `calcpy.same(values, key=None)` checks whether all elements in the first positional argument are all equal.
- `calcpy.distinct(values, key=None)` checks whether all elements in the first positional argument are all distinct.
- `calcpy.unique(values, key=None)` removes duplicated entries.

Examples:
```Python
>>> from calcpy import unique
>>> unique([4, 3, 7, 3, 4])
[4, 3, 7]
```

*Supported object types*:
`list`, `tuple`, `set`, `str`, `np.ndarray`, `pd.Series`, `pd.DataFrame`, and more.

*`union()`, `intersection()`, and `difference()` for `dict`*:

- `calcpy.intersection()` and `calcpy.difference()` support first argument of type `dict` and follow-up arguments as type `list`. In those cases, it means that limit the keys of the `dict` with a list or exclude lists out of the dict.

- `calcpy.union()` can merge multiple `dict`s into one `dict`. If two `dict`s `d1` and `d2` have the same key `k`, `union(d1, d2)` will use the value of `d1[k]` rather than `d2[k]`, which differs from `d1 | d2` who takes `d2[k]`.

Examples:
```python
>>> from calcpy import intersection, difference
>>> d = {"a": 1, "b": 2}
>>> l = ["a", "c"]
>>> intersection(d, l)
{"a": 1}
>>> difference(d, l)
{"b": 2}
```

*Customized comparison*:
The keyword parameter `key` is used for customized comparison function.
By default, it is `None`, which uses the default way to compare two objects, i.e. compare them as a whole. It is the same as `calcpy.overall_equal()`. The function `calcpy.overall_equal()` behaves like `np.array_equal()` or `np.ndarray`s, and like `loper.equals(roper)` for `pd.Series`s and `pd.DataFrame`s.

`calcpy` supports customized key functions for object comparison. For example, the following examples compare `str`s according to their lowercases:

```python
>>> from calcpy import eq
>>> eq("Hello", "hello", "HELLO", key=str.lower)
True
```

#### Enhanced Functional APIs

Documentation: https://zhiqingxiao.github.io/calcpy/builtin.html

- `calcpy.arggetter(*keys, *, default)` instantiates a callable object that fetches position arguments and/or keyword arguments, with default value for missing arguments.
- `calcpy.attrgetter(*attrs, *, default)` instantiates a callable object that fetches the given attribute(s) from its operand, with default value for missing attributes.
- `calcpy.itemgetter(*items, *, default)` instantiates a callable object that fetches the given item(s) from its operand, with muti-level keys and default value for missing items.
- `calcpy.constantcreator(value, /, *, copy=False)` instantiates a callable object that returns the same constant when it is called.


Examples:

```python
>>> from calcpy import arggetter
>>> getter = arggetter(0)  # get the first positional argument
>>> getter("value", "other_input", key="other_keyword_input")
'value'

>>> from calcpy import attrgetter
>>> getter = attrgetter("upper")
>>> getter("test")
'TEST'

>>> from calcpy import constantcreator
>>> creator = constantcreator("value")
>>> creator()
'value'
```

#### Decorators for Callable Outputs

Documentation: https://zhiqingxiao.github.io/calcpy/fill.html

- `calcpy.fillerr(fun, value=None)` instantiates a callable object that returns `value` if the function `fun` raises an exception.
- `calcpy.fillnone(fun, value=None)` instantiates a callable object that returns `value` if the function `fun` returns `None`.
- `calcpy.fillnan(fun, value=None)` instantiates a callable object that returns `value` if the function `fun` returns `nan`.

Examples:
```python
>>> from calcpy import fillerr, fillnone, fillnan
>>> @fillerr("Error")
... @fillnone("None")
... @fillnan("NaN")
... def fun(x):
...     if x > 0:
...         return nan
...     if x <= 0:
...         return 1 / x
>>> fun(0)
'Error'
>>> fun(-1)
-1.0
>>> fun(nan)
'None'
>>> fun(1)
'NaN'
``` 

#### Extensions of Built-in Functions

Similar to Python built-in functions `all()` and `any()`, we provide the functions with keyword parameter `empty` to specify the behavior when the sequence is empty.

- `calcpy.all_(iterable, *, empty=True)` checks whether all elements in a sequence are truthy. Return `empty` if the sequence is empty. (It is equivalent to `all(iterable)` when the default value of `empty` is used.)
- `calcpy.any_(iterable, *, empty=False)` checks whether any element in a sequence is truthy. Return `empty` if the sequence is empty. (It is equivalent to `any(iterable)` when the default value of `empty` is used.)
- `calcpy.never(iterable, *, empty=True)` checks whether all elements in a sequence are not truthy. Return `empty` if the sequence is empty.
- `calcpy.odd(iterable, *, empty=False)` checks whether an odd number of items in the iterable are truthy. Return `empty` if the sequence is empty.

Usage Example:
```python
>>> from calcpy import never, odd
>>> never([])
True
>>> never([False, False, False])
True
>>> odd([])
False
>>> odd([], empty=True)
True
```

We also extend the following functions in built-in modules `operator` so that it can accept an arbitrary number of arguments: `and_()`, `or_()`, `xor()`, `add()`, `mul()`, `lt()`, `le()`, `gt()`, `eq()`.

For examples, we have the following comparers. They support multiple numbers of arguments (including zero arguments and one argument).

- `calcpy.lt(*args, key=None)`
- `calcpy.le(*args, key=None)`
- `calcpy.ge(*args, key=None)`
- `calcpy.gt(*args, key=None)`
- `calcpy.eq(*args, key=None)`
- `calcpy.ne(*args, key=None)`

Usage Example:
```python
>>> from calcpy import lt
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
```

**Table**  Compare functions with multiple arguments and functions with a single iterable argument.

| Function with arbitrary number of positional arguments | Function of only one iterable positional argument | Support customized comparison |
|--------------------------------------------------------|---------------------------------------------------|-------------------------------|
| `calcpy.eq()`                                          | `calcpy.same()`                                   | Yes                           |
| `calcpy.ne()`                                          | `calcpy.distinct()`                               | Yes                           |
| `calcpy.and_()`                                        | `calcpy.all_()`                                   | Yes                           |
| `calcpy.or_()`                                         | `calcpy.any_()`                                   | Yes                           |
| `calcpy.xor()`                                         | `calcpy.odd()`                                    | Yes                           |
| `calcpy.add()`                                         | `calcpy.sum_()`                                   |                               |
| `calcpy.mul()`                                         | `calcpy.prod()`                                   |                               |
| `calcpy.matmul()`                                      | `calcpy.matprod()`                                |  


#### Relationship among Classes

Documentation: https://zhiqingxiao.github.io/calcpy/cls.html

The following APIs are provided to compare classes:

- `calcpy.ispropersubclass()`
- `calcpy.ispropersuperclass()`
- `calcpy.issubclass_()`
- `calcpy.issuperclass()`


#### Consistent APIs across Python built-in modules, numpy, and pandas

Documentation: https://zhiqingxiao.github.io/calcpy/nppd.html

We provide the following APIs that can accept arguments that are `numbers.Number`, `np.ndarray`, `pd.Series`, and/or `pd.DataFrame`.

- `calcpy.shape(arg)`
- `calcpy.ndim(arg)`
- `calcpy.size(arg)`
- `calcpy.full_like(template, fill_value, **kwargs)` supports create an object alike `template`. The parameter `template` can be a `numbers.Number`, `np.ndarray`, `pd.Series`, or `pd.DataFrame`.
- `calcpy.overall_equal(loper, roper)` support comparison two arguments as a whole. The two arguments can be `numbers.Number`, `np.ndarray`, `pd.Series`, or `pd.DataFrame`.

We provide the following decorator to extend existing functions:

- `calcpy.broadcast_first()` extends an existing function so that the first parameter can be `number.Number`, `np.ndarray`, `pd.Series`, or `pd.DataFrame`.


### Sequence APIs

**Repetend Analysis**

Documentation: https://zhiqingxiao.github.io/calcpy/seq.html#repetend-analysis

- `calcpy.min_repetend_len()` calculates the minimum length of repetends.

Usage Example:
```python
>>> from calcpy import min_repetend_len
>>> min_repetend_len([1, 2, 3, 1, 2, 3, 1, 2])
3
```

**Permutation**

Documentation: https://zhiqingxiao.github.io/calcpy/seq.html#permutation

- `calcpy.cycleperm()` permutates a list according to cycle notation.
- `calcpy.swap()` swaps two elements in a list.
- `calcpy.prioritize()` moves some positional arguments to the beginning.

Example:
```python
>>> from calcpy import cycleperm
>>> cycleperm(["a", "b", "c", "d", "e", "f", "g"], [1, 2, 4])
['a', 'c', 'e', 'd', 'b', 'f', 'g']
```


**Sequence Generator**

Documentation: http://zhiqingxiao.github.io/calcpy/seq.html#sequence-generator

- `calcpy.oeis.A276128()` generates elements of the sequence [OEIS A276128](https://oeis.org/A276128).


### File API

Documentation: http://zhiqingxiao.github.io/calcpy/file.html

- `calcpy.file.get_hash(filepath, method="sha256", batchsize=4096)` gets the hash value of a file.
