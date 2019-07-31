# Standard library imports
import base64
import json
# Third party library imports
# Local application imports
from apiMgmt import API
from customerConsentDataTable import CustomerConsentDataTable
import marketingProcessingLogic as mpl
# Module Constants


print('Loading function')


def processRecord(consentDataTable, streamDict):
    baseTable = consentDataTable.TABLE
    context = {
        baseTable: baseTable,
        tableName: baseTable.TABLE_NAME,
        consentDateTimeKeyName: baseTable.ATTRIBUTE.CONSENT_DATETIME
    }

    # Compose and add SortKey
    if(streamDict.get(context.baseTable.ATTRIBUTE.SORT_KEY) == None):
        streamDict[context.baseTable.ATTRIBUTE.SORT_KEY] = consentDataTable.composeSortKey(streamDict)

    result = mpl.processConsent(consentDataTable, streamDict, context)
    # print("  Processing Outcome: ", result)

    return result


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    successCount = 0
    totalCount = 0
    consentDataTable = CustomerConsentDataTable()

    for record in event['Records']:
        print(record)
        print("DynamoDB >> eventID: ", record['eventID'], ", eventName: ", record['eventName'])
        print("DynamoDB >> Record: " + json.dumps(record['dynamodb'], indent=2))

        # print("Consent Dictionary: ", streamDict)
        result = processRecord(consentDataTable, streamDict)
        if(API.isResultSuccess(result)):
            successCount += 1
        totalCount += 1

    return f'Successfully processed {successCount} of {totalCount} records.'
