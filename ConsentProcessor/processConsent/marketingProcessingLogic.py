# Standard library imports
# Third party library imports
# Local application imports
import timeHelper
from apiMgmt import API
# Module Constants


def processConsent(consentDataTable, incomingConsentDict, context):
    tableName = context.get("tableName")
    consentDateTimeKeyName = context.get("consentDateTimeKeyName")
    
    # Check whether Consent exists (find consent in database)
    findResult = consentDataTable.find(queryParamDict=incomingConsentDict)

    # Simple Consent date logic
    if(API.isResultFailure(findResult)):
        print(f"INSERTING new consent in '{tableName}' table.")
        result = consentDataTable.insert(incomingConsentDict)
    else:
        existingConsent = API.getResultData(findResult)
        existingConsentDateTime = timeHelper.convertStringToDateTime(existingConsent[consentDateTimeKeyName])
        incomingConsentDateTime = timeHelper.convertStringToDateTime(incomingConsentDict[consentDateTimeKeyName])
        if incomingConsentDateTime > existingConsentDateTime:
            print(f"UPDATING existing consent in '{tableName}' table.")
            result = consentDataTable.update(incomingConsentDict)
        else:
            print(f"IGNORING new consent as it is older or same as an existing consent in the '{tableName}' table.")
            result = consentDataTable.composeResult(API.STATUS_CODE.SUCCESS, existingConsent)

    # print("marketingProcessingLogic::processConsent() >> Processing Outcome: ", result)
    return result
