# Standard library imports
import base64
# Third party library imports
# Local application imports
# Module Constants


class CONSTANTS:
    RECORDS = 'Records'
    KINESIS = 'kinesis'
    DATA = 'data'


def getEventRecords(event):
    return event.get(CONSTANTS.RECORDS) if event != None else []


def getPayloadData(record):
    kinesisObject = record.get(CONSTANTS.KINESIS)
    return kinesisObject.get(CONSTANTS.DATA) if kinesisObject != None else None


def getDecodedPayloadData(record):
    encodedData = getPayloadData(record)
    return base64.b64decode(encodedData) if encodedData != None else None
