#!/usr/bin/env python3

"""
** Allows to create only one instance of an object. **
------------------------------------------------------

for the objects
"""


class MetaSingleton(type):
    """
    ** For share memory inside the current session. **

    Notes
    -----
    The arguments needs to be hashable.

    Examples
    --------
    >>> from movia.core.optimisation.cache.singleton import MetaSingleton
    >>> class A:
    ...     pass
    ...
    >>> class B(metaclass=MetaSingleton):
    ...     pass
    ...
    >>> class C(metaclass=MetaSingleton):
    ...     def __init__(self, *args, **kwargs):
    ...         self.args = args
    ...         self.kwargs = kwargs
    ...
    >>> A() is A()
    False
    >>> B() is B()
    True
    >>> C(0) is C(0)
    True
    >>> C(0) is C(1)
    False
    >>>
    """

    instances = {}

    def __call__(cls, *args, **kwargs):
        signature = (cls, args, tuple((k, kwargs[k]) for k in sorted(kwargs)))
        if signature not in MetaSingleton.instances:
            instance = cls.__new__(cls)
            instance.__init__(*args, **kwargs)
            MetaSingleton.instances[signature] = instance
        return MetaSingleton.instances[signature]
