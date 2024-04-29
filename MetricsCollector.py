from mcstatus import JavaServer
import boto3
from NCMetricsDao import NCMetricsDao
from DataPointUtil import DataPointUtil
from decimal import Decimal

NC_URL = "mc.NostalgiaCraft.fun:25565"
dynamoDBResource = boto3.resource('dynamodb',region_name="us-west-2")
ncMetricsDao = NCMetricsDao(dynamoDBResource)
server = JavaServer.lookup(NC_URL)

def main():
    try:
        status = server.status()
    except Exception as e:
        # put availability 0 metric here
        raise e

    playerCountDataPoint = DataPointUtil.createDataPoint("PlayerCount", status.players.online)
    ncMetricsDao.putData(playerCountDataPoint)

    latencyDataPoint = DataPointUtil.createDataPoint("NCPingLatency", int(status.latency))
    ncMetricsDao.putData(latencyDataPoint)

if __name__ == '__main__':
    main()

