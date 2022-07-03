---
title: "A Modest Persistence Framework"
---

FIXME
-   Almost all data science is load-process-save
-   Load and save are complements of each other
-   The world doesn't need another data format
-   But a chance to introduce several basic design ideas
    -   Functions as objects
    -   Extensibility
    -   Testing and testability

## Saving Flat Structures {: #persist-flat}

-   Use `type value` for built-in types
-   Use `type number` followed by entries for structured types
-   Use `if`-`elif`-`else` to reconstruct
-   Replace that with lookup table
    -   Functions as objects

## Saving Nested Structures {: #persist-nested}

-   Could come up with notation for list of dictionaries of lists
-   Use recursion instead
-   Function that reads the next thing from the input can call itself

## Testing {: #persist-test}

-   Introduction to pytest
-   Use string IO instead of creating files on disk
    -   Design for test: caller provides something stream-like
    -   Convenience vs. fidelity

## Extensibility {: #persist-extensible}

-   Client can register new names and translation functions
    -   Always come in pairs
-   But it means the loader must register the same types as the saver
    -   JSON, YAML, etc. restrict types to avoid this complexity

## Versioning {: #persist-extensible}

-   Colors go from RGB to RGBA
-   Preface each archive with version numbers or similar

## Exercises {: #persist-exercises}
