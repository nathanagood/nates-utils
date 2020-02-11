#!/usr/bin/env python3
"""
Prints out the value of the configuration as a string that is
suitable for sourcing as environment variables.
"""
import sys
import argparse
import random
import re
import csv
import functools

EMAIL_DOMAIN = "example.com"
LAST_NAME_SEED_FILE = "lnames.txt"
FIRST_NAME_SEED_FILE = "fnames.txt"

EMAIL_RE = re.compile(r'(?P<address>[-_a-z0-9\.]+@[^.]+\.[-_a-z0-9]+)', re.I)

LAST_NAME_SEEDS = open(LAST_NAME_SEED_FILE).read().splitlines()
FIRST_NAME_SEEDS = open(FIRST_NAME_SEED_FILE).read().splitlines()

EMAIL_ADDY_MAP = {}
NUMBER_MAP = {}

NUMBER_FORMAT = "{}"
START_VALUE = 1000
STOP_VALUE = 9999
NUMBER_MAP = {}

def number_generator(fmt, start, stop):
    """
    Generates a mostly random number.
    """
    start_number = start if start is not None else START_VALUE
    stop_number = stop if stop is not None else STOP_VALUE
    generated = fmt.format(random.randint(start_number, stop_number))
    return generated

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

def number_filter(fmt, start, stop, in_str):
    """
    Replaces real numbers with fake numbers.
    """
    out_str = in_str
    if in_str in NUMBER_MAP:
        out_str = NUMBER_MAP[in_str]
    else:
        out_str = number_generator(fmt, start, stop)
        NUMBER_MAP[in_str] = out_str

    return out_str

def email_filter(in_str):
    """
    Replaces email addresses with fake email addresses.
    """
    out_str = in_str
    match = EMAIL_RE.search(out_str)
    if not match:
        return out_str

    email = match.group('address')
    if email in EMAIL_ADDY_MAP:
        anon_email = EMAIL_ADDY_MAP[email]
    else:
        anon_email = email_generator()
        EMAIL_ADDY_MAP[email] = anon_email
    out_str = EMAIL_RE.sub(anon_email, out_str.lower(), 1)
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
    parser.add_argument("-c", "--count", help="if generating, generates this number of items")
    parser.add_argument("-f", "--field", help="operates only on the given field")
    parser.add_argument("-n", "--number", help="randomizes numbers and uses the given number format")
    parser.add_argument("-a", "--start-with", help="uses the provided value as the start")
    parser.add_argument("-z", "--end-with", help="uses the provide value as the end")

    args = parser.parse_args()

    print("Anonymizing field {}".format(args.field), file=sys.stderr)

    if args.email_addresses:
        print("Anonymizing email address...", file=sys.stderr)
        filters.append(email_filter)
        generators.append(email_generator)

    if args.number:
        print("Anonymizing numbers...", file=sys.stderr)
        nf = functools.partial(number_filter, args.number, int(args.start_with), int(args.end_with))
        filters.append(nf)
        ng = functools.partial(number_generator, args.number, int(args.start_with), int(args.end_with))
        generators.append(ng)

    print("Starting...", file=sys.stderr)

    if args.generate:
        for i in range(int(args.count)):
            record = generate_all(generators)
            print(record)
    else:
        # for line in sys.stdin:
        #     filtered = apply_filters(line, filters)
        #     print(filtered, end='')
        record_reader = csv.reader(sys.stdin)
        for row in record_reader:
            filtered_row = []
            idx = 0
            for field in row:
                idx += 1
                if args.field and idx != int(args.field):
                    filtered_row.append(field)
                    continue
                field = apply_filters(field, filters)
                filtered_row.append(field)
            print(','.join(filtered_row))


    print("Done.", file=sys.stderr)

    return 0

if __name__ == '__main__':
    CODE = main()
    sys.exit(CODE)
