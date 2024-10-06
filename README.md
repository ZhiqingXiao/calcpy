# calcpy: The Package for Calculative Python


### Installation

```shell
pip install --upgrade calcpy
```

### Features

- Function compositions: Combine multiple functions into one.

- Set-like APIs including `union()`, `intersect()`, `exclude()`, that can be applied to `list`, `tuple`, `set`, `str`, `np.ndarray`, `pd.Series`, `pd.DataFrame`, and others. Also support customiized function for comparisons.

- Uniform APIs over Python built-in numbers, `np.ndarray`, `pd.Series` and `pd.DataFrame`.

- Enhanced Python's built-in calculation functions: `eq()`, `ne()`, `lt()`,`le()`, `gt()`, `ge()`, `and_()`, `or_()`, `xor()`, `add()`, `mul()` support arbitrary number of parameters. `eq()` and `ne()` support customized comparators. `attrgetter()`, `itemgetter()`, `all_()`, and `any_()` support default values.

- Return value decorations: If the function raises an error or returns invalid values such as `None` and `nan`, fill the values with designated values.


#### Function Composition

- `calcpy.fun.combine(how, *callables)` combines multiple callables into one callable in a way that is specified by `how`.

Examples:
```python
>>> from operator import itemgetter
>>> from calcpy.fun import combine
>>> combine(max, itemgetter(1), itemgetter(2))([3, 4, 5])
5
>>> combine(min, itemgetter(1), itemgetter(2))([3, 4, 5])
4
```

We also support the following shorthand functions for function compositions: `calcpy.fun.abs_()`, `calcpy.fun.add()`, `calcpy.fun.all_()`, `calcpy.fun.and_()`, `calcpy.fun.any_()`, `calcpy.fun.concat()`, `calcpy.fun.contains()`, `calcpy.fun.countOf()`, `calcpy.fun.eq()`, `calcpy.fun.floordiv()`, `calcpy.fun.ge()`, `calcpy.fun.getitem()`, `calcpy.fun.gt()`, `calcpy.fun.index()`, `calcpy.fun.indexOf()`, `calcpy.fun.inv()`, `calcpy.fun.is_()`, `calcpy.fun.is_not()`, `calcpy.fun.le()`, `calcpy.fun.lshift()`, `calcpy.fun.lt()`, `calcpy.fun.matmul()`, `calcpy.fun.mod()`, `calcpy.fun.mul()`, `calcpy.fun.ne()`, `calcpy.fun.neg()`, `calcpy.fun.never()`, `calcpy.fun.not_()`, `calcpy.fun.odd()`, `calcpy.fun.or_()`, `calcpy.fun.pos()`, `calcpy.fun.pow_()`, `calcpy.fun.rshift()`, `calcpy.fun.setitem()`, `calcpy.fun.sub()`, `calcpy.fun.truediv()`, `calcpy.fun.truth()`, `calcpy.fun.xor()`.

Examples:
```python
>>> from operator import itemgetter
>>> from calcpy.fun import add
>>> add(itemgetter(1), itemgetter(2))([3, 4, 5])
9
>>> from calcpy import identity
>>> add(identity, identity)(3, 4)
7
```


#### Permutate Arguments

- `calcpy.permcaller(fun, /, *, cycle=())` instantiates a callable object that swaps positional arguments according to a cyclc notation. By default, it does not permutate anything.

- `calcpy.swapcaller(fun, /, *, i=0, j=1)` instantiates a callable object that swaps `i`-th positional argument and `j`-th positional argument. By default, it permutates the first two arguments.

Examples:

```python
>>> from calcpy import swapcaller
>>> executor = swapcaller(range)
>>> executor(4, 2)
range(2, 4)
```

#### Reorganize Arguments

- `calcpy.merge_args(fun)`: Merge all positional arguments of a function to a single tuple argument.

- `calcpy.demerge_args(fun)`: Replace a single tuple/list argument to many positional arguments. 


Examples:

```python
>>> from calcpy import merge_args
>>> merge_args(print)([0, 1.0, "Hello"])
0 1.0 Hello
```

#### Set-Alike APIs

Set-alike APIs operate objects with original order reserved and optional customized comparison function.

- `calcpy.unique(values, matcher=None)`  Remove duplicated entries.
- `calcpy.concat(*args, matcher=None)`   Concatenate.
- `calcpy.union(*args, matcher=None)`   Union.
- `calcpy.intersect(*args, matcher=None)`   Intersection.
- `calcpy.exclude(arg, *args, matcher=None)`   Remove follow-up arguments from the first.
- `calcpy.symmetricdiff(*args, matcher=None)`    Exclusive-or of follow-up parameters from the first parameter.
- `calcpy.eq(*args, matcher=None)`    Check whether positional arguments are all equal.
- `calcpy.ne(*args, matcher=None)`    Check whether positional arguments are all distinct.
- `calcpy.same(values, matcher=None)`  Check whether all elements in the first positional argument are all equal.
- `calcpy.distinct(values, matcher=None)`  Check whether all elements in the first positional argument are all distinct.

Examples:
```Python
>>> from calcpy import unique, union
>>> unique([4, 3, 7, 3, 4])
[4, 3, 7]
>>> union([4, 3], [7, 3], [4])
[4, 3, 7]
```

**Supported object types**: `list`, `tuple`, `set`, `str`, `np.ndarray`, `pd.Series`, `pd.DataFrame`, and more.

**`union()`, `intersect()`, and `exclude()` for `dict`**:
The function `intersect()` and `exclude()` support first argument of type `dict` and follow-up arguments as type `list`. In those cases, it means that limit the keys of the `dict` with a list or exclude lists out of the dict.

The function `union()` can merge multiple `dict`s into one `dict`. If two `dict`s `d1` and `d2` have the same key `k`, `union(d1, d2)` will use the value of `d1[k]` rather than `d2[k]`, which differs from `d1 | d2` who takes `d2[k]`.

**Customized comparison**: The keyword parameter `matcher` is used for customized comparison function.
By default, it is `None`, which uses the default way to compare two objects, i.e. compare them as a whole. It is the same as `calcpy.overall_equal()`. The function `calcpy.overall_equal()` behaves like `np.array_equal()` or `np.ndarray`s, and like `loper.equals(roper)` for `pd.Series`s and `pd.DataFrame`s.

We can write customized binary functions to compare two objects. For example, we can use the following customized function `lower_matcher` to compare two `str`s according to their lowercases:

```python
>>> def lower_matcher(loper, roper):
...     return loper.lower() == roper.lower()
...
>>> from calcpy import eq
>>> eq("Hello", "hello", "HELLO", matcher=lower_matcher)
True
```

**Construct matchers**: We provide the following helper functions to construct the binary matcher function:

- `calcpy.matcher.from_attrgetter(attr, default)`
- `calcpy.matcher.from_callable(callable, *args, **kwargs)`
- `calcpy.matcher.from_dict(mapper)`
- `calcpy.matcher.from_itemgetter(item)`
- `calcpy.matcher.from_methodcaller(name, *args, **kwargs)`


Example:

```python
>>> from calcpy import eq
>>> from calcpy.matcher import from_methodcaller
>>> lower_matcher = from_methodcaller("lower")
>>> eq("Hello", "hello", "HELLO", matcher=lower_matcher)
True
```

**Matchers for Pandas Objects**: The class `calcpy.matcher.PandasFrameMatcher` for comparing `pd.Series`s and `pd.DataFrame`s.

- `calcpy.matcher.PandasFrameMatcher()`   Compare whether pandas objects as a whole. It has the same effect as `calcpy.overall_equal()`.

- `calcpy.matcher.PandasFrameMatcher("index")`   Compare index values of pandas objects.

- `calcpy.matcher.PandasFrameMatcher("values")`   Compare values of pandas objects, ignoring the index values.

- `calcpy.matcher.PandasFrameMatcher("series")`   Compare `pd.DataFrame` in a `pd.Series` way. By default, it is `left_series.equals(right_series)`.

For `pd.DataFrame`, it also provides a keyword parameter `axis`. It compares each row when it is set to 0 (the default value) or `'index'`, and compares each column if `axis` is set to 1 or `'column'`.


#### Enhanced Functional APIs

- `calcpy.identity(value, *args, **kwargs)` returns the first value `value`.

- `calcpy.attrgetter(attr, ..., /, *, default)` instantiates a callable object that fetches the given attribute(s) from its operand, with default value for missing attributes.

- `calcpy.itemgetter(item, ..., /, *, default)` instantiates a callable object that fetches the given item(s) from its operand, with muti-level keys and default value for missing items.

- `calcpy.constantcreator(value, /, *, copy=False)` instantiates a callable object that returns the same constant when it is called.


Examples:

```python
>>> from calcpy import identity
>>> identity("value", "other_input", key="other_keyword_input")
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

- `calcpy.fillerr(fun, value=None)` instantiates a callable object that return `value` if the function `fun` raises an exception.

- `calcpy.fillnone(fun, value=None)` instantiates a callable object that return `value` if the function `fun` return `None`.

- `calcpy.fillnan(fun, value=None)` instantiates a callable object that return `value` if the function `fun` return `nan`.

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

Similary to Python built-in functions `all()` and `any()`, we provide the functions with keyword parameter `empty` to specify the behavior when the sequence is empty.

- `calcpy.all_(iterable, *, empty=True)`: Check whether all elements in a sequence are truthy. Return `empty` if the sequence is empty. (It is equivalent to `all(iterable)` when the default value of `empty` is used.)

- `calcpy.any_(iterable, *, empty=False)`: Check whether any element in a sequence is truthy. Return `empty` if the sequence is empty. (It is equivalent to `any(iterable)` when the default value of `empty` is used.)

- `calcpy.never(iterable, *, empty=True)`: Check whether all elements in a sequence are not truthy. Return `empty` if the sequence is empty.

- `calcpy.odd(iterable, *, empty=False)`: Check whether an odd number of items in the iterable are truthy. Return `empty` if the sequence is empty.

Usage Example:
```python
>>> from calcpy import never, xor
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

- `calcpy.lt(*args)`
- `calcpy.le(*args)`
- `calcpy.ge(*args)`
- `calcpy.gt(*args)`

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

| Function with multiple positional arguments | Function of only one iterable positional argument |
|---------------------------------------------|---------------------------------------------------|
| `eq()`                                      | `same()`                                          |
| `ne()`                                      | `distinct()`                                      |
| `and_()`                                    | `all_()`                                          |
| `or_()`                                     | `any_()`                                          |
| `xor()`                                     | `odd()`                                           |
| `add()`                                     | `sum()`                                           |
| `mul()`                                     | `prod()`                                          |


### Consistent APIs across Python built-in modules, numpy, and pandas

We provide the following APIs that can accept numbers, `np.ndarray`, `pd.Series`, and `pd.DataFrame`.
- `calcpy.shape(arg)`
- `calcpy.ndim(arg)`
- `calcpy.size(arg)`
- `calcpy.full_like(template, fill_value, **kwargs)`
- `calcpy.overall_equal(loper, roper)`

### Sequence APIs

**Repetend Analysis**

- `calcpy.min_repetend_len()`: Get the mimimum length of repetends.

Usage Example:
```python
>>> from calcpy import min_repetend_len
>>> min_repetend_len([1, 2, 3, 1, 2, 3, 1, 2])
3
```

**Permutation**

- `calcpy.perm()`: Permutate a list according to cycle notation.
- `calcpy.swap()`: Swap two elements in a list.

Example:
```python
>>> from calcpy import perm
>>> perm(["a", "b", "c", "d", "e", "f", "g"], [1, 2, 4])
['a', 'c', 'e', 'd', 'b', 'f', 'g']
```


**Sequence Generator**

- `calcpy.A276128()`: Generator for the sequence [OEIS A276128](https://oeis.org/A276128).

Usage Example:
```python
>>> from calcpy import A276128
>>> print(list(A276128(14)))
[0, 0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 21, 24]
```

### File API

- `calcpy.file.get_hash(filepath, algorithm="sha256")`: Get the hash value of a file.

