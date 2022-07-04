"""Utilities."""

from typing import List, Optional

from pydantic import BaseModel

# Number of digits to use in person filenames.
WIDTH = 6


class Person(BaseModel):
    """An individual person.

    Values marked `Optional` are filled in one at a time.
    """

    # Person ID.
    pid: int

    # Genome.
    genome: str

    # Age in years.
    age: Optional[int] = None

    # Genetic sex {"F", "M", "O"}.
    gsex: Optional[str] = None

    # Weight in kg.
    weight: Optional[float] = None


def filename_overall(stem):
    """Where to store overall summary."""
    return f"{stem}-overall.csv"


def filename_parameter(stem):
    """Where to store parameters."""
    return f"{stem}-parameters.json"


def filename_person(stem, pid):
    """Where to store information about a single person."""
    pid_str = str(pid).zfill(WIDTH)
    return f"{stem}-pid{pid_str}.csv"


def filename_phenotypes(stem):
    """Where to store phenotypic data for all people."""
    return f"{stem}-phenotypes.csv"


def filename_reference_genome(stem):
    """Where to store reference genome."""
    return f"{stem}-reference.json"


def pid_width(length):
    """Number of digits in personal information files' names."""
    return max(2, len(str(length)))
