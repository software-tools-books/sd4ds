#!/usr/bin/env python

"""Check project."""


import argparse
import re
import sys

from pathlib import Path


INDEX_FILE = "index.md"
RE_FILE = re.compile(r'\[%\s+excerpt.+?f="(.+?)".+?%\]')
RE_PAT = re.compile(r'\[%\s+excerpt.+?pat="(.+?)"\s+fill="(.+?)".+?%\]')


def main():
    """Main driver."""
    options = parse_args()
    for (dirname, filename) in get_sources(options):
        check_excerpts(dirname, filename)


def check_excerpts(dirname, filename):
    """Check for excerpted files."""
    referenced = get_excerpts(Path(dirname, filename))
    existing = get_files(dirname)
    report(dirname, "excerpts", referenced, existing)


def get_excerpts(filename):
    """Find excerpt filenames."""
    with open(filename, "r") as reader:
        text = reader.read()
        result = {m.group(1) for m in RE_FILE.finditer(text)}
        pats = [(m.group(1), m.group(2)) for m in RE_PAT.finditer(text)]
        for (pat, fill) in pats:
            result |= {pat.replace("*", f) for f in fill.split()}
        return result


def get_files(dirname):
    """Return set of files."""
    return set(f.name for f in Path(dirname).iterdir() if f.is_file() and (f.name != INDEX_FILE))


def get_sources(options):
    """Get (file, dir) pairs for processing."""
    result = [(options.src, INDEX_FILE)]
    subdirs = [s for s in Path(options.src).iterdir() if s.is_dir()]
    return result + [(s, INDEX_FILE) for s in subdirs]


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--src", required=True, help="Source directory")
    return parser.parse_args()


def report(dirname, title, expected, actual):
    """Report problems."""
    if expected == actual:
        return
    print(f"{dirname}: {title}")
    for (subtitle, items) in [("missing", expected - actual), ("extra", actual - expected)]:
        if not items:
            continue
        print(f"- {subtitle}")
        for i in sorted(items):
            print(f"  - {i}")


if __name__ == "__main__":
    main()
