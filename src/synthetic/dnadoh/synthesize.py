"""Synthesize data."""

import argparse
import csv
import json
import random
import sys
from typing import List, Optional

import util
from pydantic import BaseModel

# --------------------------------------------------------------------------------------
# Genomes
# --------------------------------------------------------------------------------------


# Bases (doh).
DNA = "ACGT"

# Probabilities of single nucleotide variations. The original base (from the reference
# genome) will be select 50% of the time; the other three bases will be shuffled and
# one selected per person with the given probabilities.
SNP_PROBS = (0.50, 0.25, 0.13, 0.12)


class GenePool(BaseModel):
    """A set of genomes."""

    # Number of bases in each genome.
    length: int

    # Reference genome without mutations.
    reference: str

    # Individual genomes.
    individuals: List[str]

    # Locations of mutations.
    locations: List[int]

    def __str__(self):
        """Printable representation."""
        return "\n".join(
            [
                f"length: {self.length}",
                f"reference: {self.reference}",
                "individuals:",
                "\n".join(f"- {i}" for i in self.individuals),
                "locations:",
                "\n".join(f"- {loc}" for loc in self.locations),
            ]
        )


def random_sequence(length):
    """Generate a random sequence of bases of the specified length."""
    assert 0 < length
    return "".join(random.choices(DNA, k=length))


def random_genomes(length, num_genomes, num_snps, max_num_other_mutations):
    """Generate a set of genomes with specified number of point mutations.

    1.  Create a reference genome.
    2.  Generate `num_genomes` copies.
    3.  Pick `num_mutations` distinct locations.
    4.  Introduce significant mutations using `SNP_PROBS` as weights.
    5.  Introduce up to `max_num_other_mutations` at other locations (unweighted).
    """
    assert 0 <= num_snps <= length

    # Reference genomes and specific genomes to modify.
    reference = random_sequence(length)
    individuals = [reference] * num_genomes

    # Locations for SNPs.
    locations = random.sample(list(range(length)), num_snps)

    # Introduce significant mutations.
    for loc in locations:
        candidates = _other_bases(reference, loc)
        bases = [reference[loc]] + random.sample(candidates, k=len(candidates))
        individuals = [
            _mutate_significant(reference, ind, loc, bases) for ind in individuals
        ]

    # Introduce other random mutations.
    other_locations = list(set(range(length)) - set(locations))
    individuals = [
        _mutate_other(ind, max_num_other_mutations, other_locations)
        for ind in individuals
    ]

    # Return structure.
    return GenePool(
        length=length, reference=reference, individuals=individuals, locations=locations
    )


def _mutate_significant(reference, genome, loc, bases):
    """Introduce mutations at the specified location.

    The base from the reference genome must be first in `bases` and is
    retained with probability `SNP_PROBS[0]`.  The other bases are
    selected with the other weights from `SNP_PROBS`.
    """
    choice = _choose_one(bases, SNP_PROBS)
    return genome[:loc] + choice + genome[loc + 1 :]


def _mutate_other(genome, max_num_mutations, locations):
    """Introduce up to `max_num_mutations` at specified locations."""
    num = min(max_num_mutations, len(genome))
    for loc in random.sample(locations, k=num):
        base = random.choice(_other_bases(genome, loc))
        genome = genome[:loc] + base + genome[loc + 1 :]
    return genome


# --------------------------------------------------------------------------------------
# People
# --------------------------------------------------------------------------------------


PID_WIDTH = 6  # number of digits in PID


class Person(BaseModel):
    """An individual person.

    Values marked `Optional` are filled in one at a time.
    """

    # Personal identifier.
    pid: str

    # Genome.
    genome: str

    # Age in years.
    age: Optional[int] = None

    # Genetic sex {"F", "M", "O"}.
    gsex: Optional[str] = None

    # Weight in kg.
    weight: Optional[float] = None


class PersonGenerator:
    """Generate a person given a set of parameters."""

    # Minimum and maximum ages in years.
    MIN_AGE = 25
    MAX_AGE = 75

    # Genetic sex and probability of each.
    GSEX = ("F", "M", "O")
    GSEX_PROBS = (0.49, 0.48, 0.03)

    # Mean weight in kg by genetic sex and relative standard deviation of weights.
    WEIGHT_MEANS = {"F": 80.0, "M": 87.0, "O": 84.0}
    WEIGHT_RSD = 0.12

    def __init__(self):
        """Construct generator."""

    def make(self, reference, individual, pid):
        """Generate a new random person."""
        person = Person(pid=self._make_pid(pid), genome=individual)
        for method in (self.make_age, self.make_gsex, self.make_weight):
            method(person, reference, individual)
        return person

    def make_age(self, person, reference, individual):
        """Generate a random age.

        Ages are selected uniformly within bounds.
        """
        person.age = random.randint(self.MIN_AGE, self.MAX_AGE)

    def make_gsex(self, person, reference, individual):
        """Generate a random genetic sex.

        Genetic sexes are chosen using weighted probabilities.
        """
        person.gsex = _choose_one(self.GSEX, self.GSEX_PROBS)

    def make_weight(self, person, reference, individual):
        """Generate a random weight.

        Weights are chosen from a normal distribution based on genetic sex.
        """
        assert person.gsex is not None
        mean = self.WEIGHT_MEANS[person.gsex]
        std_dev = mean * self.WEIGHT_RSD
        person.weight = _truncate(random.gauss(mean, std_dev), 1)

    def _make_pid(self, i):
        """Create personal identifier."""
        return str(i).zfill(PID_WIDTH)


def adjust_all(genomes, people, func):
    """Adjust a single value based on an SNP.

    1.  Choose one of the mutation locations at random.
    2.  Select a base other than the one in the reference genome at that location.
    3.  Apply the mutation function to everyone who has that base at that location.
    """
    if not genomes.locations:
        return
    loc = random.choice(genomes.locations)
    candidates = _other_bases(genomes.reference, loc)
    marker = random.choice(list(candidates))
    for person in people:
        if person.genome[loc] == marker:
            func(person)


def adjust_weight(person):
    """Adjust a person's weight upward by 10%."""
    person.weight = _truncate(1.1 * person.weight, 1)


# --------------------------------------------------------------------------------------
# I/O
# --------------------------------------------------------------------------------------


def _write_summary(writer, options, genomes, people):
    """Write summary information interactive use."""
    print("parameters:")
    for key in vars(options):
        print(f"- {key}: {getattr(options, key)}")
    print(genomes, file=writer)
    for p in people:
        print(p, file=writer)


def _write_files(options, genomes, people):
    """Write people as CSV."""
    assert people
    _write_options(options)
    _write_overall(options, people)
    _write_reference_genome(options, genomes)
    _write_variants(options, genomes, people)
    _write_phenotypes(options, people)


def _write_options(options):
    """Save parameter settings."""
    filename = util.filename_parameter(options.output_stem)
    with open(filename, "w") as writer:
        json.dump(vars(options), writer)


def _write_overall(options, people):
    """Write DNA sequences and people for reference."""
    filename = util.filename_overall(options.output_stem)
    headings = people[0].dict().keys()
    with open(filename, "w") as raw:
        writer = csv.DictWriter(raw, fieldnames=headings)
        writer.writeheader()
        for person in people:
            writer.writerow(person.dict())


def _write_reference_genome(options, genomes):
    """Save the reference genome and related information."""
    filename = util.filename_reference_genome(options.output_stem)
    data = {"genome": genomes.reference, "locations": list(sorted(genomes.locations))}
    with open(filename, "w") as writer:
        json.dump(data, writer)


def _write_variants(options, genomes, people):
    """Write one variant file per person."""
    for person in people:
        filename = util.filename_person(options.output_stem, person.pid)
        with open(filename, "w") as raw:
            writer = csv.DictWriter(raw, fieldnames=["location", "base"])
            writer.writeheader()
            for i in range(len(genomes.reference)):
                if person.genome[i] != genomes.reference[i]:
                    writer.writerow({"location": i + 1, "base": person.genome[i]})


def _write_phenotypes(options, people):
    """Write phenotypic data for people."""
    filename = util.filename_phenotypes(options.output_stem)
    headings = people[0].dict()
    del headings["genome"]
    with open(filename, "w") as raw:
        writer = csv.DictWriter(raw, fieldnames=headings)
        writer.writeheader()
        for person in people:
            details = person.dict()
            del details["genome"]
            writer.writerow(details)


# --------------------------------------------------------------------------------------
# Utilities
# --------------------------------------------------------------------------------------


def _choose_one(values, weights):
    """Convenience wrapper to choose a single items with weighted probabilities."""
    return random.choices(values, weights=weights, k=1)[0]


def _other_bases(seq, loc):
    """Create a list of bases minus the one in the sequence at that location.

    We return a list instead of a set because the result is used in random.choices(),
    which requires an indexable sequence.
    """
    return list(set(DNA) - {seq[loc]})


def _truncate(num, digits):
    """Truncate a number to the specified number of fractional digits."""
    scale = 10**digits
    return int(scale * num) / scale


# --------------------------------------------------------------------------------------
# Main driver
# --------------------------------------------------------------------------------------


def main():
    """Main driver."""
    options = parse_args()
    random.seed(options.seed)
    genomes, people = generate(options)
    if options.output_stem:
        _write_files(options, genomes, people)
    else:
        _write_summary(sys.stdout, options, genomes, people)


def parse_args():
    """Get command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--parameters", type=str, default=None, help="JSON parameter file"
    )
    parser.add_argument("--length", type=int, default=None, help="genome length")
    parser.add_argument(
        "--num_genomes", type=int, default=None, help="number of genomes (people)"
    )
    parser.add_argument(
        "--num_mutations",
        type=int,
        default=None,
        help="number of significant mutations",
    )
    parser.add_argument(
        "--max_num_other_mutations",
        type=int,
        default=None,
        help="maximum number of other mutations per person",
    )
    parser.add_argument("--seed", type=int, default=None, help="RNG seed")
    parser.add_argument(
        "--output_stem", type=str, default=None, help="output path/file stem"
    )

    options = parser.parse_args()
    if options.parameters:
        assert (
            (options.length is None)
            and (options.num_genomes is None)
            and (options.num_mutations is None)
            and (options.max_num_other_mutations is None)
        ), "Cannot specify individual parameters and parameter file"
        with open(options.parameters, "r") as reader:
            parameters = json.load(reader)
            for key in parameters:
                setattr(options, key, parameters[key])

    assert options.seed is not None, "Must specify random number seed"
    return options


def generate(options):
    """Generate genomes and people from parameters."""
    genomes = random_genomes(
        options.length,
        options.num_genomes,
        options.num_mutations,
        options.max_num_other_mutations,
    )
    pg = PersonGenerator()
    people = [pg.make(genomes.reference, ind, i + 1) for (i, ind) in enumerate(genomes.individuals)]
    adjust_all(genomes, people, adjust_weight)
    return genomes, people


if __name__ == "__main__":
    main()
