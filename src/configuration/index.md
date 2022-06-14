---
title: "A Minimal Configuration Manager"
---

-   Current configuration syntax allows one "overall" section and one section per pipeline stage
-   What if we want to share the overall configuration between multiple pipelines?
-   Or share some settings for a particular stage across all uses of that stage?
-   Use a layered configuration that takes configuration in this order:
    1.  A system-wide configuration file for general settings.
    2.  A user-specific configuration file for personal preferences.
    3.  Project-specific files.
    4.  Analysis-specific files.
    5.  Command-line arguments.
-   Each level adds to or overrides settings in the layer before it
    -   Example: `.gitignore` files
-   First step: modify `pipeline`

```{: .python}
SYSTEM_CONFIG = "/etc/nitinat.yml"


def pipeline(config_file, available):
    """Construct and run a processing pipeline.""
    # Set up.
    layered = read_layered_config(config_file)
    raw_config = _read_config(config_file)
    overall, stages = split_config(raw_config)
    overall = layered | overall

    # Run each stage in turn.
    # ...as before...

    # Return final result.
    return provenance, data
```

-   Write the function to read and overlay several configuration files
    -   Yes, we've used the `:=` operator - we're sinners...

```{: .python}
def read_layered_config(config_file):
    """Read layered configuration files in order."""
    all_filenames = [SYSTEM_CONFIG, _get_home_dir().joinpath(".nitinat.yml")]
    if (project_config := _find_project_config(config_file)):
        all_filenames.append(project_config)
    config = {}
    for filename in all_filenames:
        if Path(filename).exists():
            config |= _read_config(filename)
    return config
```

-   Now look for the project configuration file
    -   Search up from the directory containing the file specified for the run
    -   Stop at the user's home directory
    -   Might be better to stop at the root of the Git repository?

```{: .python}
def _find_project_config(starting_point):
    """Look up from given file to find project configuration file."""
    curdir = Path(starting_point).resolve().parent
    home = _get_home_dir()
    while curdir > home:
        candidate = curdir.joinpath(".nitinat.yml")
        if candidate.exists():
            return candidate
        curdir = curdir.parent
    return None
```

-   Relies on a helper function `_get_home_dir`
    -   Originally just used `Path.home()`
    -   But discovered we need to patch this when testing

```{: .python}
def _get_home_dir():  # pragma: no cover
    """Get current user's home directory."""
    return Path.home()
```

-   To test:
    -   Patch `_read_config` with a sequence of return values (one per config file)
    -   Replace the entire file system
-   Install [pyfakefs][pyfakefs]
    -   Add it to `development.txt`, not `requirements.txt`
-   Use the `fs` fixture it provides to manipulate an in-memory filesystem
    -   Functions like `open` are patched behind the scenes to use it

```{: .python}
from nitinat.pipeline4 import SYSTEM_CONFIG, read_layered_config

GET_HOME_DIR = "nitinat.pipeline4._get_home_dir"


def make_file(fs, path, contents):
    fs.create_file(path, contents=yaml.dump(contents))


def test_layered_config_read_system(fs):
    fs.cwd = "/home/person/project/analysis"
    expected = {"alpha": 1}
    make_file(fs, SYSTEM_CONFIG, expected)
    with patch(GET_HOME_DIR, return_value=Path("/home/person")):
        actual = read_layered_config("test.yml")
    assert actual == expected
```

-   Line by line, `test_layered_config_read_system`:
    1.  Is given the `fs` fixture created by `pyfakefs`
    2.  Specifies the pretended current working directory
    3.  Creates the expected configuration as a dictionary
    4.  Calls `make_file` to turn that dictionary into a file in the fake filesystem
        -   `make_file` uses `fs.create_file`
        -   Pulling this out into a one-line function makes the tests easier to read
    5.  Patch the `_get_home_dir` helper function to return the right value
    6.  Reads the layered configuration
        -   Which should get just the system-wide configuration
    7.  Checks
-   Here's a test of multiple configuration files layering correctly:

```{: .python}
def test_layered_config_combine_files(fs):
    fs.cwd = "/home/person/project/analysis"
    make_file(fs, SYSTEM_CONFIG, {"alpha": 1})
    make_file(fs, "/home/person/.nitinat.yml", {"beta": 2})
    make_file(fs, "/home/person/project/.nitinat.yml", {"gamma": 3})
    with patch(GET_HOME_DIR, return_value=Path("/home/person")):
        actual = read_layered_config("temp/test.yml")
    assert actual == {"alpha": 1, "beta": 2, "gamma": 3}
```

-   Everything else in the pipeline code stays the same
-   So the provenance record for each stage has the complete configuration
    -   We really should write at least a couple of tests for that...
