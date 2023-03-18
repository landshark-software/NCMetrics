import time
import math
from DataPointUtil import DataPointUtil

class NCMetricsHandler:
    ONE_DAY_IN_SECONDS = 24 * 60 * 60

    def __init__(self, dao):
        self.dao = dao

    def handle(self, request):
        datapoints = []
        days = (request["endTime"] - request["startTime"])/NCMetricsHandler.ONE_DAY_IN_SECONDS

        if math.floor(days) < days:
            days = math.floor(days) + 1
        else:
            days = math.floor(days)

        for day in range(days):
            t = time.gmtime(request["startTime"] + day * NCMetricsHandler.ONE_DAY_IN_SECONDS)
            combinedName = DataPointUtil.buildMetricCombinedName(request["metricName"], t)
            result = self.getDataPoints(combinedName, request["startTime"], request["endTime"])
            datapoints += result["dataPoints"]
        return datapoints

    def getDataPoints(self, combinedName, startTime, endTime):
        return self.dao.getOnlinePlayerCount(combinedName, startTime, endTime)
