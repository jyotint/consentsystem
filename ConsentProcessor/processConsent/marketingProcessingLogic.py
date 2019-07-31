# Standard library imports
# Third party library imports
# Local application imports
import helper
from apiMgmt import API
# Module Constants


def validateConsent(streamDict):
    result = True
    # for requiredAttr in valiation["required"]:
    #     streamDict.get(requiredAttr)
    return result


def processConsent(consentDataTable, incomingConsentDict, context):
    # Check whether Consent exists (find consent in database)
    findResult = consentDataTable.find(queryParamDict=incomingConsentDict)

    # Simple Consent date logic
    if(API.isResultFailure(findResult)):
        print(f"{context.tableName}: Inserting new consent.")
        result = consentDataTable.insert(incomingConsentDict)
    else:
        existingConsent = API.getResultData(findResult)
        existingConsentDateTime = helper.convertStringToDateTime(existingConsent[context.consentDateTimeKeyName])
        incomingConsentDateTime = helper.convertStringToDateTime(incomingConsentDict[context.consentDateTimeKeyName])
        if incomingConsentDateTime > existingConsentDateTime:
            print(f"{context.tableName}: Updating existing consent.")
            result = consentDataTable.update(incomingConsentDict)
        else:
            print(f"{context.tableName}: Ignoring new consent as it is older than existing consent in the database.")
            result = consentDataTable.composeResult(API.STATUS_CODE.SUCCESS, existingConsent)

    print("  Processing Outcome: ", result)
    return result
 