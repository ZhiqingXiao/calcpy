Set-like APIs
=============

Set-alike APIs operate objects with original order reserved and optional customized comparison function.

**Supported object types**

- `list`
- `tuple`
- `set`
- `np.ndarray`
- `pd.Series`
- `pd.DataFrame`
- others

**On keyword parameter `matcher`**: See `cmp` section for details.


**`union()`, `intersect()`, and `exclude()` for `dict`**:
The function `intersect()` and `exclude()` support first argument of type `dict` and follow-up arguments as type `list`. In those cases, it means that limit the keys of the `dict` with a list or exclude lists out of the dict.

.. autofunction:: calcpy.union
.. autofunction:: calcpy.intersect
.. autofunction:: calcpy.exclude
.. autofunction:: calcpy.symmetricdiff

