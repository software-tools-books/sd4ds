"""Assemble data for analysis."""

import csv
import json

import pandas as pd
import util


def read_combined(stem):
    """Assemble data from a set of files."""
    reference = read_reference_genome(stem)
    phenotypes = _read_phenotypes(stem)

    variants = _read_genomes(stem, phenotypes)
    variants = variants.rename(columns={"base": "alternate"})
    variants["reference"] = variants.apply(
        lambda x: reference["genome"][x["location"] - 1], axis=1
    )
    # re-arrange columns as convention is for reference to come before alternate
    new_cols = ["location", "reference", "alternate", "pid"]
    variants = variants[new_cols]
    combined = pd.merge(phenotypes, variants, on="pid", how="outer")
    return combined


def read_reference_genome(stem):
    """Read reference genome (sequence plus mutation location(s))."""
    filename = util.filename_reference_genome(stem)
    with open(filename, "r") as reader:
        return json.load(reader)


def _read_genomes(stem, raw_phenotypes):
    """Read variant data and combine with reference to create genome."""
    variants = None
    genomes = []
    for pid in raw_phenotypes["pid"]:
        filename = util.filename_person(stem, pid)
        temp = pd.read_csv(filename)
        temp["pid"] = pid
        variants = temp if (variants is None) else pd.concat([variants, temp])
    return variants


def _read_phenotypes(stem):
    """Return raw phenotype data as list of dictionaries."""
    filename = util.filename_phenotypes(stem)
    return pd.read_csv(filename)


if __name__ == "__main__":
    import sys

    combined = read_combined(sys.argv[1])
    print(combined)
