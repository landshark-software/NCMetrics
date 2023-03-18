from boto3.dynamodb.conditions import Key


class NCMetricsDao:
    NC_METRICS_TABLE_NAME = "NCMetricsStore"

    def __init__(self, ddbServiceResource):
        self.ncMetricsTable = ddbServiceResource.Table(NCMetricsDao.NC_METRICS_TABLE_NAME)

    def putOnlinePlayerCount(self, playerCountDataPoint):
        self.ncMetricsTable.put_item(Item=playerCountDataPoint)

    def getOnlinePlayerCount(self, metricName, startTime, endTime):
        result = self.ncMetricsTable.query(KeyConditionExpression=Key(metricName).between(startTime, endTime))

        return {
            "dataPoints": result["Items"],
            "cost": result["ConsumedCapacity"]["ReadCapacityUnits"],
            "lastEvaluatedKey": result["LastEvaluatedKey"]["string"]
        }
