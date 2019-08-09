# Standard library imports
# Third party library imports
# Local application imports


class API:
    class RESULT:
        STATUS = "status"
        DATA = "data"
        ERROR = "error"
        ERROR_CODE = "code"
        ERROR_MESSAGE = "message"

    class STATUS_CODE:
        SUCCESS = 0
        FAILED = -1

    FAILURE_STATUS_CODE_LIST = [
        STATUS_CODE.FAILED
    ]

    class MESSAGE:
        DEFAULT_ERROR_MESSAGE = "Unknown error has occured!"


    def getResultStatus(result):
        return result.get(API.RESULT.STATUS)

    def isResultSuccess(result):
        return API.getResultStatus(result) == API.STATUS_CODE.SUCCESS if result != None else False

    def isStatusFailure(status):
        return (status in API.FAILURE_STATUS_CODE_LIST) if status != None else False

    def isResultFailure(result):
        return API.isStatusFailure(API.getResultStatus(result))

    def getResultData(result):
        return result.get(API.RESULT.DATA) if result != None else None

    def getResultError(result):
        return result.get(API.RESULT.ERROR) if result != None else None

    def getErrorPrintMessage(result):
        status = API.getResultStatus(result)
        error = result.get(API.RESULT.ERROR)
        errorCode = error.get(API.RESULT.ERROR_CODE)
        errorMessage = error.get(API.RESULT.ERROR_MESSAGE)
        msg = f"Status: '{status}'"
        if(error != None):
            if(errorCode != None):
                msg = f"{msg}, Error Code: {errorCode}"
            if(errorMessage != None):
                msg = f"{msg}, Error Message: '{errorMessage}''"

        return msg


    def composeError(errorMessage=None, errorCode=None):
        result = {}
        if(errorCode != None):
            result[API.RESULT.ERROR_CODE] = errorCode
        result[API.RESULT.ERROR_MESSAGE] = errorMessage if errorMessage != None else API.MESSAGE.DEFAULT_ERROR_MESSAGE
        return result

    def composeResult(status, data=None, error=None, errorMessage=None, errorCode=None):
        result = {}
        result[API.RESULT.STATUS] = status
        if(data != None):
            result[API.RESULT.DATA] = data
        if(API.isStatusFailure(status)):
            if(error != None):
                result[API.RESULT.ERROR] = error
            else:
                result[API.RESULT.ERROR] = API.composeError(errorMessage=errorMessage, errorCode=errorCode)
        return result
