# Standard library imports
import json
# Third party library imports
# Local application imports
import helper
import timeHelper
import lambdaKinesisHelper
from constants import *
from apiMgmt import API
from customerConsentJsonStreamTable import CustomerConsentJsonStreamTable
import transformConsentJson
# Module Constants


print('Loading function')


def addPrimaryAndSortKey(dataDict, baseTableAttr, customerMK, sortKey):
    # Set Primary and Sort Key
    dataDict[baseTableAttr.CUSTOMER_MK] = customerMK
    dataDict[baseTableAttr.SORT_KEY] = sortKey


def processRecord(consentJsonStreamTable, requestDict, consentJson):
    requestId = localId = status = errorMessage = None

    baseTable = consentJsonStreamTable.TABLE
    baseTableAttr = baseTable.ATTRIBUTE
    print(f"CustomerMK: '{baseTable.INCOMING_DATA.CUSTOMER_MK}', requestDict: {requestDict}")
    customerMK = requestDict[baseTable.INCOMING_DATA.CUSTOMER_MK]
    sortKey = timeHelper.getUTCDateTimeString()

    # ----- INSERT the record -----
    insertRecordDict = {}
    requestId = localId = status = None
    # Tag Start DateTime
    startTime = timeHelper.getNow()
    # Set Primary and Sort Key
    addPrimaryAndSortKey(insertRecordDict, baseTableAttr, customerMK, sortKey)
    # Set Original Json
    insertRecordDict[baseTableAttr.ORIGINAL_DATA] = requestDict
    valiationResult = transformConsentJson.validate(requestDict, consentJson)
    if(API.isResultFailure(valiationResult)):
        status = API.getResultStatus(valiationResult)
        errorMessage = API.getErrorPrintMessage(valiationResult)
    else:
        # Transform and set new Json
        transformResult = transformConsentJson.transform(requestDict, consentJson)
        if(API.isResultFailure(transformResult)):
            status = API.getResultStatus(transformResult)
            errorMessage = API.getErrorPrintMessage(transformResult)
        else:
            insertRecordDict[baseTableAttr.TRANSFORMED_DATA] = API.getResultData(transformResult)

    # Set Trace and Stats dictionary
    timeLogTuple = timeHelper.getTimeLogTupleString(startTime)
    # print(f"processRecord() >> timeLogTuple (insert): '{timeLogTuple[0]}', '{timeLogTuple[1]}', '{timeLogTuple[2]}'")
    insertRecordDict[baseTableAttr.TRACE] = helper.getTraceDict(originId=requestId, localId=localId, status=status, message=errorMessage, startDateTime=timeLogTuple[0], endDateTime=timeLogTuple[1], duration=timeLogTuple[2])
    # Insert into the table
    # print("processRecord() >> insert dictionary: ", insertRecordDict)
    insertResult = consentJsonStreamTable.insert(insertRecordDict)
    # print("  processRecord() >> Processing Outcome (insert): ", insertResult)
    if(API.isResultFailure(insertResult)):
        # TODO What do we do in this scenario?
        return insertResult if insertResult != None else consentJsonStreamTable.composeResult(API.STATUS_CODE.FAILED)
    else:
        # ----- UPDATE the record trace (overall processing time until insert DB operation was successful) -----
        status = API.getResultStatus(insertResult)

        updateRecordDict = {}
        addPrimaryAndSortKey(updateRecordDict, baseTableAttr, customerMK, sortKey)
        # Update the End DateTime
        timeLogTuple = timeHelper.getTimeLogTupleString(startTime)
        # print(f"processRecord() >> timeLogTuple (update): '{timeLogTuple[0]}', '{timeLogTuple[1]}', '{timeLogTuple[2]}'")
        updateRecordDict[baseTableAttr.TRACE] = helper.getTraceDict(originId=requestId, localId=localId, status=status, message=errorMessage, startDateTime=timeLogTuple[0], endDateTime=timeLogTuple[1], duration=timeLogTuple[2])
        # Update ConsentProcessStream
        # print("processRecord() >> update dictionary: ", insertRecordDict)
        updateResult = consentJsonStreamTable.update(updateRecordDict)
        # print("  processRecord() >> Processing Outcome (update): ", updateResult)
        # Ignore the update error as insert operation (the key operation) is successful 
        # if(API.isResultFailure(updateResult)):
        #     return updateResult if updateResult != None else consentJsonStreamTable.composeResult(API.STATUS_CODE.FAILED)

    # ----- RETURN the insertResult -----
    return insertResult if insertResult != None else consentJsonStreamTable.composeResult(API.STATUS_CODE.FAILED)


def recordHandler(consentJsonStreamTable, record):
    returnValue = False
    
    # try:
    # Kinesis data is base64 encoded so decode here
    payload1 = lambdaKinesisHelper.getDecodedPayloadData(record)
    print(f"recordHandler() >> Decoded payload - type: {type(payload1)}, data: {payload1}")
    payload2 = payload1.decode("utf-8")
    print(f"recordHandler() >> Decoded payload2 - type: {type(payload2)}, data: {payload2}")
    payload3 = json.loads(payload2)
    print(f"recordHandler() >> Decoded payload3 - type: {type(payload3)}, data: {payload3}")
    # requestDict = helper.convertDataToObject(payload3)
    requestDict = json.loads(payload3)
    print(f"recordHandler() >> Consent Dictionary - Type: {type(requestDict)}, Data: {requestDict}")

    result = processRecord(consentJsonStreamTable, requestDict, payload3)
    if(API.isResultSuccess(result)):
        returnValue = True
    else:
        # TODO Push this record into "Poison" Queue for manual intervention
        pass
    returnValue = False

    # except Exception as err:
    #     print(f"Exception occurred while processing. Type: {type(err)}, str: '{err}'")
    #     returnValue = False
    
    return returnValue


def lambda_handler(event, context):
    # print("lambda_handler() >> Received event: " + helper.convertObjectToJson(event, indent=2))
    print("context: ", context)
    successCount = totalCount = 0

    consentJsonStreamTable = CustomerConsentJsonStreamTable()
    for record in lambdaKinesisHelper.getEventRecords(event):
        result = recordHandler(consentJsonStreamTable, record)
        if(result == True):
            successCount += 1
        totalCount += 1

    # context.succeed()
    return f'Successfully processed {successCount} of {totalCount} records.'
