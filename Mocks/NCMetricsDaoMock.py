class NCMetricsDaoMock:
    NC_METRICS_TABLE_NAME = "NCMetrics"

    def putOnlinePlayerCount(self, playerCountDataPoint):
        print("putOnlinePlayerCount called with: ", playerCountDataPoint)

    def getOnlinePlayerCount(self, metricName, startTime, endTime):
        print("getOnlinePlayerCount called with: ", metricName, startTime, endTime)
        return {
            "dataPoints": [{
                "metricCombinedName": "TEST_METRIC-01/01/2023",
                "time": 12345,
                "playerCount": 1,
                "timeToLive": 756
            }, {
                "metricCombinedName": "TEST_METRIC-01/01/2023",
                "time": 12345,
                "playerCount": 2,
                "timeToLive": 756
            }, {
                "metricCombinedName": "TEST_METRIC-01/01/2023",
                "time": 12345,
                "playerCount": 3,
                "timeToLive": 756
            }],
            "cost": 5,
            "lastEvaluatedKey": {"metricCombinedName": "TEST_METRIC-01/01/2023", "time": 12345}
        }
