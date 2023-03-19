from flask import Flask, request, Response
from flask_limiter import Limiter
from http import HTTPStatus
import time
import boto3
from NCMetricsDao import NCMetricsDao
from NCMetricsHandler import NCMetricsHandler

app = Flask(__name__)
limiter = Limiter(
    lambda: "Server",
    app=app,
    storage_uri="memory://",
)
dynamoDBResource = boto3.resource('dynamodb', region_name="us-west-2")
ncMetricsDao = NCMetricsDao(dynamoDBResource)
ncMetricsHandler = NCMetricsHandler(ncMetricsDao)


@app.route("/NCMetrics", methods=["GET"])
@limiter.limit("20 per second", key_func=lambda: "NCMetrics")
def getMetrics():
    metricName = request.args.get("metricName")
    startTime = request.args.get("startTime")
    endTime = request.args.get("endTime")

    if not metricName or not startTime or not endTime:
        print("invalid args", metricName, startTime, endTime)
        return Response(response={"errorMessage":"metricName, startTime, endTime url parameters must be included",
                                  "data": [],
                                  "resultStartTime": 0,
                                  "resultEndTime": 0},
                        status=HTTPStatus.BAD_REQUEST)

    startTime = int(startTime)
    endTime = int(endTime)
    
    result = ncMetricsHandler.handle({"metricName": metricName,
                                      "startTime": startTime,
                                      "endTime": endTime})
    datapoints = result["data"]

    cleanedDataPoints = []
    for dataPoint in datapoints:
        cleanedDataPoints.append({"playerCount": dataPoint["playerCount"], "time": dataPoint["time"]})
    return {"data": cleanedDataPoints,
            "resultStartTime": result["resultStartTime"],
            "resultEndTime": result["resultEndTime"],
            "errorMessage": "None"}
