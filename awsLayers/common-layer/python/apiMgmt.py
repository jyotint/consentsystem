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
        API.STATUS_CODE.FAILED
    ]

    class MESSAGE:
        DEFAULT_ERROR_MESSAGE = "Unknown error has occured!"


    def isResultSuccess(result):
        return result.get(API.RESULT.STATUS) == API.STATUS_CODE.SUCCESS

    def isResultFailure(result):
        return result.get(API.RESULT.STATUS) in API.FAILURE_STATUS_CODE_LIST

    def getResultData(result):
        return result.get(API.RESULT.DATA)

    def getResultError(result):
        return result.get(API.RESULT.ERROR)

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
        if(error != None):
            result[API.RESULT.ERROR] = error
        else:
            result[API.RESULT.ERROR] = API.composeError(errorMessage=errorMessage, errorCode=errorCode)
        return result
