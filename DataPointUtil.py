import time

class DataPointUtil:
    DATA_RETENTION_PERIOD = 2592000  # 1 month in seconds

    @staticmethod
    def createPlayerCountDataPoint(playerCount):
        currentTime = DataPointUtil._getCurrentEpoch()
        ttl = DataPointUtil._getTimeToLive(currentTime)
        return {
            "metricCombinedName": DataPointUtil.buildMetricCombinedName("PlayerCount", time.gmtime()),  # partition key
            "time": currentTime,  # sort key
            "playerCount": playerCount,
            "timeToLive": ttl
        }

    @staticmethod
    def buildMetricCombinedName(metricName, t):
        return metricName + "-" + DataPointUtil._getDate(t)

    @staticmethod
    def _getCurrentEpoch():
        return int(time.time())

    @staticmethod
    def _getTimeToLive(currentTime):
        return currentTime + DataPointUtil.DATA_RETENTION_PERIOD

    @staticmethod
    def _getDate(t):
        return time.strftime("%Y/%m/%d", t)