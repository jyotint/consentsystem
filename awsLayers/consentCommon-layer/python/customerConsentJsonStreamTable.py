# Standard library imports
# Third party library imports
# Local application imports
import helper
from consentConstants import *
from dynamoDbTableOps import DynamoDbTableOps
# Module constants and variables


class CustomerConsentJsonStreamTable(DynamoDbTableOps):
    TABLE = CONSENT_DB.CONSENT_JSON_STREAM

    def __init__(self):
        table = CustomerConsentJsonStreamTable.TABLE
        super().__init__(table.TABLE_NAME, table.ATTRIBUTE.CUSTOMER_MK, table.ATTRIBUTE.SORT_KEY)


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
        # print(f"CustomerConsentJsonStreamTable::find() >> PrimaryKeyName: '{self.tablePrimaryKeyName}', SortKeyName: '{self.tableSortKeyName}'")
        if(queryParamDict != None):
            customerMK = queryParamDict.get(self.tablePrimaryKeyName)
            sortKey = queryParamDict.get(self.tableSortKeyName)

        # print(f"CustomerConsentJsonStreamTable::find() >> PrimaryKey Value: '{customerMK}', SortKey Value: '{sortKey}'")
        return super().find(customerMK, sortKey)