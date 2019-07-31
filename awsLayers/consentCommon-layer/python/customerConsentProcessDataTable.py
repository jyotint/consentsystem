# Standard library imports
# Third party library imports
# Local application imports
import helper
from consentConstants import *
from dynamoDbTableOps import DynamoDbTableOps
# Module constants and variables


class CustomerConsentProcessDataTable(DynamoDbTableOps):
    TABLE = CONSENT_DB.CONSENT_PROCESS_STREAM

    def __init__(self):
        super().__init__(TABLE.TABLE_NAME, TABLE.ATTRIBUTE.CUSTOMER_MK, TABLE.ATTRIBUTE.SORT_KEY)


    def __del__(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return f"{self.__class__.__name__} >> {super().__str__()}"


    def composeSortKey(self, dataDict):
        sortKey = helper.getCurrentUtcDateTime()

        print(f"{self.__class__.__name__}::composeSortKey() >> CustomerMK: '{dataDict[self.tablePrimaryKeyName]}', SortKey: '{sortKey}'")
        return sortKey


    def find(self, queryParamDict = None, customerMK = None, sortKey = None):
        if(queryParamDict == None):
            return self.find(customerMK, sortKey)
        else:
            return self.find(queryParamDict[self.tablePrimaryKeyName], queryParamDict[self.tableSortKeyName])
