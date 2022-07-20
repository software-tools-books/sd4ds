"""Handle file excerpts.

The `[% excerpt ... %]` shortcode includes other files or portions of
other files:

-   `[% excerpt f="path" %]` includes an entire file. The path is
    relative to the including file.

-   `[% excerpt f="path" keep="key" %]` includes everything between
    lines marked with `[key]` and `[/key]`.  (These markers are usually
    placed in comments.)

-   `[% excerpt f="path" omit="key" %]` omits everything between
    markers.

-   `[% excerpt f="path" keep="outer" omit="inner" %]` selects the
    lines within the `outer` section, then omits lines within that
    section marked with `inner`.

-   `[% excerpt pat="path.*" fill="one two" %]` includes the files
    `path.one` and `path.two` (i.e., replaces `*` in `pat` with each
    of the tokens in `fill`, then includes all of that file).

To make this work:

-   `filter_files` tells Ivy to only process files ending in `.html`
    and `.md` so that it won't try to templatize source code files.

-   `copy_files` copies all of the files used as inclusions to the
    output directory so that they can be linked to. It assumes that
    a chapter or appendix `A` generates `docs/A/index.html` so that
    the included file can be copied to `docs/A/whatever`.

-   `excerpt` handles file inclusion.  If the `node` argument is
    empty, it's too early in the processing cycle, so the function
    does nothing; otehrwise, it dispatches to a case-specific handler.
"""

import shutil

import ivy
import shortcodes
import util


@ivy.filters.register(ivy.filters.Filter.LOAD_NODE_FILE)
def filter_files(value, filepath):
    """Only process HTML and Markdown files."""
    result = filepath.suffix in {".html", ".md"}
    return result


@ivy.events.register(ivy.events.Event.EXIT_BUILD)
def copy_files():
    """Copy all included files."""
    # Wrong part of the cycle.
    if (inclusions := util.get_config("inclusions")) is None:
        return

    # Copy files.
    for (src, dst) in inclusions.items():
        shutil.copy(src, dst)


@shortcodes.register("excerpt")
def excerpt(pargs, kwargs, node):
    """Handle a file inclusion, possibly excerpting."""
    # Error checking.
    if pargs:
        util.fail(f"Badly-formatted excerpt shortcode with {pargs} in {node.filepath}")

    # Handle by cases.
    inclusions = util.make_config("inclusions")
    if ("pat" in kwargs) and ("fill" in kwargs):
        return _multi(inclusions, node, **kwargs)
    elif "f" not in kwargs:
        util.fail(f"Badly-formatted excerpt shortcode with {kwargs} in {node.filepath}")
    elif ("keep" in kwargs) and ("omit" in kwargs):
        return _keep_omit(inclusions, node, **kwargs)
    elif "keep" in kwargs:
        return _keep(inclusions, node, **kwargs)
    elif "omit" in kwargs:
        return _omit(inclusions, node, **kwargs)
    else:
        return _file(inclusions, node, **kwargs)


def _file(inclusions, node, f):
    """Handle a simple file inclusion."""
    filepath = _inclusion_filepath(inclusions, node, f)
    return _include_file(node, filepath)


def _keep(inclusions, node, f, keep):
    """Handle a sliced file inclusion."""
    filepath = _inclusion_filepath(inclusions, node, f)
    return _include_file(node, filepath, lambda lns: _keep_lines(filepath, lns, keep))


def _keep_omit(inclusions, node, f, keep, omit):
    """Handle an inclusion that keeps some content but omits other."""
    filepath = _inclusion_filepath(inclusions, node, f)
    return _include_file(
        node,
        filepath,
        lambda lns: _keep_lines(filepath, lns, keep),
        lambda lns: _omit_lines(filepath, lns, omit),
    )


def _multi(inclusions, node, pat, fill):
    """Handle multiple file inclusion."""
    result = []
    replacements = [r.strip() for r in fill.strip().split()]
    replacements = [r for r in replacements if r]
    for rep in replacements:
        file = pat.replace("*", rep)
        result.append(_file(inclusions, node, file))
    return "\n\n".join(result)


def _omit(inclusions, node, f, omit):
    """Handle an erasing file inclusion."""
    filepath = _inclusion_filepath(inclusions, node, f)
    return _include_file(node, filepath, lambda lns: _omit_lines(filepath, lns, omit))


def _find_markers(lines, key):
    """Find start/stop markers in files."""
    start = f"[{key}]"
    stop = f"[/{key}]"
    i_start = None
    i_stop = None
    for (i, line) in enumerate(lines):
        if start in line:
            i_start = i
        elif stop in line:
            i_stop = i
    return i_start, i_stop


def _include_file(node, filepath, *filters):
    """Include a file, filtering if asked to."""
    kind = filepath.split(".")[-1]
    try:
        with open(filepath, "r") as reader:
            lines = reader.readlines()
            for f in filters:
                lines = f(lines)
            return _make_html(kind, lines)
    except OSError:
        util.fail(f"Unable to read inclusion '{filepath}' in {node.filepath}.")


def _keep_lines(filepath, lines, key):
    """Select lines between markers."""
    start, stop = _find_markers(lines, key)
    if (start is None) or (stop is None):
        util.fail(f"Failed to match inclusion 'keep' key {key} in {filepath}")
    return lines[start + 1 : stop]  # noqa e203


def _make_html(kind, lines):
    """Construct HTML inclusion from lines."""
    body = "\n".join(x.rstrip() for x in lines)
    return f"```{kind}\n{body}\n```"


def _omit_lines(filepath, lines, key):
    """Remove lines between markers."""
    start, stop = _find_markers(lines, key)
    if (start is None) or (stop is None):
        util.fail(f"Failed to match inclusion 'omit' key {key} in {filepath}")
    return lines[:start] + lines[stop + 1 :]  # noqa e203


def _inclusion_filepath(inclusions, node, f):
    """Make path to included file."""
    src, dst = util.make_copy_paths(node, f)
    inclusions[src] = dst
    return src
