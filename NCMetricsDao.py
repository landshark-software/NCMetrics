from boto3.dynamodb.conditions import Key


class NCMetricsDao:
    NC_METRICS_TABLE_NAME = "NCMetricsStore"

    def __init__(self, ddbServiceResource):
        self.ncMetricsTable = ddbServiceResource.Table(NCMetricsDao.NC_METRICS_TABLE_NAME)

    def putOnlinePlayerCount(self, playerCountDataPoint):
        self.ncMetricsTable.put_item(Item=playerCountDataPoint)

    def getOnlinePlayerCount(self, metricName, startTime, endTime):
        result = self.ncMetricsTable.query(KeyConditionExpression=Key("metricCombinedName").eq(metricName) & Key("time").between(startTime, endTime),
                                           ReturnConsumedCapacity="TOTAL")
        cost = 0
        lastEvaluatedKey = None
        
        if result["ConsumedCapacity"] != None and result["ConsumedCapacity"]["CapacityUnits"] != None:
            cost = result["ConsumedCapacity"]["CapacityUnits"]
        if result["LastEvaluatedKey"] != None and result["LastEvaluatedKey"]["string"] != None:
            lastEvaluatedKey = result["LastEvaluatedKey"]["string"]
        
        return {
            "dataPoints": result["Items"],
            "cost": cost,
            "lastEvaluatedKey": lastEvaluatedKey
        }
