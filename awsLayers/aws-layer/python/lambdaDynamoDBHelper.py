# Standard library imports
# Third party library imports
# Local application imports
# Module Constants


class CONSTANTS:
    RECORDS = 'Records'
    EVENT_ID = 'eventID'
    EVENT_NAME = 'eventName'
    EVENT_NAME_INSERT = 'INSERT'
    EVENT_NAME_MODIFY = 'MODIFY'
    EVENT_NAME_REMOVE = 'REMOVE'
    DYNAMO_DB = 'dynamodb'
    DYNAMO_DB_NEW_IMAGE = 'NewImage'
    DYNAMO_DB_OLD_IMAGE = 'OldImage'
    M_KEY = 'M'


def getEventRecords(dynamoDbEvent):
    return dynamoDbEvent[CONSTANTS.RECORDS] if dynamoDbEvent != None else []


def getEventId(dynamoDbRecord):
    return dynamoDbRecord.get(CONSTANTS.EVENT_ID) if dynamoDbRecord != None else None


def getEventName(dynamoDbRecord):
    return dynamoDbRecord.get(CONSTANTS.EVENT_NAME) if dynamoDbRecord != None else None


def isRecordEventInserted(dynamoDbRecord):
    return getEventName(dynamoDbRecord) == CONSTANTS.EVENT_NAME_INSERT


def isEventModified(dynamoDbRecord):
    return getEventName(dynamoDbRecord) == CONSTANTS.EVENT_NAME_MODIFY


def isEventDeleted(dynamoDbRecord):
    return getEventName(dynamoDbRecord) == CONSTANTS.EVENT_NAME_REMOVE


def getDynamoDBRecord(dynamoDbRecord):
    return dynamoDbRecord.get(CONSTANTS.DYNAMO_DB) if dynamoDbRecord != None else None


def getNewImage(dynamoDbRecord):
    subObject = getDynamoDBRecord(dynamoDbRecord)
    return subObject.get(CONSTANTS.DYNAMO_DB_NEW_IMAGE) if subObject != None else None


def getOldImage(dynamoDbRecord):
    subObject = getDynamoDBRecord(dynamoDbRecord)
    return subObject.get(CONSTANTS.DYNAMO_DB_OLD_IMAGE) if subObject != None else None


def getDictionaryByKey(dataDict, key):
    finalResult = None
    if(dataDict == None):
        return None
    result = dataDict.get(key)
    if(result != None):
        finalResult = result.get(CONSTANTS.M_KEY)
    return finalResult
