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
dynamoDBResource = boto3.resource('dynamodb',region_name="us-west-2")
ncMetricsDao = NCMetricsDao(dynamoDBResource)
ncMetricsHandler = NCMetricsHandler(ncMetricsDao)


@app.route("/NCMetrics", methods=["GET"])
@limiter.limit("20 per second", key_func=lambda: "NCMetrics")
def getMetrics():
    metricName = request.args.get("metricName")
    startTime = int(request.args.get("startTime"))
    endTime = int(request.args.get("endTime"))

    if not metricName or not startTime or not endTime:
        return Response(response="metricName, startTime, endTime url parameters must be included",
                        status=HTTPStatus.BAD_REQUEST)

    datapoints = ncMetricsHandler.handle({"metricName": metricName,
                                          "startTime": startTime,
                                          "endTime": endTime})

    result = []
    for dataPoint in datapoints:
        result.append({"playerCount": dataPoint["playerCount"], "time": dataPoint["time"]})
    return result
