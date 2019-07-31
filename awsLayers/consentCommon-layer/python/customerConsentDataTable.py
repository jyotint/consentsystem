# Standard library imports
# Third party library imports
# Local application imports
from consentConstants import *
from dynamoDbTableOps import DynamoDbTableOps
# Module constants and variables


class CustomerConsentDataTable(DynamoDbTableOps):
    TABLE = CONSENT_DB.CONSENT_DATA

    def __init__(self):
        table = CustomerConsentDataTable.TABLE
        tableAttr = CustomerConsentDataTable.TABLE.ATTRIBUTE
        
        super().__init__(table.TABLE_NAME, tableAttr.CUSTOMER_MK, tableAttr.SORT_KEY)

        self.contactTypeKeys = {}
        self.contactTypeKeys[table.CONTACT_TYPE_LIST[0]] = tableAttr.EMAIL
        self.contactTypeKeys[table.CONTACT_TYPE_LIST[1]] = tableAttr.PHONE_NUMBER
        self.contactTypeKeys[table.CONTACT_TYPE_LIST[2]] = tableAttr.PHONE_NUMBER
        self.contactTypeKeys[table.CONTACT_TYPE_LIST[3]] = tableAttr.POSTAL


    def __del__(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self):
        return f"{self.__class__.__name__} >> {super().__str__()}"


    def composeSortKey(self, consentDict):
        tableAttr = CustomerConsentDataTable.TABLE.ATTRIBUTE
        separator = self.SORT_KEY_SEPARATOR

        sourceMarket = consentDict[tableAttr.SOURCE_MARKET]
        country = consentDict[tableAttr.COUNTRY]
        contactType = consentDict[tableAttr.CONTACT_TYPE]
        contactTypeKey = consentDict[self.contactTypeKeys[contactType]]
        sortKey = f"{sourceMarket}{separator}{country}{separator}{contactType}{separator}{contactTypeKey}"    
        
        print(f"{self.__class__.__name__}::composeSortKey() >> CustomerMK: '{consentDict[self.tablePrimaryKeyName]}', SortKey: '{sortKey}'")
        return sortKey


    def find(self, queryParamDict = None, customerMK = None, sortKey = None):
        if(queryParamDict == None):
            return self.find(customerMK, sortKey)
        else:
            return self.find(queryParamDict[self.tablePrimaryKeyName], queryParamDict[self.tableSortKeyName])
