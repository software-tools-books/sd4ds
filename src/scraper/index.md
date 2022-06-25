---
title: "A Modest Web Scraper"
---

This short lesson will show you how to build a fully functional web scraper.
We'll tackle the problem in three steps:
handling nested data,
handling HTML,
and finally getting HTML pages from the web.

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

## HTML and CSS {: #scraper-htmlcss}

HTML is the standard way to represent documents for presentation in web browsers,
and CSS is the standard way to describe how it should look.
Both are more complicated than they should have been,
but in order to create web applications,
we need to understand a little of both.

An HTML document contains elements and text
(and possibly other things that we will ignore for now).
Elements are shown using tags:
an opening tag `<tagname>` shows where the element begins,
and a corresponding closing tag `</tagname>` (with a leading slash) shows where it ends.
If there's nothing between the two, we can write `<tagname/>` (with a trailing slash).

A document's elements must form a tree,
i.e.,
they must be strictly nested.
This means that if Y starts inside X,
Y must end before X ends,
so `<X>…<Y>…</Y></X>` is legal,
but `<X>…<Y>…</X></Y>` is not.
Finally,
every document should have a single root element that encloses everything else,
although browsers aren't strict about enforcing this.
In fact,
most browsers are pretty relaxed about enforcing any kind of rules at all,
since most people don't obey them anyway.

The text in an HTML page is normal printable text.
However,
since `<` and `>` are used to show where tags start and end,
we must use escape sequences to represent them,
just as we use `\"` to represented a literal double-quote character
inside a double-quoted string in JavaScript.
In HTML,
escape sequences are written `&name;`,
i.e.,
an ampersand, the name of the character, and a semi-colon.
A few common escape sequences are shown below:

| Name         | Escape Sequence | Character |
| ------------ | --------------- | --------- |
| Less than    | `&lt;`          | <         |
| Greater than | `&gt;`          | >         |
| Ampersand    | `&amp;`         | &         |
| Copyright    | `&copy;`        | ©         |
| Plus/minus   | `&plusmn;`      | ±         |
| Micro        | `&micro;`       | µ         |

The first two are self-explanatory,
and `&amp;` is needed so that we can write a literal ampersand
(just as `\\` is needed in JavaScript strings so that we can write a literal backslash).
`&copy;`, `&plusmn;`, and `&micro;` are usually not needed any longer,
since most editors will allow us to put non-ASCII characters directly into documents these days,
but occasionally we will run into older or stricter systems.

An HTML page should have:

-   a single `html` element that encloses everything else,
-   a single `head` element that contains information about the page, and
-   a single `body` element that contains the content to be displayed.

It doesn't matter whether or how we indent the tags showing these elements and the content they contain,
but laying them out on separate lines
and indenting to show nesting
helps human readers.
Well-written pages also use comments, just like code:
these start with `<!--` and end with `-->`.
Unfortunately,
comments cannot be nested,
i.e.,
if you comment out a section of a page that already contains a comment,
the results are unpredictable.

Here's an empty HTML page with the structure described above:

```{: .html}
<html>
  <head>
    <!-- description of page goes here -->
  </head>
  <body>
    <!-- content of page goes here -->
  </body>
</html>
```

Nothing shows up if we open this in a browser,
so let's add a little content:
{: .continue}

```{: .html}
<html>
  <head>
    <title>This text is displayed in the browser bar</title>
  </head>
  <body>
    <h1>Displayed Content Starts Here</h1>
    <p>
      This course introduces core features of <em>JavaScript</em>
      and shows where and how to use them.
    </p>
    <!-- The word "JavaScript" is in italics (emphasis) in the preceding paragraph. -->
  </body>
</html>
```

-   The `title` element inside `head` gives the page a title.
    This is displayed in the browser bar when the page is open,
    but is *not* displayed as part of the page itself.

-   The `h1` element is a level-1 heading;
    we can use `h2`, `h3`, and so on to create sub-headings.

-   The `p` element is a paragraph.

-   Inside a heading or a paragraph,
    we can use `em` to *emphasize* text.
    We can also use `strong` to make text **stronger**.
    Tags like these are better than tags like `i` (for italics) or `b` (for bold)
    because they signal intention rather than forcing a particular layout.
    Someone who is visually impaired, or someone using a small-screen device,
    may want emphasis of various kinds displayed in different ways.

Elements can be customized by giving them attributes,
which are written as `name="value"` pairs inside the element's opening tag.
Forr example:

```{: .html}
<h1 align="center">A Centered Heading</h1>
```

centers the `h1` heading on the page, while:
{: .continue}

```{: .html}
<p class="disclaimer">This planet provided as-is.</p>
```

marks this paragraph as a disclaimer.
That doesn't mean anything special to HTML,
but as we'll see later,
we can define styles based on the `class` attributes of elements.
{: .continue}

An attribute's name may appear at most once in any element,
just like a key can only appear once in any JavaScript object,
so `<p align="left" align="right">…</p>` is illegal.
If we want to give an attribute multiple values---for example,
if we want an element to have several classes---we put all the values in one string.
Unfortunately,
as the example below shows,
HTML is inconsistent about whether values should be separated by spaces or semi-colons:

```{: .html}
<p class="disclaimer optional" style="color: blue; font-size: 200%;">
```

However they are separated,
values are supposed to be quoted,
but in practice we can often get away with `name=value`.
And for Boolean attributes whose values are just true or false,
we can even sometimes just get away with `name` on its own.

Headings and paragraphs are all very well,
but data scientists need more.
To create an unordered (bulleted) list,
we use a `ul` element,
and wrap each item inside the list in `li`.
To create an ordered (numbered) list,
we use `ol` instead of `ul`,
but still use `li` for the list items.

```{: .html}
<ul>
  <li>first</li>
  <li>second</li>
  <li>third</li>
</ul>
```

```{: .html}
<ol>
  <li>first</li>
  <li>second</li>
  <li>third</li>
</ol>
```

Lists can be nested by putting the inner list's `ul` or `ol`
inside one of the outer list's `li` elements.

Unsurprisingly,
we use the `table` element to create these.
Each row is a `tr` (for ``table row''),
and within rows,
column items are shown with `td` (for ``table data'')
or `th` (for ``table heading'').

```{: .html}
<table>
  <tr> <th>Alkali</th>   <th>Noble Gas</th> </tr>
  <tr> <td>Hydrogen</td> <td>Helium</td>    </tr>
  <tr> <td>Lithium</td>  <td>Neon</td>      </tr>
  <tr> <td>Sodium</td>   <td>Argon</td>     </tr>
</table>
```

Links to other pages are what make HTML hypertext.
Confusingly,
the element used to show a link is called `a`.
The text inside the element is displayed and (usually) highlighted for clicking.
Its `href` attribute specifies what the link is pointing at;
both local filenames and URLs are supported.
Oh,
and we can use `<br/>` to force a line break in text
(with a trailing slash inside the tag, since the `br` element doesn't contain any content):

```{: .html}
<a href="https://nodejs.org/">Node.js</a>
<br/>
<a href="https://facebook.github.io/react/">React</a>
<br/>
<a href="../index.html">home page (relative path)</a>
```

Images can be stored directly inside HTML pages by embedding SVG
or by encoding the image as text and including that text in the body of the page.
The first is hard to edit,
since most text editors don't allow you to draw,
while the second is both hard to edit and impossible to read.

It is far more common to store each image in a separate file
and refer to that file using an `img` element
(which also allows us to use the image in many places without copying it).
The `src` attribute of the `img` tag specifies where to find the file;
as with the `href` attribute of an `a` element,
this can be either a URL or a local path.
Every `img` should also include a `title` attribute (whose purpose is self-explanatory)
and an `alt` attribute with some descriptive text to aid accessibility and search engines.
(Again, we have wrapped and broken lines so that they will display nicely in the printed version.)

```{: .html}
<img src="./img/logo.png" title="Book Logo"
     alt="Displays the book logo using a local path" />
<img src="https://third-bit.com/sd4ds/img/logo.png"
     title="Book Logo"
     alt="Display the book logo using a URL" />
```

Two things to note here are:

1.  Since `img` elements don't contain any text,
    they are often written with the trailing-slash notation,
    or as `<img src="...">` without any slashes at all.

2.  If an image file is referred to using a path rather than a URL,
    that path can be either relative
    or absolute.
    If it's a relative path,
    it's interpreted starting from where the web page is located;
    if it's an absolute path,
    it's interpreted relative to wherever the web browser thinks
    the root directory of the filesystem is.

When HTML first appeared, people styled elements by setting their attributes:

```{: .html}
<html>
  <body>
    <h1 align="center">Heading is Centered</h1>
    <p>
      <b>Text</b> can be highlighted
      or <font color="coral">colorized</font>.
    </p>
  </body>
</html>
```

Many still do,
but a better way is to use Cascading Style Sheets (CSS).
These allow us to define a style once and use it many times,
which makes it much easier to maintain consistency.
Here's a page that uses CSS instead of direct styling:

```{: .html}
<html>
  <head>
    <link rel="stylesheet" href="simple-style.css" />
  </head>
  <body>
    <h1 class="title">Heading is Centered</h1>
    <p>
      <span class="keyword">Text</span> can be highlighted
      or <span class="highlight">colorized</span>.
    </p>
  </body>
</html>
```

The `head` contains a link to an external style sheet
stored in the same directory as the page itself;
we could use a URL here instead of a relative path,
but the `link` element *must* have the `rel="stylesheet"` attribute.
Inside the page,
we then set the `class` attribute of each element we want to style.

The file `simple-style.css` looks like this:

```{: .css}
h1.title {
  text-align: center;
}
span.keyword {
  font-weight: bold;
}
.highlight {
  color: coral;
}
```

Each entry has the form `tag.class` followed by a group of properties inside curly braces,
and each property is a key-value pair.
We can omit the class and just write (for example):
{: .continue}

```{: .css}
p {
  font-style: italic;
}
```

in which case the style applies to everything with that tag.
If we do this,
we can override general rules with specific ones:
the style for a disclaimer paragraph is defined by `p` with overrides defined by `p.disclaimer`.
We can also omit the tag and simply use `.class`,
in which case every element with that class has that style.
{: .continue}

Elements may have multiple values for class,
as in `<span class="keyword highlight">…</span>`.
(The `span` element simply marks a region of text,
but has no effect unless it's styled.)

One other thing CSS can do is match specific elements.
We can label particular elements uniquely within a page using the `id` attribute,
then refer to those elements using `#name` as a selector.
For example,
if we create a page that gives two spans unique IDs:

```{: .html}
<html>
  <head>
    <link rel="stylesheet" href="selector-style.css" />
  </head>
  <body>
    <p>
      First <span id="major">keyword</span>.
    </p>
    <p>
      Full <span id="minor">explanation</span>.
    </p>
  </body>
</html>
```

then we can style those spans like this:
{: .continue}

```{: .css}
span#major {
  text-decoration: underline red;
}
span#minor {
  text-decoration: overline blue;
}
```

<div class="callout" markdown="1">
### Internal Links

We can link to an element in a page using `#name`
inside the link's `href`:
for example,
`<a href="page.html#place">text</a>`
refers to the `#place` element in `page.html`.
This is particularly useful *within* pages:
`<a href="#place">jump</a>`
takes us straight to the `#place` element within this page.
Internal links like this are often used for cross-referencing and to create a table of contents.
</div>

## Exercises {: #scraper-exercises}

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

### Cutting Corners {: .exercise}

What does your browser display if you forget to close a paragraph or list item tag
like this:

```{: .html}
<p>This paragraph starts but doesn't officially end.

<p>Another paragraph starts here but also doesn't end.

<ul>
  <li>First item in the list isn't closed.
  <li>Neither is the second.
</ul>
```

### Mix and Match {: .exercise}

1.  Create a page that contains a 2×2 table,
    each cell of which has a three-item bullet-point list.
    How can you reduce the indentation of the list items within their cells using CSS?

1.  Open your page in a different browser (e.g., Firefox or Edge).
    Do they display your indented lists consistently?

### Color {: .exercise}

HTML and CSS define names for a small number of colors.
All other colors must be specified using RGB values.
Write a small program that creates an HTML page
that displays the word `color` in 100 different randomly-generated colors.
