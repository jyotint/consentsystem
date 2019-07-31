# Standard library imports
import json
# Third party library imports
# Local application imports
from apiMgmt import API
from apiMgmtHttp import HttpAPI
from customerConsentDataTable import CustomerConsentDataTable


# Module constants and variables
SUPPORTED_HTTP_METHOD = 'GET'


print('Loading function')
def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    # Get HTTP Method for the request and validate it
    operation = event['httpMethod']
    if operation != SUPPORTED_HTTP_METHOD:
        return HttpAPI.prepareHttpResponse(HttpAPI.HTTP_STATUS.METHOD_NOT_ALLOWED, error=Exception(f"Unsupported method '{operation}'"))

    # Get Payload dictionary based on HTTP Method type
    payload = event['queryStringParameters'] if operation == SUPPORTED_HTTP_METHOD else event['body']
    if type(payload) != type({}):
        msg = f"Invalid payload type '{type(payload)}' for method '{operation}'. Expected payload type {type({})}"
        return HttpAPI.prepareHttpResponse(HttpAPI.HTTP_STATUS.BAD_REQUEST, error=Exception(msg))


    # Get variables from Payload
    customerMK = payload.get("CustomerMK")
    sortKey = payload.get("SortKey")
    queryParamDict = None

    consentDataTable = CustomerConsentDataTable()
    result = consentDataTable.query(customerMK, sortKey, queryParamDict)
    # print("consentDataTable.query(): ", result)
    if(API.isResultFailure(result)):
        return HttpAPI.prepareHttpResponse(HttpAPI.HTTP_STATUS.NOT_FOUND, error=Exception("Not found"))
    else:
        dataResponse = API.getResultData(result)
        return HttpAPI.prepareHttpResponse(HttpAPI.HTTP_STATUS.OK, data=dataResponse)
