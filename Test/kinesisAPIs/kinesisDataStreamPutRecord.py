import os
import sys
import base64
import json
import argparse
import boto3


def setupAndParseCommandLine(args):
    print(f"run: {args}")
    parser = argparse.ArgumentParser(description = "Post data to to Kinesis")
    parser.add_argument("-p", "--pk", required="True", help="Partition Key")
    parser.add_argument("-f", "--file", default="data.json", required="True", help="JSON data to post in AWS Kinesis Data Stream")
    commandline = parser.parse_args(args)
    print(f"commandline >> ParitiionKey (pk): '{commandline.pk}', file: '{commandline.file}'")
    return commandline


def putRecord(arguments):
    kinesis = boto3.client("kinesis")

    fileData = open(arguments.file, 'r')
    jsonData = json.dumps(fileData.readline())
    print(f"{os.linesep}Request JSON: {os.linesep}{json.dumps(jsonData, indent=2)}")
    encodedJsonData = bytes(jsonData, encoding='utf8')

    request = {
        'StreamName': 'ConsentJson'
        , 'Data': encodedJsonData
        , 'PartitionKey': arguments.pk
    }

    result = kinesis.put_record(**request)
    print(f"{os.linesep}kinesis.put_record() result: {os.linesep}{json.dumps(result, indent=2)}")


if( __name__ == '__main__'):
    arguments = setupAndParseCommandLine(sys.argv[1:])
    putRecord(arguments)
