#!/usr/bin/env python3
"""
Prints out the value of the configuration as a string that is
suitable for sourcing as environment variables.
"""
import os
import sys
import configparser

USER_HOME = os.path.expanduser("~")
AWS_FILE_NAME = os.path.join(USER_HOME, ".aws/credentials")


def main():
    """
    Main function.
    """
    aws_config = configparser.ConfigParser()
    aws_config.read(AWS_FILE_NAME)
    try:
        aws_profile_name = sys.argv[1]
    except IndexError:
        aws_profile_name = 'default'

    aws_access_key_id = aws_config[aws_profile_name]['aws_access_key_id']
    aws_secret_access_key = aws_config[aws_profile_name][
        'aws_secret_access_key']

    print(f"export AWS_ACCESS_KEY_ID={aws_access_key_id}")
    print(f"export AWS_SECRET_ACCESS_KEY={aws_secret_access_key}")


if __name__ == '__main__':
    main()
