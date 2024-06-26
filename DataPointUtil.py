import time

class DataPointUtil:
    DATA_RETENTION_PERIOD = 365 * 24 * 60 * 60  # 1 year in seconds
    DATE_FORMAT = "%Y/%m/%d"

    @staticmethod
    def createDataPoint(metricName, value):
        currentTime = DataPointUtil._getCurrentEpoch()
        ttl = DataPointUtil._getTimeToLive(currentTime)
        return {
            "metricCombinedName": DataPointUtil.buildMetricCombinedName(metricName, time.gmtime()),  # partition key
            "time": currentTime,  # sort key
            "value": value,
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
        return time.strftime(DataPointUtil.DATE_FORMAT, t)
