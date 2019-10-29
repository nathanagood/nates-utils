#!/usr/bin/env python3
"""
Prints out a sign-in URL for the current user given a role that the user would
like to assume.
"""
import urllib
import json
import sys
import requests
import boto3


def get_signin_link(aws_role_arn):
    """
    Creates a link that can be used to sign-in for the AWS account as the
    provided role.
    """
    sts_connection = boto3.client('sts')

    assumed_role_object = sts_connection.assume_role(
        RoleArn=aws_role_arn,
        RoleSessionName="AssumeRoleSession",
    )

    url_credentials = {}
    url_credentials['sessionId'] = assumed_role_object.get(
        'Credentials').get('AccessKeyId')
    url_credentials['sessionKey'] = assumed_role_object.get(
        'Credentials').get('SecretAccessKey')
    url_credentials['sessionToken'] = assumed_role_object.get(
        'Credentials').get('SessionToken')
    json_string_with_temp_credentials = json.dumps(url_credentials)

    request_parameters = "?Action=getSigninToken"
    if sys.version_info[0] < 3:
        def quote_plus_function(unquoted):
            return urllib.quote_plus(unquoted)
    else:
        def quote_plus_function(unquoted):
            return urllib.parse.quote_plus(unquoted)
    request_url = "https://signin.aws.amazon.com/federation"
    signin_response = requests.get(
        request_url,
        params={
            'Action': 'getSigninToken',
            'Session': json_string_with_temp_credentials
        })
    signin_token = json.loads(signin_response.text)

    request_parameters = "?Action=login"
    request_parameters += "&Issuer=Example.org"
    request_parameters += "&Destination=" + \
        quote_plus_function("https://console.aws.amazon.com/")
    request_parameters += "&SigninToken=" + signin_token["SigninToken"]
    request_url = "https://signin.aws.amazon.com/federation" + \
        request_parameters

    return request_url


if __name__ == "__main__":
    print(get_signin_link(sys.argv[1]))
