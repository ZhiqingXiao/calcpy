Comparers
=========

Functions to compare objects. The comparers support an arbitrary number of operands.

For `eq()`, `ne()`, `same()`, and `distinct()`, it also supports a keyword parameter `matcher`. For the usage of `matcher`, see the `matcher` section.

.. autofunction:: calcpy.eq
.. autofunction:: calcpy.ne
.. autofunction:: calcpy.lt
.. autofunction:: calcpy.le
.. autofunction:: calcpy.ge
.. autofunction:: calcpy.gt

.. autofunction:: calcpy.same
.. autofunction:: calcpy.distinct
.. autofunction:: calcpy.unique

-------
Matcher
-------

The `matcher` parameter is used to customize the comparison function.

We provide some binary functions to check the equality of two objects.

.. autofunction:: calcpy.overall_equal


The following helper functions are used to construct matchers:

.. autofunction:: calcpy.matcher.from_attrgetter
.. autofunction:: calcpy.matcher.from_callable
.. autofunction:: calcpy.matcher.from_dict
.. autofunction:: calcpy.matcher.from_itemgetter
.. autofunction:: calcpy.matcher.from_methodcaller

We also provide a class `calcpy.matcher.PandasFrameMatcher` for comparing `pd.DataFrame`s.

.. autoclass:: calcpy.matcher.PandasFrameMatcher

`calcpy` also provides a class `calcpy.matcher.PandasFrameMatcher` for comparing `pd.Series`s and `pd.DataFrame`s.

- `calcpy.matcher.PandasFrameMatcher()`   Compare whether pandas objects as a whole. It has the same effect as `calcpy.overall_equal()`.

- `calcpy.matcher.PandasFrameMatcher("index")`   Compare index values of pandas objects.

- `calcpy.matcher.PandasFrameMatcher("values")`   Compare values of pandas objects, ignoring the index values.

- `calcpy.matcher.PandasFrameMatcher("series")`   Compare `pd.DataFrame` in a `pd.Series` way. By default, it is `left_series.equals(right_series)`.

For `pd.DataFrame`, it also provides a keyword parameter `axis`. It compares each row when it is set to 0 (the default value) or `'index'`, and compares each column if `axis` is set to 1 or `'column'`.
