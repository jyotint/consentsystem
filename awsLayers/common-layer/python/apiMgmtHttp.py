# Standard library imports
import json
from http import HTTPStatus
# Local application imports
from constants import *
# Module constants and variables


class HttpAPI:
    HTTP_STATUS = HTTPStatus

    # List of successful http statuses where 'response' is expected
    httpSuccessStatuses = {
        HTTP_STATUS.OK: True,
        HTTP_STATUS.CREATED: True
    }


    class RESPONSE:
        HEADERS_TAG = "headers"
        MESSAGE_TAG = "message"
        BODY_TAG = "body"
        STATUSCODE_TAG = "statusCode"

    class DEFAULT:
        class RESPONSE:
            HEADERS = {
                "Content-Type": "application/json"
            }


    def prepareErrorDict(httpStatus, error):
        """
        Compose error dictionary
        """
        result = {}
        if(httpStatus != None):
            result[HttpAPI.RESPONSE.STATUSCODE_TAG] = httpStatus
        if(error != None):
            result[HttpAPI.RESPONSE.MESSAGE_TAG] = str(error)
        return result


    def prepareHttpResponse(httpStatus, error=None, data=None, headers=None):
        """
        Prepare HTTP Response
        """

        # Use 'response' if httpStatus is in successful status codes, otherwise use 'error'
        httpBody = {}
        if httpStatus in HttpAPI.httpSuccessStatuses:
            httpBody = json.dumps(data) if data != None else json.dumps({})
        else:
            httpBody = json.dumps(prepareErrorDict(httpStatus, error))

        # If headers are supplied use it, otherwise use default headers
        httpHeaders = headers if headers != None else HttpAPI.DEFAULT.RESPONSE.HEADERS

        return {
            HttpAPI.RESPONSE.STATUSCODE_TAG: httpStatus,
            HttpAPI.RESPONSE.HEADERS_TAG: httpHeaders,
            HttpAPI.RESPONSE.BODY_TAG: httpBody
        }
