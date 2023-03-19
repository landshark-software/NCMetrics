from boto3.dynamodb.conditions import Key


class NCMetricsDao:
    NC_METRICS_TABLE_NAME = "NCMetricsStore"

    def __init__(self, ddbServiceResource):
        self.ncMetricsTable = ddbServiceResource.Table(NCMetricsDao.NC_METRICS_TABLE_NAME)

    def putOnlinePlayerCount(self, playerCountDataPoint):
        self.ncMetricsTable.put_item(Item=playerCountDataPoint)

    def getOnlinePlayerCount(self, metricName, startTime, endTime, lek):
        print("------")
        print("calling getOnlinePlayerCount in dao", metricName, startTime, endTime)
        result = self.ncMetricsTable.query(KeyConditionExpression=Key("metricCombinedName").eq(metricName) & Key("time").between(startTime, endTime),
                                           ReturnConsumedCapacity="TOTAL",
                                           ExclusiveStartKey=lek)
        
        print(result)
        print("------")
        cost = 0
        lastEvaluatedKey = None
        
        if "ConsumedCapacity" in result and "CapacityUnits" in result["ConsumedCapacity"]:
            cost = result["ConsumedCapacity"]["CapacityUnits"]
        if "LastEvaluatedKey" in result and "string" in result["LastEvaluatedKey"]:
            lastEvaluatedKey = result["LastEvaluatedKey"]["string"]
        
        return {
            "dataPoints": result["Items"],
            "cost": cost,
            "lastEvaluatedKey": lastEvaluatedKey
        }
