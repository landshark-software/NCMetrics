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
        resultEndTime = requestStartTime

        datapoints = []
        days = (requestEndTime - requestStartTime)/NCMetricsHandler.ONE_DAY_IN_SECONDS

        if math.floor(days) < days:
            days = math.floor(days) + 1
        else:
            days = math.floor(days)

        for day in range(days):
            t = time.gmtime(requestStartTime + day * NCMetricsHandler.ONE_DAY_IN_SECONDS)
            combinedName = DataPointUtil.buildMetricCombinedName(request["metricName"], t)

            try:
                result = self.getDataPoints(combinedName, requestStartTime, requestEndTime)
            except Exception as e:
                print("Exception while getting data points")
                print(e)
                break

            datapoints += result["dataPoints"]
            if day == days - 1:
                resultEndTime = requestEndTime
            else:
                resultEndTime = NCMetricsHandler.roundTimeDown(t) + NCMetricsHandler.ONE_DAY_IN_SECONDS

        return {"data": datapoints, "resultStartTime": resultStartTime, "resultEndTime": resultEndTime}

    def getDataPoints(self, combinedName, startTime, endTime):
        return self.dao.getOnlinePlayerCount(combinedName, startTime, endTime)

    @staticmethod
    def roundTimeDown(t):
        return time.mktime(time.strptime(time.strftime(DataPointUtil.DATE_FORMAT, t), DataPointUtil.DATE_FORMAT))
