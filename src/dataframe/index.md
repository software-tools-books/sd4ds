---
title: "A Modest Dataframe"
syllabus:
- Storing two-dimensional data using one-dimensional data structures.
- How polymorphism enables performance tuning.
- Measuring performance to evaluate engineering tradeoffs.
---

Dataframes aren't magical:
whether your tool of choice is Python, R, SQL, or Excel,
you're almost certainly doing data science on tables
with named columns that have the same type of value in every row.
To explore how they work,
this repo contains two implementations of dataframes in Python:
one that stores values in columns,
the other that stores them in rows.

## Defining Operations {: #dataframe-ops}

We start by creating an *abstract base class*
that defines the methods our two dataframe classes will support.
This class is (unimaginatively) called `DF`;
it lives in `df.py` and requires *concrete* classes to implement:

-   `ncol`: report the number of columns.
-   `nrow`: report the number of rows.
-   `cols`: return the set of column names.
-   `eq`: check whether this dataframe is equal to another.
-   `get`: get a scalar value from a specified column and row.
-   `set`: set the scalar value in a specified column and row.
-   `select`: create a new dataframe containing some or all of the original's columns.
-   `filter`: create a new dataframe containing some or all of the original's rows.

## Storing Values in Columns {: #dataframe-cols}

We then derive a class `DfCol` that uses *column-wise* storage:

-   Each column is stored as a list of values,
    all of which are of the same type.
-   The dataframe is a dictionary of such lists,
    all of which have the same length.

Some methods are almost trivial to implement on top of this storage mechanism;
others are more difficult:

| Method   | Difficulty |
| -------- | ---------- |
| `ncol`   | easy       |
| `nrow`   | moderate   |
| `cols`   | easy       |
| `eq`     | moderate   |
| `get`    | easy       |
| `set`    | easy       |
| `select` | easy       |
| `filter` | hard       |

## Storing Values in Rows {: #dataframe-rows}

1.  Create a new class `DfRow` in a file called `df_row.py`
    that uses *row-wise* storage:
    -   Each row is stored as a dictionary
        that maps column names to values.
        All of these dictionaries have exactly the same keys,
        and the same type of value is associated with a particular key
        in each dictionary.
    -   The dataframe is a list of such dictionaries.

2.  Implement the eight methods required by the abstract base class.
    Which ones are easy and which ones are hard?

3.  Copy the file `test_dfcol.py` to create `test_dfrow.py`.
    Change the `import` statement and replace every reference to `DfCol`
    with a reference to `DfRow`,
    but do not make any other changes.
    Do all of the tests pass?
    If not, why not?
