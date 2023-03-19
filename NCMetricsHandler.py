import time
import math
from DataPointUtil import DataPointUtil

class NCMetricsHandler:
    ONE_DAY_IN_SECONDS = 24 * 60 * 60
    TEN_MINUTES_IN_SECONDS = 10*60

    def __init__(self, dao):
        self.dao = dao

    def handle(self, request):
        requestStartTime = request["startTime"]
        requestEndTime = request["endTime"]
        currentTime = int(time.time())

        # Don't try to get data older than the retention period
        if requestStartTime < currentTime - DataPointUtil.DATA_RETENTION_PERIOD:
            requestStartTime = currentTime - DataPointUtil.DATA_RETENTION_PERIOD

        # Only get data that is older than 10 minutes. In case DDB is still putting the newest data in
        if requestEndTime > currentTime - NCMetricsHandler.TEN_MINUTES_IN_SECONDS:
            requestEndTime = currentTime - NCMetricsHandler.TEN_MINUTES_IN_SECONDS

        resultStartTime = requestStartTime
        resultEndTime = NCMetricsHandler.roundTimeDown(time.gmtime(requestStartTime))

        datapoints = []
        totalCost = 0
        while resultEndTime < requestEndTime:
            combinedName = DataPointUtil.buildMetricCombinedName(request["metricName"], time.gmtime(resultEndTime))

            try:
                totalCost += self.getDataPoints(combinedName, requestStartTime, requestEndTime, datapoints)
            except Exception as e:
                print("Exception while getting data points")
                print(e)
                break
            resultEndTime += NCMetricsHandler.ONE_DAY_IN_SECONDS

        if resultEndTime > requestEndTime:
            resultEndTime = requestEndTime
        print("Total Cost of Request: ", totalCost)
        return {"data": datapoints, "resultStartTime": resultStartTime, "resultEndTime": resultEndTime}

    def getDataPoints(self, combinedName, startTime, endTime, buffer):
        cost = 0
        # should be a do while loop, but that does not exist in python :(
        result = self.dao.getOnlinePlayerCount(combinedName, startTime, endTime, {})
        buffer += result["dataPoints"]
        lastEvaluatedKey = result["lastEvaluatedKey"]
        cost += result["cost"]
        while lastEvaluatedKey is not None:
            result = self.dao.getOnlinePlayerCount(combinedName, startTime, endTime, lastEvaluatedKey)
            buffer += result["dataPoints"]
            lastEvaluatedKey = result["lastEvaluatedKey"]
            cost += result["cost"]
        return cost

    # round given time down to the nearest day in UTC
    @staticmethod
    def roundTimeDown(t):
        return time.mktime(time.strptime(time.strftime(DataPointUtil.DATE_FORMAT, t), DataPointUtil.DATE_FORMAT))
