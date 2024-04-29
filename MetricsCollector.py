from mcstatus import JavaServer
import boto3
from NCMetricsDao import NCMetricsDao
from DataPointUtil import DataPointUtil

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
    print("Players online: ", status.players.online, " Latency: ", status.latency)

    playerCountDataPoint = DataPointUtil.createDataPoint("PlayerCount", status.players.online)
    ncMetricsDao.putDataPoint(playerCountDataPoint)

    latencyDataPoint = DataPointUtil.createDataPoint("NCPingLatency", status.latency)
    ncMetricsDao.putDataPoint(latencyDataPoint)

if __name__ == '__main__':
    main()

