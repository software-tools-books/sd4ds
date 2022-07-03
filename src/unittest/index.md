---
title: "A Modest Unit Testing Framework"
syllabus:
- How and why to create fixtures for tests.
- The three kinds of outcomes a test can have.
- Using introspection to find tests automatically.
---

We have written many small programs in the previous chapters,
but haven't really tested any of them.
That's OK for exploratory programming,
but if our software is going to be used instead of just read,
we should try to make sure it works.

A tool for writing and running [% g unit_test "unit tests" %] is a good first step.
Such a tool should:

-   find files containing tests;
-   find the tests in those files;
-   run the tests;
-   capture their results; and
-   report each test's result and a summary of those results.

Our design is inspired by [Pytest][pytest],
which was in turn inspired by many tools built for other languages
from the 1980s onward [% b Meszaros2007 %].

## Structuring Tests {: #unittest-structure}

As in other unit testing frameworks,
each test will be a function of zero arguments
so that the framework can run them all in the same way.
Each test will create a [% g fixture "fixture" %] to be tested
and use [% g assertion "assertions" %]
to compare the [% g actual_result "actual result" %]
against the [% g expected_result "expected result" %].
The outcome can be exactly one of:

-   [% g pass_test "Pass" %]:
    the [% g test_subject "test subject" %] works as expected.

-   [% g fail_test "Fail" %]:
    something is wrong with the test subject.

-   [% g error_test "Error" %]:
    something wrong in the test itself,
    which means we don't know whether the test subject is working properly or not.

To make this work,
we need some way to distinguish failing tests from broken ones.
Our solution relies on the fact that exceptions are objects
and that a program can use [% g introspection "introspection" %]
to determine the class of an object.
If a test [% g throw_exception "throws an exception" %] whose class is `assert.AssertionError`,
then we will assume the exception came from
one of the assertions we put in the test as a check.
Any other kind of assertion indicates that the test itself contains an error.

To start,
let's record tests and what they mean.
We don't run tests immediately
because we want to wrap each one in our own [% g exception_handler "exception handler" %].
Instead,
the function `hope_that` saves a descriptive message and a function that implements a test
in an array:

[% excerpt f="dry_run.py" keep="save" %]

> ### Independence
>
> Because we're appending tests to an array,
> they will be run in the order in which they are registered,
> but we shouldn't rely on that.
> Every unit test should work independently of every other
> so that an error or failure in an early test
> doesn't affect the result of a later one.

The function `main` runs all registered tests:

[% excerpt f="dry_run.py" keep="main" %]

If a test completes without an exception, it passes.
If any of the `assert` calls inside the test raises an `AssertionError`,
the test fails,
and if it raises any other exception,
it's an error.
After all tests are run,
`main` reports the number of results of each kind.
{: .continue}

Let's try it out:

[% excerpt f="dry_run.py" keep="use" %]
[% excerpt f="dry_run.out" %]

## Discovery {: #unittest-discovery}

This simple approach does what it's supposed to, but:

1.  It doesn't tell us which tests have passed or failed.

1.  The description of the test is separate from the test code.
    Some people argue that tests shouldn't need descriptions---that
    we should instead give them long names that describe what they're doing---but
    we should support string-style explanations for those who want them.

1.  It doesn't discover tests on its own:
    we have to remember to register the test using `hope_that`,
    which means that sooner or later (probably sooner)
    some of our tests won't be run.

1.  We don't have a way to test things that are supposed to raise `AssertionError`.
    Putting assertions into code to check that it is behaving correctly
    is called [% g defensive_programming "defensive programming" %];
    it's a good practice,
    but we should make sure those assertions are failing when they're supposed to,
    just as we should test our smoke detectors every once in a while.

We can solve several of these problems at once by looking up test functions dynamically.
Python stores the variables and functions we define in a dictionary.
We can get that dictionary by calling the function `globals`:

[% excerpt pat="show_globals.*" fill="py out" %]

We can loop over the keys of this dictionary and find things with particular names:

[% excerpt pat="show_tests.*" fill="py out" %]

which means we can find all the tests in a module,
call them,
and keep track of their results:
{: .continue}

[% excerpt pat="discovery.*" fill="py out" %]

This approach is less typing and less fragile than our first,
but we can improve it by showing the test function's [% g docstring "docstring" %]
if it has one.
Again,
functions are just objects,
which means they can have attributes.
If we give a function a docstring:

```
def example():
   "This is documentation."""
   pass
```

then `example.__doc__` contains the string `"This is documentation."`

We can do more than just print these strings when reporting problems:
we can embed instructions for the test framework in them.
For example,
we could decide that the string `"test:skip"` means "skip this test",
while `"test:fail"` means "we expect this test to fail".
Let's rewrite our tests to show this off:

[% excerpt f="docstring.py" keep="tests" %]

and then modify `run_tests` to look for these strings and act accordingly:
{: .continue}

[% excerpt f="docstring.py" keep="run" %]

The output is now:

[% excerpt f="docstring.out" %]

## Exercises {: #unittest-exercises}

### Literal strings {: .exercise}

If we have defined a variable with the test-skipping marker,
why can't we use that variable as the function's docstring like this:

```python
TEST_SKIP = "test:skip"


def test_sign_negative():
    TEST_SKIP
    assert sign(-3) == -1
```
