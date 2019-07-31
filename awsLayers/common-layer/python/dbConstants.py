# Standard library imports
# Third party library imports
# Local application imports
# Module constants and variables


class DB:
    DB_RESOURCE_NAME = 'dynamodb'

    class API:
        class QUERY:
            KEY_CONDITION_EXPRESSION = "KeyConditionExpression"
        class RESPONSE:
            ITEM = "Item"
            ITEMS = "Items"
        class RETURN_VALUES:
            UPDATED_NEW = "UPDATED_NEW"

    class COMMON:
        SORT_KEY_SEPARATOR = "^"
        class ATTRIBUTE:
            CREATED_ON = "CreatedOn"
            UPDATED_ON = "UpdatedOn"
