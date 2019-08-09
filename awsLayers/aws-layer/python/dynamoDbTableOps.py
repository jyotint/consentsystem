# Standard library imports
# Third party library imports
import boto3
from boto3.dynamodb.conditions import Key
# Local application imports
import timeHelper
import dynamoDbHelper
from apiMgmt import API
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


class DynamoDbTableOps():
    def __init__(self, tableName, tablePrimaryKeyName, tableSortKeyName, tableCreateOnKeyName = None, tableUpdatedOnKeyName = None):
        self.SORT_KEY_SEPARATOR = DB.COMMON.SORT_KEY_SEPARATOR
        
        self.tableName = tableName
        self.tablePrimaryKeyName = tablePrimaryKeyName
        self.tableSortKeyName = tableSortKeyName
        
        self.tableCreateOnKeyName = tableCreateOnKeyName if tableCreateOnKeyName != None else DB.COMMON.ATTRIBUTE.CREATED_ON
        self.tableUpdatedOnKeyName = tableUpdatedOnKeyName if tableUpdatedOnKeyName != None else DB.COMMON.ATTRIBUTE.UPDATED_ON

        self.dynamoDb = boto3.resource(DB.DB_RESOURCE_NAME)
        self.dbTable = self.dynamoDb.Table(self.tableName)


    def __del__(self):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.tableName}', '{self.tablePrimaryKeyName}', '{self.tableSortKeyName}', '{self.tableCreateOnKeyName}', '{self.tableUpdatedOnKeyName}')"

    def __str__(self):
        return f"{self.__class__.__name__} >> tableName: '{self.tableName}', tablePrimaryKeyName: '{self.tablePrimaryKeyName}', tableSortKeyName: '{self.tableSortKeyName}', tableCreateOnKeyName: '{self.tableCreateOnKeyName}', tableUpdatedOnKeyName: '{self.tableUpdatedOnKeyName}'"

    def composeResult(self, status, data=None, error=None, errorMessage=None, errorCode=None):
        return API.composeResult(status, data, error, errorMessage, errorCode)


    def composeSortKey(self, dataDict):
        # Derived class must implement this method
        return None

    def extract(self, dataDict):
        # Derived class must implement this method
        return {}

    def validate(self, dataDict):
        # Derived class must implement this method
        return self.composeResult(API.STATUS_CODE.FAILED, errorMessage="Derived class must implement this method!")



    def deserializeRecordToDict(dynamoDbRecord):
        if(dynamoDbRecord == None):
            return None
        deserializer = boto3.dynamodb.types.TypeDeserializer()
        return {k: deserializer.deserialize(v)  for k, v in dynamoDbRecord.items()}

    def serializeDictToRecord(dataDict):
        if(dataDict == None):
            return None
        serializer = boto3.dynamodb.types.TypeSerializer()
        return {k: serializer.serialize(v)  for k, v in dataDict.items()}


    def find(self, primaryKey, sortKey):
        keys = {
            self.tablePrimaryKeyName: primaryKey,
            self.tableSortKeyName: sortKey
        }

        #print("keys: ", keys)
        response = self.dbTable.get_item(Key=keys, TableName=self.tableName)
        # print("response: ", response)

        dataItem = response.get(DB.API.RESPONSE.ITEM)
        if(dataItem == None):
            return self.composeResult(API.STATUS_CODE.FAILED, errorMessage="No item was received from the database!")
        else:
            return self.composeResult(API.STATUS_CODE.SUCCESS, data=dataItem)


    def query(self, primaryKey, sortKey=None, queryParamDict=None):
        kwargs = {}
        kwargs[DB.API.QUERY.KEY_CONDITION_EXPRESSION] = Key(self.tablePrimaryKeyName).eq(primaryKey)

        # Add SortKey if exists
            
        # Add Filters if exists

        response = self.dbTable.query(**kwargs)
        # print(response)
        dataItems = response[DB.API.RESPONSE.ITEMS]
        if(dataItems == None):
            return self.composeResult(API.STATUS_CODE.FAILED, errorMessage="No item(s) were received from the database!")
        else:
            return self.composeResult(API.STATUS_CODE.SUCCESS, data=dataItems)


    def insert(self, dataDict):
        currentUtcDateTime = timeHelper.getUTCDateTimeString()
        dataDict[self.tableCreateOnKeyName] = currentUtcDateTime
        dataDict[self.tableUpdatedOnKeyName] = currentUtcDateTime
        print("dynamoDbTableOps::insert() >> dataDict: ", dataDict)

        result = self.dbTable.put_item(Item=dataDict)
        if(result == None):
            return self.composeResult(API.STATUS_CODE.FAILED, errorMessage="No item was received from the database!")
        else:
            # print("dynamoDbTableOps::insert() >> returned result: ", result)
            if(dynamoDbHelper.isOperationSuccessful(result)):
                return self.composeResult(API.STATUS_CODE.SUCCESS, data=result)
            else:
                return self.composeResult(API.STATUS_CODE.FAILED, error=result)


    def update(self, dataDict):
        updateKeys = {}
        updateExpression = ""
        expressionAttributeValues = {}
        
        currentUtcDateTime = timeHelper.getUTCDateTimeString()
        dataDict[self.tableUpdatedOnKeyName] = currentUtcDateTime
        print("dynamoDbTableOps::update() >> request dataDict: ", dataDict)

        attributeCount = 1
        for key in dataDict.keys():
            if key == self.tablePrimaryKeyName or key == self.tableSortKeyName:
                updateKeys[key] = dataDict[key]
            else:
                if len(updateExpression) > 0:
                    updateExpression += ", "
                updateExpression += f"{key} = :{attributeCount}"
                expressionAttributeValues[f":{attributeCount}"] = dataDict[key]
                attributeCount += 1
        
        if updateExpression != None:
            updateExpression = f"set {updateExpression}"

        result = self.dbTable.update_item(
            Key = updateKeys,
            UpdateExpression = updateExpression,
            ExpressionAttributeValues = expressionAttributeValues,
            ReturnValues = DB.API.RETURN_VALUES.UPDATED_NEW
        )
        # print("dynamoDbTableOps::update() >> returned result: ", result)
        if(result == None):
            return self.composeResult(API.STATUS_CODE.FAILED, errorMessage="No item was received from the database!")
        else:
            if(dynamoDbHelper.isOperationSuccessful(result)):
                return self.composeResult(API.STATUS_CODE.SUCCESS, data=result)
            else:
                return self.composeResult(API.STATUS_CODE.FAILED, error=result)


    def upsert(self, dataDict):
        sortKey = self.composeSortKey(dataDict)
        findResult = self.find(dataDict[self.tablePrimaryKeyName], dataDict[self.tableSortKeyName])
        if(API.isResultSuccess(findResult)):
            return self.update(dataDict)
        else:
            return self.insert(dataDict)
