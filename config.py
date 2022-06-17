"""Ivy configuration file."""

# GitHub repository.
github = "https://github.com/gvwilson/sd4ds"

# Use our own theme.
theme = "mccole"

# Enable various Markdown extensions.
markdown_settings = {
    "extensions": ["markdown.extensions.extra", "pymdownx.superfences"]
}

# Site title and subtitle.
title = "Software Design for Data Scientists"
tagline = "A modest introduction using Python"

# Chapters (slugs in order).
chapters = [
    "introduction",
    "toolkit",
    "dataframe",
    "pipeline",
    "configuration",
    "cache",
    "interpreter",
    "unittest",
    "build",
    "reader",
    "versioning",
    "packaging",
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
    "license",
    "conduct",
    "bibliography",
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
    "*.py",
    "*.svg",
]

# Exclusions (don't process).
exclude = [
    "*.csv",
    "*.gz",
    "*.py",
    "*.pyc",
    "*.svg",
    "*~",
    "*/__pycache__"
]

# Warn about missing or unused entries.
warnings = False
