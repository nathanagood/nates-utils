#!/usr/bin/env python3
"""
Prints out the value of the configuration as a string that is
suitable for sourcing as environment variables.
"""
import sys
import argparse
import random
import re

EMAIL_DOMAIN = "example.com"
LAST_NAME_SEED_FILE = "lnames.txt"
FIRST_NAME_SEED_FILE = "fnames.txt"

EMAIL_RE = re.compile(r'')

LAST_NAME_SEEDS = open(LAST_NAME_SEED_FILE).read().splitlines()
FIRST_NAME_SEEDS = open(FIRST_NAME_SEED_FILE).read().splitlines()

def email_generator():
    """
    Generates a pretty much random email address, given
    the seed files and domain.
    """
    generated = "{}.{}@{}".format(random.choice(FIRST_NAME_SEEDS),
                                  random.choice(LAST_NAME_SEEDS),
                                  EMAIL_DOMAIN
                                 ).lower()
    return generated

def generate_all(generators):
    """
    """
    out_str = ""
    for gen in generators:
        out_str = out_str + gen()
    return out_str

def email_filter(in_str):
    """
    Replaces email addresses with fake email addresses.
    """
    out_str = in_str
    return out_str

def apply_filters(in_str, filter_set):
    """
    Applies the provied line and returns the result of applying all of the filters.
    """
    out_str = in_str
    for fil in filter_set:
        out_str = fil(out_str)
    return out_str

def main():
    """
    Main function.
    """

    filters = []
    generators = []

    parser = argparse.ArgumentParser(description='Anonymize data in a CSV file.')
    parser.add_argument("-e",
                        "--email-addresses",
                        help="perform smart anonymizing of email addresses",
                        action="store_true")
    parser.add_argument("-g",
                        "--generate",
                        help="generates the anonymous data instead of replacing it from STDIN",
                        action="store_true")
    parser.add_argument("-n", "--number", help="if generating, generates this number")

    args = parser.parse_args()

    if args.email_addresses:
        print("Anonymizing email address...", file=sys.stderr)
        filters.append(email_filter)
        generators.append(email_generator)

    print("Starting...", file=sys.stderr)

    if args.generate:
        for i in range(int(args.number)):
            record = generate_all(generators)
            print(record)
    else:
        for line in sys.stdin:
            filtered = apply_filters(line, filters)
            print(filtered, end='')

    print("Done.", file=sys.stderr)

    return 0

if __name__ == '__main__':
    CODE = main()
    sys.exit(CODE)
