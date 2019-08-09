# Standard library imports
import json
# Third party library imports
# Local application imports
import constants


def encodeStringToBytes(data, encoding='utf-8'):
    return bytes(data, encoding=encoding)

def decodeBytesToString(data, encoding='utf-8'):
    return data.decode(encoding=encoding)


def convertObjectToJson(obj, indent=None):
    """
    Serialize obj to a JSON formatted str.
    """
    return json.dumps(obj, indent=indent)

def convertDataToObject(data):
    """
    Deserialize data (a str, bytes or bytearray instance containing a JSON document) to a Python object.
    """
    return json.loads(data)


def MergeDictionaries(dict1, dict2):
    """
    Merges two dictionaries and return a new dictinary (Python code to merge dict using a single expression)
    """
    return {**dict1, **dict2}


def getTraceDict(originId=None, localId=None, status=None, message=None, startDateTime=None, endDateTime=None, duration=None):
    dataDict = {}
    traceAttr = constants.TRACE.ATTRIBUTE
    
    if(originId != None):
        dataDict[traceAttr.ORIGIN_ID] = originId
    if(localId != None):
        dataDict[traceAttr.LOCAL_ID] = localId
    if(status != None):
        dataDict[traceAttr.STATUS] = status
    if(message != None):
        dataDict[traceAttr.MESSAGE] = message
    if(startDateTime != None):
        dataDict[traceAttr.START_DATETIME] = startDateTime
    if(endDateTime != None):
        dataDict[traceAttr.END_DATETIME] = endDateTime
    if(startDateTime != None and endDateTime != None):
        dataDict[traceAttr.DURATION] = duration
    
    return dataDict
