---
title: "A Minimal Functional Programming Toolkit"
---

-   The single biggest idea in programming is that *code is just another kind of data*
-   Easy to see that programs are just text files
-   But harder to see that instructions in memory are data too
    -   A string is a bunch of numbers in consecutive bytes that represent characters
    -   A pixel is a bunch of numbers that represent color values
    -   A function is a bunch of numbers that represent instructions
-   We'll play with this data structure in [% x interpreter %] and [% x compiler %]
-   But since many design techniques rely on this fact, we'll explore it here

## Functions as Data {: #functional-data}

-   Here's what happens when we create a variable whose value is an integer FIGURE
    -   Python turns the characters into a number
    -   Creates a variable that refers to that number
-   Here's what happens when we define a function FIGURE
    -   Python turns the characters into instructions
    -   Creates a variable that refers to those instructions
-   Notice the [% g boxing "boxing" %]
    -   Every object in Python keeps track of what kind of thing it is
    -   So that the interpreter knows what it can do to/with it
-   Here's what happens when we assign the value of an integer variable to another variable FIGURE
    -   Aliasing
-   Same thing happens with functions FIGURE
    -   FIXME: code
    -   Calling the function with either name has the same effect *because it's the same function*
-   We can do more with this than give functions new names
-   When we pass something as an argument to a function, we are creating an alias FIGURE
-   So we can pass functions as arguments to other functions
    -   Call this function twice
    -   Call this function once for each element of a list and return a list of results
-   This technique is a way to avoid duplication in code
    -   Compare these two functions
    -   Only thing that differs is one line in the middle
    -   Any time we see duplicated code, we should think about [% g refactoring "refactoring" %] it
-   The "call for each list element" function above is `map`
    -   Built into the language
    -   Available as `[f(x) for x in data]`
-   Also have `filter`, which is equivalent to this code FIXME

-   Sidebar: these are methods of the list class in JavaScript to enable a [% g fluent_interface "fluent interface" %]

## Lookup Tables {: #functional-lookup}

-   Introduce `globals()` and `locals()`
-   These are copies of the actual tables

```{: .python}
def f(x):
    print(f"before {x}")
    locals()["x"] = "changed"
    print(f"after {x}")

f("original")
```

-   Build our own lookup tables
-   E.g., select which function to run based on a command-line (string) argument

## Metadata {: #functional-metadata}

-   Functions are objects and objects have attributes

```{: .python}
>>> def f(x=0):
        "Documentation"
        pass

>>> f.__doc__
'Documentation'

>>> f.__defaults__
(0,)

>>> f.__module__
'__main__'

>>> f.__name__
'f'
```

-   Use this to get all the docstrings out of a module for display
-   Note: a class is just an object too
    -   So we can pass classes to functions or other classes
    -   Will explore this later

## Modules {: #functional-modules}

-   A module is just another (kind of) dictionary

```{: .python title="a.py"}
"""Docstring for module"""

def f(x):
    print(f"before {x}")
    locals()["x"] = 9
    print(f"after {x}")

if __name__ == '__main__':
    f(3)
```

```{: .python title="b.py"}
import a

print(dir(a))
print(a.__doc__)
```

-   We can load modules dynamically

```{: .python title="loader.py"}
import sys
from importlib import import_module

name = sys.argv[1]
loaded = import_module(name)
print(loaded)
loaded.f(3)
```

-   Works for files in sub-directories FIXME: subdir
-   But what about arbitrary directories like `/tmp`
-   Solution: temporarily add that directory to `sys.path`

```{: .python title="loader_path.py"}
import sys
from importlib import import_module

extra = sys.argv[1]
name = sys.argv[2]

sys.path.insert(0, extra)
loaded = import_module(name)
sys.path = sys.path[1:]
print(loaded)
```

## Exercises {: #functional-exercises}

### Reduce and scan {: .exercise}

-   Implement `reduce`.
-   Implement `scan`.
-   What should they do with empty data?

### Function attributes {: .exercise}

-   Functions also have `__kwdefaults__` (short for "keyword defaults"): why?
-   What happens to `__name__` if we assign a function to another variable with a different name?

### Missing documentation {: .exercise}

-   Write a program that loads a single Python file
    and produces a list of all the functions that *don't* have docstrings.

### Entry points {: .exercise}

-   Write a function that calls `entrypoint()` from every file named on the command line.
