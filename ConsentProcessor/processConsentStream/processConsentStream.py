# Standard library imports
import base64
import json
# Third party library imports
# Local application imports
import helper
from constants import *
from apiMgmt import API
from customerConsentProcessDataTable import CustomerConsentProcessDataTable
# Module Constants


print('Loading function')


def addPrimaryAndSortKey(requestDict, dataDict, baseTable, baseTableAttr):
    # Set Primary and Sort Key
    dataDict[baseTableAttr.CUSTOMER_MK] = requestDict[baseTable.INCOMING_DATA.CUSTOMER_MK] 
    dataDict[baseTableAttr.SORT_KEY] = helper.getCurrentUtcDateTime()


def transformIncomingJson(requestDict):
    # TODO
    # transformedDict = {}
    transformedDict = API.composeResult(API.STATUS_CODE.SUCCESS, data=requestDict)
    return transformedDict


def processRecord(consentProcessDataTable, requestDict):
    baseTable = consentProcessDataTable.TABLE
    baseTableAttr = baseTable.ATTRIBUTE

    # ----- INSERT the record -----
    insertRecordDict = {}
    requestId = localId = status = None
    # Tag Start DateTime
    startDateTime = helper.getUtcDateTime()
    # Set Primary and Sort Key
    addPrimaryAndSortKey(requestDict, insertRecordDict, baseTable, baseTableAttr)
    # Set Original Json
    insertRecordDict[baseTableAttr.ORIGINAL_DATA] = requestDict
    # Transform and set new Json
    transformResult = transformIncomingJson(requestDict)
    if(API.isResultSuccess(transformResult)):
        insertRecordDict[baseTableAttr.TRANSFORMED_DATA] = API.getResultData(transformResult)
    else:
        pass
    # TODO
    # requestId = localId = None
    # status = None
    # Set Trace and Stats dictionary
    insertRecordDict[baseTableAttr.TRACE] = helper.getTraceDict(requestId, localId, status, startDateTime, helper.getUtcDateTime())
    # Insert into ConsentProcessStream
    print("processRecord() - insert dictionary: ", insertRecordDict)
    result = consentProcessDataTable.insert(insertRecordDict)
    print("  Processing Outcome (insert): ", result)
    if(API.isResultFailure(result)):
        # TODO
        pass

    # ----- UPDATE the record -----
    updateRecordDict = {}
    addPrimaryAndSortKey(requestDict, updateRecordDict, baseTable, baseTableAttr)
    # Update the End DateTime
    updateRecordDict[baseTableAttr.STATS] = helper.getTraceDict(startDateTime=startDateTime, endDateTime=helper.getUtcDateTime())
    # Update ConsentProcessStream
    print("processRecord() - update dictionary: ", insertRecordDict)
    # TODO
    # updateResult = consentProcessDataTable.update(updateDict)
    # print("  Processing Outcome (update): ", updateResult)
    # if(API.isResultFailure(updateResult)):
    #    # TODO
    #     pass

    # ----- RETURN the result -----
    # TODO Evaluate whether following statement is correct or not
    return result if result != None else consentProcessDataTable.composeResult(API.STATUS_CODE.FAILED)


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    successCount = 0
    totalCount = 0
    consentProcessDataTable = CustomerConsentProcessDataTable()

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data'])
        # print("Decoded payload: ", payload)
        requestDict = json.loads(payload)
        # print("Consent Dictionary: ", requestDict)
        result = processRecord(consentProcessDataTable, requestDict)
        if(API.isResultSuccess(result)):
            successCount += 1
        totalCount += 1

    return f'Successfully processed {successCount} of {totalCount} records.'
