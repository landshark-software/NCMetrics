import random


class NCMetricsDaoMock:
    NC_METRICS_TABLE_NAME = "NCMetrics"

    def __init__(self):
        self.timeCount = 1676602011

    def putOnlinePlayerCount(self, playerCountDataPoint):
        print("putOnlinePlayerCount called with: ", playerCountDataPoint)

    def getOnlinePlayerCount(self, metricName, startTime, endTime, lek):
        print("getOnlinePlayerCount called with: ", metricName, startTime, endTime, lek)
        datapoints = []

        for i in range(random.randint(1, 10)):
            datapoints.append({
                "metricCombinedName": "TEST_METRIC-01/01/2023",
                "time": self.timeCount,
                "playerCount": random.randint(0, 30),
                "timeToLive": self.timeCount + 2592000
            })
            self.timeCount += 5*60

        return {
            "dataPoints": datapoints,
            "cost": 5,
            "lastEvaluatedKey": None if "metricCombinedName" in lek else {"metricCombinedName": "TEST_METRIC-01/01/2023", "time": 12345}
        }


