# Standard library imports
# Third party library imports
# Local application imports
from apiMgmt import API
from customerConsentDataTable import CustomerConsentDataTable
# Module Constants


print('Loading function')


def validate(consentDict, consentJson):
    consentDataTable = CustomerConsentDataTable()
    return consentDataTable.validate(consentDict)
    # return API.composeResult(API.STATUS_CODE.SUCCESS)


def transform(consentDict, consentJson):
    # transformedDict = {}

    # Perform the transformation
    #   As of now, not required as Original JSON conforms to the requirement of Transformed JSON
    result = API.composeResult(API.STATUS_CODE.SUCCESS, data=consentDict)
    return result
