from flask import Flask, request, Response
from flask_limiter import Limiter
from http import HTTPStatus
import time
import boto3
from NCMetricsDao import NCMetricsDao
from NCMetricsHandler import NCMetricsHandler
from werkzeug.middleware.proxy_fix import ProxyFix
import os

X_FOR_HEADERS = int(os.environ['X_FOR_HEADERS'])
X_PROTO_HEADERS = int(os.environ['X_PROTO_HEADERS'])
X_HOST_HEADERS = int(os.environ['X_HOST_HEADERS'])
X_PREFIX_HEADERS = int(os.environ['X_PREFIX_HEADERS'])

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=X_FOR_HEADERS, x_proto=X_PROTO_HEADERS, x_host=X_HOST_HEADERS, x_prefix=X_PREFIX_HEADERS
)

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
        cleanedDataPoints.append({"value": dataPoint["playerCount"] if "playerCount" in dataPoint else dataPoint["value"], "time": dataPoint["time"]})
    return {"data": cleanedDataPoints,
            "resultStartTime": result["resultStartTime"],
            "resultEndTime": result["resultEndTime"],
            "errorMessage": "None"}


ProxyFix

