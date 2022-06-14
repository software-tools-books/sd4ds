---
title: "Introduction"
---

[% root README.md %]

## Audience {: #introduction-audience}

Every lesson should be written with specific learners in mind [% b Wilson2019 %]..
These two personas describe ours:

-   **Jess** is doing a PhD in ecology.
    Their one-and-only undergraduate programming course taught them
    how to write hundred-line Python programs with lists, loops, and functions;
    they now need to simulate changes in the ranges of several rodent species as a result of climate change
    and validate the predictions against dozens of datasets collected by previous students in their supervisor's lab,
    all of which need to be cleaned up and put in a consistent format.

-   After a BSc in astronomy,
    **Rupinder** became a data analyst at a health services startup,
    where he inherited a bewildering mix of spreadsheets,
    slide decks,
    shell scripts,
    [R Markdown][r_markdown] files,
    [Jupyter notebooks][jupyter],
    and out-of-date README files.
    He is comfortable creating classes in Python,
    and has even built a small package for his own use;
    he feels the company's code could and should be cleaner,
    but he doesn't know exactly what that means or how to get there.

Like Jess and Rupinder, readers should be able to:

-   Write Python programs using dictionaries, functions, and classes.

-   Install Python packages on their computer
    and run programs with it from the command line.

-   Use [Git][git] to save and share files.
    (It's OK not to know [the more obscure commands][git-man-page-generator].)

[% x glossary %] defines the terms we introduce in these lessons,
which in turn define their scope:

## Layout {: #introduction-layout}

We display Python source code like this:

```{: .python}
for s in species:
    print(s)
```

Note that we write functions as `functionName` rather than `functionName()`:
the latter is more common,
but people don't use `objectName{}` for objects or `arrayName[]` for arrays,
and the empty parentheses makes it hard to tell
whether we're talking about "the function itself" or "a call to the function with no parameters".
{: .continue}

We Unix shell commands like this:

```{: .sh}
for filename in *.dat
do
    cut -d , -f 10 $filename
done
```

and display data files and programs' output like this:
{: .continue}

```{: .txt}
Package,Releases
0,1
0-0,0
0-0-1,1
00print-lol,2
00smalinux,0
01changer,0
```

We occasionally wrap lines in source code in unnatural ways to make listings fit the printed page,
and sometimes use `...` to show where lines have been omitted.
Where we need to break lines of output for the same reason,
we end incomplete lines with a single backslash `\`.
The full listings are all available in [our Git repository][sd4ds_repo]
and [on our website][sd4ds_site].
