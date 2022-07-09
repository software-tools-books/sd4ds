"""Ivy configuration file."""

# ----------------------------------------

# Abbreviation for this document.
abbrev = "sd4ds"

# GitHub repository.
github = "https://github.com/software-tools-books/sd4ds"

# Site title and subtitle.
title = "Software Design for Data Scientists"
tagline = "A modest introduction using Python"
author = "Greg Wilson"

# Chapters (slugs in order).
chapters = [
    "introduction",
    "persist",
    "dataframe",
    "scraper",
    "pipeline",
    "ingestion",
    "cache",
    "synthetic",
    "invperc",
    "interpreter",
    "unittest",
    "build",
    "reader",
    "versioning",
    "database",
    "binary",
    "regexp",
    "templating",
    "linter",
    "server",
    "compiler",
    "conclusion",
]

# Appendices (slugs in order).
appendices = [
    "bibliography",
    "syllabus",
    "license",
    "conduct",
    "glossary",
    "links",
    "credits",
    "contents",
]

# Use our own theme.
theme = "mccole"

# Enable various Markdown extensions.
markdown_settings = {
    "extensions": [
        "markdown.extensions.extra",
        "pymdownx.superfences"
    ]
}

# Debug.
debug = True

# Warn about missing or unused entries.
warnings = False

# ----------------------------------------

# Links (inserted into Markdown files for consistency).
bibliography = "info/bibliography.bib"
bibliography_style = "unsrt"
credits = "info/credits.yml"
glossary = "info/glossary.yml"
links = "info/links.yml"

# Language code.
lang = "en"

# Input and output directories.
src_dir = "src"
out_dir = "docs"

# Use "a/" URLs instead of "a.html".
extension = "/"

# Files to copy verbatim.
copy = [
    "*.html",
    "*.png",
    "*.py",
    "*.svg",
]

# Exclusions (don't process).
exclude = [
    "*.csv",
    "*.gz",
    "*.out",
    "*.png",
    "*.py",
    "*.pyc",
    "*.svg",
    "*~",
    "*/__pycache__"
]

# Display values for LaTeX generation.
if __name__ == "__main__":
    import sys
    assert len(sys.argv) == 2, "Expect exactly one argument"
    if sys.argv[1] == "--abbrev":
        print(abbrev)
    elif sys.argv[1] == "--latex":
        print(f"\\title{{{title}}}")
        print(f"\\subtitle{{{tagline}}}")
        print(f"\\author{{{author}}}")
    else:
        assert False, f"Unknown flag {sys.argv[1]}"
