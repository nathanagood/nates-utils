#!/usr/bin/env python3
"""
Prints out the value of the configuration as a string that is
suitable for sourcing as environment variables.
"""
import os
import sys
import argparse

EMAIL_DOMAIN="example.com"
LAST_NAME_SEED_FILE="lnames.txt"
FIRST_NAME_SEED_FILE="fnames.txt"

EMAIL_RE = re.compile(r'')

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
    for
    return out_str

def main():
    """
    Main function.
    """

    filters = []

    parser = argparse.ArgumentParser(description='Anonymize data in a CSV file.')
    parser.add_argument("-e", "--email-addresses", help="perform smart anonymizing of email addresses", action="store_true")

    args = parser.parse_args()

    if args.email_addresses:
        print("Anonymizing email address...", file=sys.stderr)

    print("Starting anonymization...")

    for line in sys.stdin:
        filtered = apply_filters(line, filters)
        print(filtered, end='')

    print("Done.")

    return 0

if __name__ == '__main__':
    code = main()
    exit(code)
