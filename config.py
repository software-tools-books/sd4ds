"""Ivy configuration file."""

# GitHub repository.
github = "https://github.com/gvwilson/sd4ds"

# Use our own theme.
theme = "mccole"

# Enable various Markdown extensions.
markdown_settings = {
    "extensions": [
        "markdown.extensions.extra",
        "pymdownx.superfences"
    ]
}

# Site title and subtitle.
title = "Software Design for Data Scientists"
tagline = "A modest introduction using Python"

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

# Links (inserted into Markdown files for consistency).
bibliography = "info/bibliography.bib"
bibliography_style = "unsrt"
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

# Debug.
debug = True

# Warn about missing or unused entries.
warnings = False
