# Standard library imports
# Third party library imports
# Local application imports


class CONSENT_DB:
    class CONSENT_DATA:
        TABLE_NAME = "CustomerConsent.Data"
        class ATTRIBUTE:
            CUSTOMER_MK = "CustomerMK"
            SORT_KEY = "SortKey"
            SOURCE_MARKET = "SourceMarket"
            COUNTRY = "Country"
            CONTACT_TYPE = "ContactType"
            EMAIL = "Email"
            PHONE_NUMBER = "PhoneNumber"
            POSTAL = ""
            CONSENT_STATUS = "ConsentStatus"
            CONSENT_DATETIME = "ConsentDateTime"
        CONTACT_TYPE_LIST = ["Email", "Call", "SMS", "Postal"]

    class CONSENT_JSON_STREAM:
        TABLE_NAME = "CustomerConsent.ConsentJsonStream"
        class ATTRIBUTE:
            CUSTOMER_MK = "CustomerMK"
            SORT_KEY = "SortKey"
            ORIGINAL_DATA = "originalData"
            TRANSFORMED_DATA = "transformedData"
            TRACE = "trace"
        class INCOMING_DATA:
            CUSTOMER_MK = "CustomerMK"
