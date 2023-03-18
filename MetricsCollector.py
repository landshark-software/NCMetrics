import requests
import boto3
from NCMetricsDao import NCMetricsDao
from DataPointUtil import DataPointUtil

MC_STATUS_NC_URL = "https://api.mcsrvstat.us/2/mc.nostalgiacraft.fun"
dynamoDBResource = boto3.resource('dynamodb')
ncMetricsDao = NCMetricsDao(dynamoDBResource)


def main():
    response = requests.get(MC_STATUS_NC_URL).json()
    if response["online"]:
        print("Players online: ", response["players"]["online"])
        playerCountDataPoint = DataPointUtil.createPlayerCountDataPoint(response["players"]["online"])
        ncMetricsDao.putOnlinePlayerCount(playerCountDataPoint)


if __name__ == '__main__':
    main()

