# calcpy

Implementations of basic calculations in Python.


### Installation

```shell
pip install --upgrade calcpy
```


### Set-Alike APIs

Set-alike APIs operate objects with original order reserved and optional customized comparison function.

```Python
>>> from calcpy import unique
>>> unique([4, 3, 7, 3, 4])
[4, 3, 7]
```

**List of APIs:**

- `calcpy.unique(values, matcher=None)`  Remove duplicated entries.
- `calcpy.concat(*args, matcher=None)`   Concatenate.
- `calcpy.union(*args, matcher=None)`   Union.
- `calcpy.intersect(*args, matcher=None)`   Intersection.
- `calcpy.exclude(arg, *args, matcher=None)`   Remove follow-up arguments from the first.
- `calcpy.xor(*args, matcher=None)`    Exclusive-or of follow-up parameters from the first parameter.
- `calcpy.eq(*args, matcher=None)`    Check whether parameters are all equal.
- `calcpy.ne(*args, matcher=None)`    Check whether parameters are all distinct.


**Supported object types**

- `list`
- `tuple`
- `set`
- `np.ndarray`
- `pd.Series`
- `pd.DataFrame`
- others

**On keyword parameter `matcher`**: 
The keyword parameter `matcher` is for customized comparison function.
By default, it is `None`, which uses the default way to compare two objects, i.e. compare them as a whole.
We can write customized binary functions to compare two objects. For example, we can compare the equality of two `np.ndarray`s using `np.array_equal`, or use the following customized function `lower_matcher` to compare two `str`s according to their lowercases:

```python
>>> def lower_matcher(loper, roper):
...     return loper.lower() == roper.lower()
...
>>> from calcpy import eq
>>> eq("Hello", "hello", "HELLO", matcher=lower_matcher)
True
```

`calcpy` also provide a class `calcpy.matcher.PandasFrameMatcher` for comparing `pd.Series`s and `pd.DataFrame`s.

- `calcpy.matcher.PandasFrameMatcher()`   Compare whether pandas objects as a whole. The same as `loper.equals(roper)`.

- `calcpy.matcher.PandasFrameMatcher("index")`   Compare index values of pandas objects.

- `calcpy.matcher.PandasFrameMatcher("values")`    Compare values of pandas objects, ignoring the index values.

- `calcpy.matcher.PandasFrameMatcher("series")`     Compare `pd.DataFrame` in a `pd.Series` way. By default, it is `left_series.equals(right_series)`.

For `pd.DataFrame`, it also provides a keyword parameter `axis`. It compares each row when it is set to 0 (the default value) or `'index'`, and compares each column if `axis` is set to 1 or `'column'`.

### Sequence APIs

**Repetend Analysis**

- `calcpy.sequence.min_repetend_len()`: Get the mimimum length of repetends.

Usage Example:
```python
>>> from calcpy.sequence import min_repetend_len
>>> min_repetend_len([1, 2, 3, 1, 2, 3, 1, 2])
3
```

**Sequence Generator**

- `calcpy.sequence.A276128()`: Generator for the sequence [OEIS A276128](https://oeis.org/A276128).

Usage Example:
```python
>>> from calcpy.sequence import A276128
>>> print(list(A276128(14)))
[0, 0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 21, 24]
```
