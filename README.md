This package enables a sort of local variable scoping in Python. It provides a
context manager that resets the definitions (and existence) of local variables
on exit to what they were at the start of the `with` statement.

    a = 3
    with scope():
        a, b = 5, 7
    # a is back to 3, b doesn't exist

There are also usage patterns that allow you to reset only certain variables,
or all except certain variables.

This is particularly useful for interactive work in e.g. iPython notebooks. For
real code, it's better to use a function.
