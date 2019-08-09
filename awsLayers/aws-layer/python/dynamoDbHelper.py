# Standard library imports
# Third party library imports
import boto3
# Local application imports
# Module constants and variables


def isOperationSuccessful(result):
    rmd = result.get('ResponseMetadata')
    return (rmd.get('HTTPStatusCode') == 200) if rmd != None else False


def isOperationFailed(result):
    rmd = result.get('ResponseMetadata')
    return (rmd.get('HTTPStatusCode') != 200) if rmd != None else False


def deserializeRecordToDict(dynamoDbRecord):
    if(dynamoDbRecord == None):
        return None
    deserializer = boto3.dynamodb.types.TypeDeserializer()
    return {k: deserializer.deserialize(v)  for k, v in dynamoDbRecord.items()}

def serializeDictToRecord(dataDict):
    if(dataDict == None):
        return None
    serializer = boto3.dynamodb.types.TypeSerializer()
    return {k: serializer.serialize(v)  for k, v in dataDict.items()}
