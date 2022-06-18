---
title: "A Modest Binary Storage System"
---

All data is stored as 1's and 0's
(or "are" stored, if you're a purist).
The great divide in computing is between 1's and 0's that represent characters
and those that represent something else.
That "something else" is commonly called binary data;
it's usually manipulated using special-purpose software
like image viewers and MP3 players,
your programs can read and write binary data too.

This chapter looks at how binary values are stored and manipulated.
We'll use Python for examples, but the ideas are universal.
Before we start,
please remember that real binary data formats tend to be pretty complicated:
good libraries exist for working with every image, sound, and video format there is:
please don't write one of your own unless you are really sure you need to.

## Why Binary? {: #binary-why}

Why store data in a format that can't be handled by editors like Notepad and Nano?
There are generally four reasons:

1.  Size:
    the string `"10239472"` is 8 bytes long,
    but the 32-bit integer it represents only needs 4 bytes in memory.
    This doesn't matter for small data sets
    (what's a few megabytes here and there?),
    but it does for large ones,
    and it definitely does when data has to be moved between disk and memory
    or between different computers.

2.  Speed:
    adding the integers 34 and 56 is a single machine operation.
    Adding the values represented by the strings `"34"` and `"56"` is dozens:

    ```
    def add_double_digits(left, right):
        left_val = 10 * (left[0] - "0") + (left[1] - "0")
        right_val = 10 * (right[0] - "0") + (right[1] - "0")
        result_val = left_val + right_val
        if result_val > 100:
            result = "0" + (result_val % 100)
            result = result - 100
        else:
            result_val = ""
        result += "0" + (result_val / 10)
        result += "0" + (result_val % 10)
        return result
    ```

    (This doesn't actually work as written---I should use
    the built-in `ord` and `chr` functions in a few places---but
    you get the idea.)
    Most programs that read and
    write text files convert the values in those files into binary data
    using the `int` or `float` functions,
    but if we're going to process the data many times,
    it makes sense to avoid paying the conversion cost over and over.

3.  Hardware interfaces:
    someone, somewhere, has to convert the signal from the gas chromatograph
    to a number,
    and that signal probably arrives arrives as a stream of 1's and 0's.

4.  Lack of anything better:
    it's possible to represent images as text---think of ASCII art---but sound?
    Or video?
    It would be possible, but it would hardly be sensible.

## Storage {: #binary-storage}

Let's start by looking at how numbers are stored.
If we only have 1's and 0's,
the natural way to store a positive integer is to use base 2,
so \\(1001_2\\) is \\((1×2^3)+(0×2^2)+(0×2^1)+(1×2^0) = 9_{10}\\).
It's equally natural to extend this scheme to negative numbers
by reserving one bit for the sign:
if we use 0 for positive numbers and 1 for those that are negative,
\\(+9_{10}\\) would be \\(01001_2\\)
and \\(9_{10}\\) would be \\(11001_2\\).

But there are two problems with this.
The first is that this scheme gives us two representations for zero
(\\(00000_2\\) and \\(10000_2\\)).
This isn't fatal,
but any claims this scheme has to being "natural" disappear
when we have to write code like:

```{: .python}
if (length != +0) and (length != -0):
```

As for the other problem,
it turns out that the circuits needed to do addition and other arithmetic
on this *sign and magnitude* representation
is more complicated than the hardware needed for another called *two's complement*.
Instead of mirroring positive values,
two's complement "rolls over" when going below zero like a car's odometer.
If we're using four bits per number so that \\(0_{10}\\) is \\(0000_2\\),
then \\(-1_{10}\\) is \\(1111_2\\).
\\(-2_{10}\\) is \\(1110_2\\),
\\(-3_{10}\\) is \\(1101_2\\),
and so on until we reach the most negative number we can represent,
\\(1000_2\\),
which is -8.
Our representation then wraps around again,
so that \\(0111_2\\) is \\(7_{10}\\).

This scheme isn't intuitive,
but it solves sign and magnitude's "double zero" problem
and the hardware to handle it is faster and cheaper.
As a bonus,
we can still tell whether a number is positive or negative
by looking at the first bit:
negative numbers have a 1, positives have a 0.
The only odd thing is its asymmetry:
because 0 counts as a positive number,
numbers go from -8 to 7, or -16 to 15.

So much for integers:
what about floating-point numbers?
The simple version is that floats are stored using one bit for the sign,
a few bits for the exponent,
and the remaining bits for the fractional part,
or *mantissa*.
The real story is much more complicated---the mantissa
may be shifted around to avoid leading zeroes,
for example,
and some bit patterns are reserved for positive and negative infinity---but
those details don't matter when we're doing I/O.

## Input and Output {: #binary-io}

Most functions that handle text pretend that files are made up of lines:
they read characters until they see an end-of-line marker,
then hand back those characters as a string.
We can also use character-oriented routines,
the most basic of which is simply called `read`.
If `stream` is an open file,
then `stream.read(N)` hands back up to the next N bytes from the file
("up to", because there might not be that much data left).
The result is returned as a string,
but---and this is crucial---there is no guarantee that the values represent characters.
We can concatenate it with other text,
or use methods like `str.count` to see how many times some pattern occurs in it,
but the "characters" might actually be bytes in an image.

Where there's a `read` there's a `write`,
and sure enough,
`stream.write(str)` writes the string `str` to a file that has been opened for writing.
In both the reading and writing cases,
it's important to open the file in *binary mode* using either:

```
reader = open('input.dat', 'rb')
```

or:
{: .continue}

```
writer = open('input.dat', 'wb')
```

The `"b"` at the end of the mode string tells Python *not* to "help" us
by translating Windows line endings (which are the two characters `"\r\n"`)
into Unix line endings (the single character `"\n"`).
This translation is handy when we're working with text,
since it means our programs only have to deal with one style of line ending
no mater what platform the code is running on,
but it messes up non-textual data.

## Packing and Unpacking {: #binary-packing}

There's another tricky bit here as well.
In C and Fortran,
integers are "naked" 32-bit values:
the program uses what the machine provides,
no more and no less.
Python, Java, and other languages usually don't use raw values, though;
instead,
they usually put the value in a larger data structure that keeps track of its type,
whether anything is still referring to it,
and so on.
This extra data allows those languages to recycle memory that's no longer being used;
it also allows us to assign values to variables without explicitly declaring their type,
since the value we're assigning carries its type along with it.

A similar issue comes up when we compare Fortran's arrays to Python's lists.
In Fortran,
the data in an array is stored contiguously in memory,
i.e.,
the array's values are side by side in one big block of memory without any holes.
Writing this to disk is easy:
if the array starts at location L in memory and has N values,
each of which is B bytes in size, we just copy the bytes from L to L+NB-1 to the file.

A Python list,
on the other hand,
may be broken into many scattered blocks,
and what it actually stores is pointers to values rather than the values themselves.
To put the values in a file
we can either write them one at a time or pack them into a contiguous block and write that.
Similarly,
when reading from a file,
we can either grab the values one by one or read a larger block and then unpack it in memory.

Packing data is a lot like formatting values for textual output.
The *format* specifies what types of data are being packed,
how big they are (e.g., is this a 32-bit or 64-bit floating point number?),
and how many values there are.
Putting it all together,
the format exactly determines how much memory is required by the packed representation.
The result of packing values is a block of bytes.

Unpacking reverses this process.
After reading data into memory,
we can unpack it according to a format.
The most important thing is that
*we can unpack data any way we want*.
We might pack an integer and then unpack it as four characters,
since both are 32 bits long.
Or we might save two characters, an integer, and two more characters,
then unpack it as a 64-bit floating point number.
The bits are just bits:
it's *our* responsibility to make sure we keep track of their meaning
when they're down there on disk,
all alone in the cold.

In Python,
we use the `struct` module to do this packing and unpacking.
The function `pack(format, val_1, val_2, ...)`
takes a format string and a bunch of values as arguments,
packs then into a block of bytes,
and gives that back to us.
The inverse function `unpack(format, string)`
takes a block of bytes and a format,
and returns a tuple containing the unpacked values:

```{: .python title="simple_struct.py"}
import struct

fmt = "ii" # two 32-bit integers
x = 31
y = 65

binary = struct.pack(fmt, x, y)
print("binary representation:", repr(binary))

normal = struct.unpack(fmt, binary)
print("back to normal:", normal)
```
```{: .text}
binary representation: b'\x1f\x00\x00\x00A\x00\x00\x00'
back to normal: (31, 65)
```

What is `\x1f` and why is it in our data?
Well,
if Python finds a character in a string that doesn't have a printable representation,
it prints a 2-digit escape sequence in hexadecimal.
Python is therefore trying to tell us that our string contains the eight bytes
`['x1f', 'x00', 'x00', 'x00', 'A', 'x00', 'x00', 'x00']`.
That actually makes sense:
`1f` in hex is \\((1×{16}^1)+(15×{16}^0)\\) or 31.
And `"A"`?
That's our 65,
because the ASCII code for an upper-case letter A is the decimal value 65.
All the other bytes are zeroes (`"x00"`)
because each of our integers is 32 bits long,
and the significant digits only fill one byte's worth of each.

The `struct` module offers a lot of different formats:

| Format | Meaning |
| ------ | ------- |
| `"c"`  | Single character (i.e., string of length 1) |
| `"B"`  | Unsigned 8-bit integer |
| `"h"`  | Short (16-bit) integer |
| `"i"`  | 32-bit integer |
| `"f"`  | 32-bit float |
| `"d"`  | Double-precision (64-bit) float |

The `"B"` and `"h"` formats deserve some explanation.
`"B"` takes the least significant 8 bits out of an integer and packs those;
`"h"` takes the least significant 16 bits and does likewise.
They're useful because binary data formats often store only as much data as they need to,
so we need a way to get 8- and 16-bit values out of files.
(Many audio formats, for example, only store 16 bits per sample.)

Any format can be preceded by a count,
so the format `"3i"` means "three integers".
For example:

```{: .python title="mistaken.py"}
from struct import pack

print(repr(pack("3i", 1, 2, 3)))
print(repr(pack("5s", bytes("hello", "utf-8"))))
print(repr(pack("5s", bytes("a longer string", "utf-8"))))
```
```{: .text}
b'\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00'
b'hello'
b'a lon'
```

Oops:
we told Python to pack five characters,
so we only got the first five characters of our string.
How can we tell it to pack all the data that's there regardless of length?

The answer is that we can't:
we *must* specify how much we want packed.
But that doesn't mean we can't handle variable-length strings;
it just means that we have to construct the format on the fly.
Have a look at this:

```{: .python}
format = '%ds' % len(message)
```

`len(str)` is the length of the string `str`,
and the old-fashioned format `"%d"` means "a decimal integer",
so `"%ds"` is "a decimal integer followed by the literal letter 's'".
If `message` contains the string `"example"`,
the expression above will assign the string `"7s"` to `format`,
which is exactly the right format to use to pack it,
since it's a 7-character string.

That's fine for writing,
how do we know how much data to get if we're reading?
For example,
suppose I have the two strings "hello" and "Python".
I can pack them like this:

```{: .python}
buffer = pack("5s6s", "hello", "Python")
```

but how do I know how to unpack 5 characters then 6
rather than 2 and then 9,
or 2, 7, and 2?

The trick is to save the size along with the string
to create *self-describing data*.
If we always use exactly the same number of bytes to store the size,
we can read it back reliably
and then use it to figure out how big our string is:

```{: .python title="flexible.py"}
def pack_string(str):
    header = pack("i", len(str))
    body_format = "%ds" % len(str)
    body = pack(body_format, str)
    return header + body

packed = pack_string("hello")
print(repr(packed))
```
```text
b'\x05\x00\x00\x00hello'
```

The unpacking function is only a few lines longer:

```{: .python title="flexible.py"}
def unpack_string(buffer):
    header, body = buffer[:4], buffer[4:]
    unpacked_header = unpack("i", header)
    length = unpacked_header[0]
    body_format = "%ds" % length
    result = unpack(body_format, body)
    return str(result[0], "utf-8")

unpacked = unpack_string(packed)
print(unpacked)
```

First, we break the buffer into two parts:
a header that's exactly four bytes long
(i.e., the right size for an integer)
and a body made up of whatever's left.
We then unpack the header,
whose format we know,
to determine how many bytes are in the string.
Once we have that
we use the trick shown earlier to construct the right format on the fly
and then unpack the string and return it.

Rather than counting bytes,
you should also use the `struct` library's `calcsize` function,
which tells you how large (in bytes) the data produced or consumed by a format will be.
For example:

```{: .python title="calc_size.py"}
from struct import calcsize

print(calcsize("4s"))
print(calcsize("3i4s5d"))
```
```{: .text}
4
56
```

Binary data is to programming what chemistry is to biology:
you don't want to spend any more time thinking at that level than you have to,
but when you *do* have to,
there's no substitute.
Please always remember that libraries already exist to handle
(almost) every binary format ever created
and to read data from almost every instrument on the market,
so you shouldn't worry about 1's and 0's unless you really have to.

## Exercises {: #binary-exericses}

### Big-endian vs. little-endian

The packed representation of the integer 5 is `b'\x05\x00\x00\x00'`.
This is called *little-endian*, and is used by Intel and ARM processors.
Some other processors put the most significant byte first (which is called *big-endian*).
There are pro's and con's to both that we won't go into here;
what you *do* need to know is that if you move data from one architecture to another,
it's your responsibility to flip the bytes around,
because *the machine doesn't know what the bytes mean*.
This is such a pain that the `struct` library,
and other libraries like in other languages,
will do things for you if you ask it to.
If you're using `struct`,
the first character of a format string optionally indicates the byte order:

| Character | Byte order    | Size     | Alignment |
| --------- | ------------- | -------- | --------- |
| `@`       | native        | native   | native |
| `=`       | native        | standard | none |
| `<`       | little endian | standard | none |
| `>`       | big endian    | standard | none |
| `!`       | network       | standard | none |

The last entry is the most important.
The protocols used for transmitting data around the Internet all use the same byte order.
For historical reasons it is big-endian,
which means that in almost all cases,
data is flipped from little-endian order to big-endian,
transmitted,
then flipped back.
That doesn't matter:
what does is that it's a standard,
so if you think you're going to want to move your data from machine to machine
(either over the web or forward through time),
you should use '!' as the first character in your format strings.
