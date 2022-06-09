"""Handle file exclusions."""

from fnmatch import fnmatch
from pathlib import Path

import ivy


@ivy.filters.register(ivy.filters.Filter.LOAD_NODE_FILE)
def exclude(value, filepath):
    """Only process the right kinds of files."""
    if (patterns := ivy.site.config.get("exclude", None)) is None:
        return True
    return not any(fnmatch(filepath, pat) for pat in patterns)


@ivy.filters.register(ivy.filters.Filter.LOAD_NODE_DIR)
def exclude(value, dirpath):
    """Do not process directories with exclusion markers."""
    return not Path(dirpath, ".ivyignore").exists()
