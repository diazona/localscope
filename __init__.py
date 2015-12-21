import inspect

class ScopeContextManager(object):
    '''Creates a local scope for variable definitions. This is particularly
    useful for interactive work in e.g. iPython notebooks, and serviceable but
    a little clunky for working in a terminal. For real (non-interactive)
    code, just use a function.

    The best way to explain what this does is a few examples. In all
    the following snippets, `scope = ScopeContextManager` for brevity.
    First, the simplest way to use a scope is with no arguments:

        with scope():
            # temporary assignments

    In this usage, any assignments made to local variables inside the
    scope (i.e. inside the `with` statement) will be undone afterwards.
    So in the following example, once the scope ends, `a` and `b` are
    restored to their original values, and `c` is restored to not existing.

        >>> a, b = 7, 9
        >>> with scope():
        ...     a, b = 3, 5
        ...     c = a + b
        ...     print(c)
        8
        >>> print(a + b)
        16
        >>> print(c)
        Traceback (most recent call last):
            ...
        NameError: name 'c' is not defined

    You can also provide a list of variable names to preserve. If you do this,
    everything is reset at the end of the scope _except_ for the chosen names.

        >>> a, b = 7, 9
        >>> with scope(['c']):
        ...     a, b = 3, 5
        ...     c = a + b
        ...     print(c)
        8
        >>> print(a + b)
        16
        >>> print(c)
        8

    The simple mode with no arguments is equivalent to passing an empty list.

    You can also provide keyword arguments along with the list of names.
    The keyword arguments are used to set initial values for the
    corresponding variables. For instance, the last example could also be
    done like this:

        >>> a, b = 7, 9
        >>> with scope(['c'], a=3, b=5):
        ...     c = a + b
        ...     print(c)
        8
        >>> print(a + b)
        16
        >>> print(c)
        8

    The keyword arguments can also be variables in the list, in which
    case their values won't be reset afterwards.

        >>> a, b = 7, 9
        >>> with scope(['c', 'b'], a=3, b=5):
        ...     c = a + b
        ...     print(c)
        8
        >>> print(a + b)
        12
        >>> print(c)
        8

    There's another usage mode where you pass _only_ keyword arguments,
    without also giving a list. In this case, only the variables provided as
    keyword arguments will be reset at the end of the scope, and everything
    else will be untouched. This is similar to Mathematica's `With` statement,
    except that it doesn't perform a literal substitution on the code as
    Mathematica does). For example:

        >>> a, b = 7, 9
        >>> with scope(a=3):
        ...     b = 5
        ...     c = a + b
        ...     print(c)
        8
        >>> print(a + b)
        12
        >>> print(c)
        8

    Note that `b` is not reset to 9 at the end of the scope. Contrast that
    with the following example:

        >>> a, b = 7, 9
        >>> with scope(a=3, b=5):
        ...     c = a + b
        ...     print(c)
        8
        >>> print(a + b)
        16
        >>> print(c)
        8

    in which `b` _is_ reset, because it was given as a keyword argument.

    It's important to keep in mind that the list+keyword mode resets all
    variables not explicitly named in the list, whereas the keyword-only
    mode resets _only_ the variables named as keywords. So using
    `scope(a=3, b=5)` has a totally different effect from
    `scope([], a=3, b=5)`. A variable `c` would be reset in the latter case,
    not the former.
    '''
    def __init__(self, *args, **kwargs):
        self.initial_values = kwargs
        if len(args) == 0:
            if len(kwargs) == 0:
                self.vars_to_preserve = []
            else:
                self.vars_to_preserve = None
        elif len(args) == 1 and isinstance(args[0], list):
            self.vars_to_preserve = args[0]
        else:
            raise ValueError('Scope context manager takes one (optional) positional argument, a list of variables to preserve')
    def __enter__(self):
        l = inspect.stack()[1][0].f_locals
        self.old_locals = l.copy()
        l.update(self.initial_values)
    def __exit__(self, exc_type, exc_msg, exc_tb):
        l = inspect.stack()[1][0].f_locals
        if isinstance(self.vars_to_preserve, list):
            # clear out everything except the vars named in the list passed to the constructor
            preserved = dict((name, l[name]) for name in self.vars_to_preserve if name in l)
            l.clear()
            l.update(self.old_locals)
            l.update(preserved)
        else:
            # clear and restore only the variables given initial values
            for name in self.initial_values:
                if name in self.old_locals:
                    l[name] = self.old_locals[name]
                else:
                    del l[name]

scope = ScopeContextManager

if __name__ == '__main__':
    import doctest
    doctest.testmod()
