---
title: "A Modest Python Toolkit"
---

-   The single biggest idea in programming is that *code is just another kind of data*
-   Easy to see that programs are just text files
-   But harder to see that instructions in memory are data too
    -   A string is a bunch of numbers in consecutive bytes that represent characters
    -   A pixel is a bunch of numbers that represent color values
    -   A function is a bunch of numbers that represent instructions
-   We'll play with this data structure in [% x interpreter %] and [% x compiler %]
-   But since many design techniques rely on this fact, we'll explore it here

## Nested Data {: #scraper-nested}

The list `flat` contains three strings:

```
flat = ["red", "green", "blue", "lime"]
```

If we want to get the total length of those strings,
we just add up the lengths of the items in `flat`:

```
total = 0
for word in flat:
    total += len(word)
```

If we have a list of lists,
we can use a double loop:

```
double = [["red", "green"], ["blue", "lime"]]
total = 0
for sublist in double:
    for word in sublist:
        total += len(word)
```

But what if we have a mix of words and lists?
What do we do if we have a structure like this:

```
irregular = ["red", ["green", "blue"], ["lime"]]
```

We could test the type of the item in the outer loop,
and only run the inner loop when the item is a sublist:

```
total = 0
for thing in irregular:
    if isinstance(thing, str):
        total += len(thing)
    elif isinstance(thing, list):
        for item in thing:
            total += len(item)
    else:
        print("Whoops, I don't know what", thing, "is")
```

That code isn't easy to read.
It also breaks as soon as we have sub-sub-lists like this:

```
nested = ["red", ["green", ["blue", "lime"]]]
```

To handle this,
we need to take a step back and write a function.
Here's our first attempt:

```
def add_len(thing):
    # If we're given a string, return its length immediately.
    if isinstance(thing, str):
        return len(thing)

    # If it's not a string, it had better be a list.
    assert isinstance(thing, list)

    # It's a list, so do something with each of its items.
    pass # What do we do here?
```

The last line of the code block above is the hard part.
We know we have a list.
We know it contains string and lists.
We want the total length of all the strings it contains.
If we had a magic function that could give us that total,
we'd be done:

```
def add_len(thing):
    if isinstance(thing, str):
        return len(thing)

    assert isinstance(thing, list)

    total = 0
    for item in thing: # we can loop because we know 'thing' is a list
        total += magic_function(item) # this is the part we're missing
    return total
```

But we *have* the magic function we need:
it's called `add_len`.
Let's plug that in to get the final version of `add_len`:

```
def add_len(thing):
    if isinstance(thing, str):
        return len(thing)

    assert isinstance(thing, list)

    total = 0
    for item in thing:
        total += add_len(item)
    return total
```

Let's trace its execution.

1.  `add_len("red")`:
    since `thing` is the string `"red"`,
    the function immediately returns 3.

2.  `add_len(["red"])`:
    `thing` is a list with one item,
    so we initialize `total` to 0 and go around our loop once.
    Inside the loop, we add `add_len("red")` to `total`.
    We've already established that `add_len("red")` returns 3,
    so we set `total` to 0+3,
    finish the loop,
    and return 3.

3.  `add_len(["red", "green"])`:
    OK, `thing` is a list with two items,
    so our loop calls `add_len("red")` and `add_len("green")`
    in that order,
    setting `total` to 3 and then 8
    and returns that.

4.  `add_len(["red", ["green", "blue"]])`:
    we'll trace this one point by point.
    The initial call to `add_len` sees a list so it goes to the bottom code.
    -   It initializes `total` to 0.
    -   The first time around the loop we call `add_len("red")`.
        This returns 3, so `total` becomes 3.
    -   The second time around the loop we call `add_len(["green", "blue"])`.
        Since we've given `add_len` a list,
        we go into a loop inside *that* call to the function.
        -   We initialize `total` to 0.
            This is *not* the same variable as the `total` mentioned above:
            this `total` belongs to the new call to `add_total`,
            just like different people each have their own nose.
        -   The first time around the loop we call `add_len("green")`.
            It returns 5, so we set this function call's `total` to 5.
        -   The second time around we call `add_len("blue")`,
            so total becomes 9.
        -   There's nothing else in the list, so this function call returns 9.
    -   We're now back in the initial function call.
        Its total is 3 (the length of `"red"`)
        and the call to `add_len(["green", "blue"])` just returned 9,
        so we set `total` to 12.
    -   There's nothing else in this function call's list,
        so we return 12
        and we're done.

This explanation is probably very confusing,
so please head over to <https://pythontutor.com/visualize.html#mode=edit>,
copy the `add_len` function into the text box,
add a line to call the function,
and then click on `[Visualize Execution]`.
As you click `[Next]`,
it will show you what's happening step by step as your code runs.

<div align="center">
  <img src="add_len.png" alt="Visualization of add_len function" width="80%"/>
</div>

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

### Joining All Strings {: .exercise}

Write a function called `join_all` that joins all the strings
in a bunch of nested lists.
For example:

```
join_all([["red", ["green", "blue"]], "lime"])
```

should return `"redgreenbluelime"`.
{: .continue}

### Searching Nested Lists {: .exercise}

Write a function called `longest` that returns the longest string it finds
in a bunch of nested lists.
For example:

```
longest(["red", ["green", "blue"], ["lime"]])
```

should return `"green"`.
If several strings are of equal longest length,
return whichever you want.
{: .continue}

### JSON {: .exercise}

JSON (short for "JavaScript Object Notation")
consists of nested lists and dictionaries,
where the dictionaries can only have strings as keys.
For example,
this is a valid JSON data structure:

```
{"alpha": 1, "beta": {"gamma": [2, 3], "delta": [4, {"epsilon": 5}]}}
```

It may be easier to read if it's written like this:
{: .continue}

```
{
    "alpha": 1,
    "beta": {
        "gamma": [
            2,
            3
        ],
        "delta": [
            4,
            {
                "epsilon": 5
            }
        ]
    }
}
```

Modify `add_len` so that it returns the total length
of all the numbers that appear as values in a JSON data structure.
For example, the result for the data structure shown above is 15.
{: .continue}

## Searching JSON {: .exercise}

Write a function `json_find` that takes a list of keys and indices
and returns the part of a JSON structure at that location.
For example, the list `["beta", "delta", 1]` should return the
dictionary `{"epsilon":5}` in the previous exercise:

-   The key `"beta"` selects a sub-dictionary.
-   They key `"delta"` selects a list.
-   The index 1 selects the second element of that list.

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
