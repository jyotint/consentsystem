# Standard library imports
import time
# Third party library imports
# Local application imports
import constants


def getUtcDateTime():
    return time.gmtime()

def getCurrentUtcDateTime():
    return convertDateTimeToString(time.gmtime())

def convertDateTimeToString(datetime):
    return time.strftime(constants.DATETIME_STRING_FORMAT, datetime)

def convertStringToDateTime(datetimeString):
    return time.strptime(datetimeString, constants.DATETIME_STRING_FORMAT)


def MergeDictionaries(dict1, dict2):
    """
    Merges two dictionaries and return a new dictinary
    Python code to merge dict using a single expression
    """
    return {**dict1, **dict2}


def getTraceDict(originId=None, localId=None, status=None, startDateTime=None, endDateTime=None):
    dataDict = []
    traceAttr = constants.TRACE.ATTRIBUTE
    
    if(originId != None):
        dataDict[traceAttr.ORIGIN_ID] = originId
    if(localId != None):
        dataDict[traceAttr.LOCAL_ID] = localId
    if(status != None):
        dataDict[traceAttr.STATUS] = status
    if(startDateTime != None):
        dataDict[traceAttr.START_DATETIME] = convertDateTimeToString(startDateTime)
    if(endDateTime != None):
        dataDict[traceAttr.END_DATETIME] = convertDateTimeToString(endDateTime)
    if(startDateTime != None and endDateTime != None):
        dataDict[traceAttr.DURATION_IN_MS] = endDateTime - startDateTime
    
    return dataDict
