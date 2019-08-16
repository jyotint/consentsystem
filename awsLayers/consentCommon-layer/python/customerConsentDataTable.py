# Standard library imports
# Third party library imports
# Local application imports
from apiMgmt import API
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

        sourceMarket = consentDict.get(tableAttr.SOURCE_MARKET)
        country = consentDict.get(tableAttr.COUNTRY)
        contactType = consentDict.get(tableAttr.CONTACT_TYPE)
        contactTypeKey = consentDict.get(self.contactTypeKeys.get(contactType))
        sortKey = f"{sourceMarket}{separator}{country}{separator}{contactType}{separator}{contactTypeKey}"    
        
        # print(f"{self.__class__.__name__}::composeSortKey() >> CustomerMK: '{consentDict[self.tablePrimaryKeyName]}', SortKey: '{sortKey}'")
        return sortKey


    def __extract_addAttrIfPresent(self, dataDict, consentDict, attr):
        if(dataDict.get(attr) != None):
            consentDict[attr] = dataDict.get(attr)

    def extract(self, dataDict):
        tableAttr = CustomerConsentDataTable.TABLE.ATTRIBUTE
        consentDict = {}

        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.CUSTOMER_MK)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.SORT_KEY)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.SOURCE_MARKET)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.COUNTRY)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.CONTACT_TYPE)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.EMAIL)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.PHONE_NUMBER)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.POSTAL)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.CONSENT_STATUS)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.CONSENT_DATETIME)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.SOURCE_SYSTEM_CODE)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.LINE_TYPE)
        self.__extract_addAttrIfPresent(dataDict, consentDict, tableAttr.CONTACT_POINT_CATEGORY)

        return consentDict

        
    def __validate_checkAndAddToMissingAttrList(self, consentDict, missingAttrList, attr):
        if(consentDict.get(attr) == None):
            missingAttrList.append(attr)

    def validate(self, consentDict):
        """
        Validates Consent dictionary for mandatory attributes
            Method does "not" support Postal Consent attribute check yet
        """
        if(consentDict == None):
            return self.composeResult(API.STATUS_CODE.FAILED, errorMessage="Invalid consent dictionary object (null) passed!")

        missingAttrList = []
        tableAttr = CustomerConsentDataTable.TABLE.ATTRIBUTE
        self.__validate_checkAndAddToMissingAttrList(consentDict, missingAttrList, tableAttr.CUSTOMER_MK)
        self.__validate_checkAndAddToMissingAttrList(consentDict, missingAttrList, tableAttr.SOURCE_MARKET)
        self.__validate_checkAndAddToMissingAttrList(consentDict, missingAttrList, tableAttr.COUNTRY)
        self.__validate_checkAndAddToMissingAttrList(consentDict, missingAttrList, tableAttr.CONTACT_TYPE)
        self.__validate_checkAndAddToMissingAttrList(consentDict, missingAttrList, tableAttr.CONSENT_STATUS)
        self.__validate_checkAndAddToMissingAttrList(consentDict, missingAttrList, tableAttr.CONSENT_DATETIME)

        contactType = consentDict.get(tableAttr.CONTACT_TYPE)
        contactTypeKey = self.contactTypeKeys.get(contactType)
        self.__validate_checkAndAddToMissingAttrList(consentDict, missingAttrList, contactTypeKey)

        if(len(missingAttrList) > 0):
            errorMessage = f"Consent is missing mandatory attribute(s): {missingAttrList}!"
            return self.composeResult(API.STATUS_CODE.FAILED, errorMessage=errorMessage)

        return self.composeResult(API.STATUS_CODE.SUCCESS, data=consentDict)


    def find(self, queryParamDict = None, customerMK = None, sortKey = None):
        # print(f"CustomerConsentDataTable::find() >> PrimaryKeyName: '{self.tablePrimaryKeyName}', SortKeyName: '{self.tableSortKeyName}'")
        if(queryParamDict != None):
            customerMK = queryParamDict.get(self.tablePrimaryKeyName)
            sortKey = queryParamDict.get(self.tableSortKeyName)

        # print(f"CustomerConsentDataTable::find() >> PrimaryKey Value: '{customerMK}', SortKey Value: '{sortKey}'")
        return super().find(customerMK, sortKey)
