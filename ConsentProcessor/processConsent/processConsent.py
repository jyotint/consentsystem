# Standard library imports
import base64
import json
# import traceback
# Third party library imports
# Local application imports
from apiMgmt import API
import lambdaDynamoDBHelper 
from customerConsentDataTable import CustomerConsentDataTable
from customerConsentJsonStreamTable import CustomerConsentJsonStreamTable
import marketingProcessingLogic as mpl
# Module Constants


print('Loading function')


def processRecord(callContext):
    consentDataTable = callContext.get("consentDataTable")
    transformedDataDict = callContext.get("transformedDataDict")

    baseTable = consentDataTable.TABLE
    context = {
        "baseTable": baseTable,
        "tableName": baseTable.TABLE_NAME,
        "consentDateTimeKeyName": baseTable.ATTRIBUTE.CONSENT_DATETIME
    }

    # Extract CustomerConsentDataTable related attributes from the Dictionary
    consentDict = consentDataTable.extract(transformedDataDict)
    # print(f"processRecord() >> Extract Consent Dictionary: {consentDict}")

    # Compose and add SortKey, if does not exists
    if(consentDict.get(baseTable.ATTRIBUTE.SORT_KEY) == None):
        consentDict[baseTable.ATTRIBUTE.SORT_KEY] = consentDataTable.composeSortKey(consentDict)
    print(f"processRecord() >> Extract Consent Dictionary: {consentDict}")

    # Validate and Process Consent
    result = consentDataTable.validate(consentDict)
    print("processRecord() >> Validation Outcome: ", result)
    if(API.isResultSuccess(result)):
        result = mpl.processConsent(consentDataTable, consentDict, context)
    
    print("processRecord() >> Processing Outcome: ", result)
    return result


def recordHandler(context):
    returnValue = "failed"
    consentJsonStreamTable = context.get("consentJsonStreamTable")
    record = context.get("record")

    # try:
    eventName = lambdaDynamoDBHelper.getEventName(record)
    if(lambdaDynamoDBHelper.isRecordEventInserted(record)):
        print(f"PROCESSING DynamoDB '{eventName}' event further...")
        newDbRecord = lambdaDynamoDBHelper.getNewImage(record)
        if(newDbRecord == None):
            result = consentJsonStreamTable.composeResult(API.STATUS_CODE.FAILED, errorMessage="DynamoDB Event missing 'NewImage'!")
        else:
            # transformedData = newDbRecord.get(consentJsonStreamTable.TABLE.ATTRIBUTE.TRANSFORMED_DATA)
            transformedData = lambdaDynamoDBHelper.getDictionaryByKey(newDbRecord, consentJsonStreamTable.TABLE.ATTRIBUTE.TRANSFORMED_DATA)
            if(transformedData == None):
                result = consentJsonStreamTable.composeResult(API.STATUS_CODE.FAILED, errorMessage=f"Record is missing '{consentJsonStreamTable.TABLE.ATTRIBUTE.TRANSFORMED_DATA}'!")
            else:
                transformedDataDict = CustomerConsentJsonStreamTable.deserializeRecordToDict(transformedData)
                # print("recordHandler() >> Consent Dictionary: ", transformedDataDict)
                context["transformedDataDict"] = transformedDataDict
                result = processRecord(context)

        if(API.isResultSuccess(result)):
            returnValue = "success"
        else:
            print(API.getErrorPrintMessage(result))
            returnValue = "failed"
    else:
        print(f"IGNORING DynamoDB '{eventName}' event.")
        returnValue = "skipped"

    # except Exception as err:
    #     print(f"Exception occurred while processing. Type: {type(err)}, str: '{err}'")
    #     # traceback.print_exc()
    #     returnValue = "failed"

    return returnValue


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    successCount = failedCount = skippedCount = totalCount = 0

    consentDataTable = CustomerConsentDataTable()
    consentJsonStreamTable = CustomerConsentJsonStreamTable()
    context = {
        "consentDataTable": consentDataTable,
        "consentJsonStreamTable": consentJsonStreamTable
    }

    for record in lambdaDynamoDBHelper.getEventRecords(event):
        print("lambda_handler() >> record: ", record)
        # print("lambda_handler() >> DynamoDB >> eventID: ", record['eventID'], ", eventName: ", record['eventName'])
        # print("lambda_handler() >> DynamoDB >> Record: " + json.dumps(record['dynamodb'], indent=2))

        context["record"] = record
        result = recordHandler(context)
        if(result == "skipped"):
            skippedCount += 1
        elif(result == "success"):
            successCount += 1
        elif(result == "failed"):
            failedCount += 1
        else:
            failedCount += 1
        totalCount += 1

    return f'Successfully processed {successCount} of {totalCount} records (Skipped Count: {skippedCount}, Failed Count: {failedCount})'
