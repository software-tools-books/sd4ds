---
title: "A Minimal Interpreter"
---

Programming languages aren't magical:
one piece of software translates text into instructions,
while another does what those instructions tell it to.
To explore how this works,
this chapter implements a small but completely functional language.

## Expressions {: #interpreter-expressions}

FIXME

## Statements {: #interpreter-statements}

`tll.py` reads a JSON file from standard input and executes the program it represents.
Each command is stored as a list
that starts with the name of an instruction
and may contain Booleans, numbers, strings, or other lists (representing other instructions).
For example,
this program that starts with the number 1 and doubles it four times:

```{: title="doubling.tll"}
[
    "seq",
    ["comment", "Double a number repeatedly"],
    ["set", "a", 1],
    ["print", "initial", ["get", "a"]],
    [
        "repeat",
        4,
        [
            "seq",
            ["set", "a", ["add", ["get", "a"], ["get", "a"]]],
	    ["if",
		["leq", ["get", "a"], 10],
		["print", "small", ["get", "a"]],
		["print", "large", ["get", "a"]]
	    ]
        ]
    ]
]
```

-   *Why JSON?*
    So we can parse the program with a single call to `json.load`.

-   *Why lists?*
    Because that's all a program is: a list of instructions,
    some of which are other lists of instructions.

-   *Why put the name of the instruction first?*
    To make it easy to find.
    Expressions like `2 + 3 * 5` take several dozen lines of code to parse
    because elements appear in mixed order
    and because we can't be sure what to do with one thing (like `+`)
    until we've seen a later thing (like `*`).

So how does TLL execute instructions?
First,
it defines one function for each instruction.
All of these functions take exactly the same parameters:
an *environment* (which is a dictionary containing all the program's variables)
and the instructions' arguments.
When given a list representing an instruction,
the function `do` uses the list's first element to figure out what other function to call
and calls it;
when given anything else, like a number or string,
`do` just returns that value immediately.

And that's pretty much it.
A function like `do_add` calls `do` to evaluate its arguments and then returns their sum;
a function like `do_seq` calls `do` once for each of its arguments in order
and returns the value of the last one;
`do_get` and `do_set` look up a variable's value and store new values respectively,
and `do_if` uses the result of evaluating its first argument
to decide whether to evaluate its second or third.
It's really that simple.

## Reflection {: #interpreter-reflection}

FIXME: Explain how the table `OPERATIONS` is constructed.

## Functions {: #interpreter-functions}

TLL can do a lot:
in fact,
since it has variables, loops, and conditionals,
it can do everything that *any* programming language can do.
However,
writing TLL programs will be painful
because there's no way for users to define new operations within the language itself.
Doing this in `tllfunc.py` makes TLL less than 60 lines longer:

1.  Instead of using a single dictionary to store an environment
    we use a list of dictionaries.
    The first dictionary is the global environment;
    the others store variables belonging to active function calls.

2.  When we get or set a variable,
    we check the most recent environment first
    (i.e., the one that's last in the list);
    if the variable isn't there we look in the global environment.
    We *don't* look at the environments in between.

3.  A function definition looks like:

        ["def", "same", ["num"], ["get", "num"]]

    It has a name, a (possibly empty) list of parameter names,
    and a single instruction as a body
    (which will usually be a `"seq"` instruction).

4.  Functions are stored in the environment like any other value.
    The value stored for the function defined above would be:

        ["func", ["num"], ["get", "num"]]

    We don't need to store the name: that's recorded by the environment,
    just like it is for any other variable.

5.  A function call looks like:

        ["call", "same", 3]

    The values passed to the functions are normally expressions rather than constants,
    and are *not* put in a sub-list.
    The implementation:
    1.  Evaluates all of these expressions.
    2.  Looks up the function.
    3.  Creates a new environment whose keys are the parameters' names
        and whose values are the expressions' values.
    4.  Calls `do` to run the function's action and captures the result.
    5.  Discards environment created two steps previously.
    6.  Returns the function's result.

## Exercises {: #interpreter-exercises}

### Arrays {: .exercise}

Implement fixed-size one-dimensional arrays:
`["array", "new", 10]` creates an array of 10 elements,
while other instructions get and set particular array elements by index.

### While Loops {: .exercise}

Add a `while` loop to TLL.

### Loop Variables {: .exercise}

The `"repeat"` instruction runs some other instruction(s) several times,
but there is no way to access the loop counter inside those instructions.
Modify `"repeat"` so that programs can do this.
(Hint: allow people to create a new variable to hold the loop counter's current value.)

### Error handling {: .exercise}

Several of the instruction functions started with `assert` statements,
which means that users get a stack trace of TLL itself
when there's a bug in their program.

1.  Define a new exception class called `TLLException`.

2.  Write a utility function called `check`
    that raises a `TLLException` with a useful error message
    when there's a problem.

3.  Add a `catch` statement to handle these errors.

### Documentation {: .exercise}

The docstring in each action function explain what it does.
Rewrite those for `do_repeat` and `do_seq` to be clearer and more consistent.

### Tracing {: .exercise}

Add a `--debug` command-line flag to `tllfunc.py`.
When enabled, it makes TLL print a messages showing each function call and its result.

### Returning Early {: .exercise}

Add a `"return"` instruction to TLL that ends a function call immediately
and returns a single value.
(Hint: try throwing an exception.)

### Variable Arguments {: .exercise}

Add variable-length parameter lists to TLL
so that a user-defined function can be called with any number of arguments.
(This exercise depends on having implemented arrays earlier.)

### Closures {: .exercise}

`tllfunc.py` allows users to define functions inside functions.
What variables can the inner function access when you do this?
What variables *should* it be able to access?
What would you have to do to enable this?
